# -*- coding:utf-8 -*-
from random import random,uniform
import numpy as np
import matplotlib.pyplot as plt
from coverage import Draw
from SINR import distance
from numpy import log2
import random
"""
信道分配的代码
信道分配的原则是：
(1)先随机分配信道给用户，满足用户的最低速率要求
(2)从剩余的信道的集合中(如果还存在剩余信道的话），将未分配的信道分给信噪比大用户

"""
"""   
一个cell中的包含一个宏基站、两个微基站，每个基站的信道数量都是64个，
用户设备使用的信道的为此用户有效信道，其他的是为干扰。
一个用户在一个地点只能连接一个离他最近基站，
这样的话如果存在剩余信道的话，基站只能把剩余信道分配给它覆盖范围内的信道
求SINR值时，使用的信道功率是平均功率

"""
   
### MinRate表示用户的速度

# ##用户距离基站的位置
# userLocation = [float(format(uniform(50,120),'.1f')) for i in xrange(24)]
##用户最大速率，即MOS(4.5)时对应的速率
maxRate = 1500 #kbit/s
### 下面是初始化信息
MacroNum = 1
PicoNum = 6
FemtoNum = 2
RelayNum = 2
TotalNum =  MacroNum+PicoNum+FemtoNum+RelayNum
usernum = np.random.randint(20,50)
# usernum = np.random.randint(50,60)
print "usernum=%d"%usernum

macroR = 500.0     ##宏基站的覆盖半径/m
microR = 100.0     ##微基站的覆盖半径/m
channelnum = 64    ##信道数量
bandwidth = 150.0*(10**3) ##带宽/MHz,w->dbm:dbm = 10log10(w/1mw)=30+10log10(W),#print 40+10*np.log10(15)=51.
macroPower = 20.0  ##宏基站功率/w
picoPower = 1.0   ##微基站功率/w
noisePower = 9.0   ##dB
alpha = 10
Rmin = 1200 ##单位kbps
Rmax = 4500 ##单位kbps
# macropathLoss = 128.1 + 37.6*np.log10(d) ###d表示用户与基站的距离
# micropathLoss = 145.4+37.5*np.log10(d)   ###/km

macroAveragePower = macroPower/channelnum  ##宏基站的信道平均功率
microAveragePower = picoPower/channelnum  ##微基站的信道平均功率
channelbandwidth = bandwidth/channelnum  ##每个信道的带宽

# 用户的坐标位置和基站的坐标位置
UserX,UserY, BSX,BSY = Draw(samples_num= usernum,R = 500)#接收用户坐标和基站坐标(不包括宏基站)

''' 
"""------------------------------------此 函 数 已 经 废 弃----------------------------------------"""   
def sinr(BSid,Userchannellist,chan):###BSid基站类型：0:picoBS;1:MacroBS，已分配信道列表Userchannellist,chan要给用户分配的信道
    """
    信噪比公式 sinr =  P(n,s)*D(n,k)**(-4)/(Interference+Noise)
    Interference = sum(P(m,s)*D(m,k)**(-4)) if m!=n
    Noise = P(total)*L(n)/a
    D(n,k):用户k到链接基站n的距离
    L(n):基站n的覆盖半径
    """
    pass
 '''
    
def classifyUser(r,ux=UserX,uy=UserY,bsx=BSX,bsy=BSY):##定义一个分类函数
    '''
        将用户按照：是否处于某个基站覆盖范围分类,r基站的半径
        基站坐标不能包含宏基站坐标，宏基站用户需等待所有其他类型的基站分类完毕之后才能得到
    
    '''
    if(len(ux)>len(uy)):ux = ux[:len(uy)]
    elif(len(ux)<len(uy)):uy = uy[:len(ux)]
    if(len(bsx)>len(bsy)):ux = ux[:len(uy)]
    elif(len(bsx)<len(bsy)):uy = uy[:len(ux)]
    #初始化一个列表，每一行代表一个基站范围内的用户列表
    BSCoverage = []
    for i in xrange(len(bsx)):##处于两个基站交叉区域的用户会出现在两个基站的list中
        BSCoverage.append( [(x,y) for x,y in zip(ux ,uy) if distance(x, y, bsx[i], bsy[i])<=r])
    temp  =[]
    for i in BSCoverage:
        temp += i
    ###过滤掉重复的坐标
    temp = list(set(temp))
    ###筛选只在宏基站内的用户坐标, 最后一行为只分布在宏基站范围内的用户
    BSCoverage.append([(x,y) for x,y in zip(ux,uy) if (x,y) not in temp])
    return BSCoverage

def getDM(ux,uy,bsx,bsy):
    '''求基站到所有用户的距离矩阵,行代表基站，列代表用户 DM[i][j]表示:基站i到用户j的距离'''
    if(len(ux)==len(uy) and len(bsx)==len(bsy)):
        DM=[]
        for i in xrange(len(bsx)):
            dm = []
            for j in xrange(len(ux)):
                d = distance(ux[j],uy[j],bsx[i],bsy[i])
                dm.append(d)
            DM.append(dm)
    else:exit(0)
    return DM

def interfere(n,s,chanlist,bsx=BSX,bsy=BSY):
    '''
    ##不同基站相同信道才会产生干扰，除此之外只有噪声,基站BS_n 在信道chan_s上的干扰,不同基站只要分配了相同编号的信道，
    ##无论是否给同一个用户都会相互干扰，只是相同编号的信道分配给同一个用户干扰最大
    chanlist 是信道的分配列表 等同于下面的BSchanAllocate，已分配信道是用用户坐标表示的，未分配信道值为-1
    '''
    BSX +=[0]
    BSY +=[0]
    interf = 0
    for i in xrange(len(chanlist)):#循环基站数量次
        if(i!=n and chanlist[i][s]!=-1):##如果不是参数中的基站,且信道已经分配给用户(信道值为-1说明：此信道未分配，值为用户坐标说明此信道已经分配给该坐标用户)
            k = chanlist[n][s] #定位连接基站n分配信道s的用户
            
            d = distance(k[0],k[1],bsx[i],bsy[i])
            if i!=(len(chanlist)-1):#最后一个基站为宏基站，如果不是最后一个基站，功率p为微基站功率
                p = microAveragePower
            else:  #否则为宏基站功率
                p = macroAveragePower
            interf += p*(d**(-4))
    return interf

##基站到用户的距离DM,行代表某个基站，列代表用户
# DM = getDM(UserX,UserY,BSX,BSY)

#调用分类函数将用户按它所在的基站分类
"""
    BSCover 一行代表一个基站 下的所有用户
"""

'''
        #初始化一个信道分配矩阵，每一行代表一个基站的信道的分配，未分配的信道记为-1,如果某个信道分配给用户了，则标记为 用户   坐标 
        BSchanAllocate = [        
        BS0 : [-1,-1,....,-1]
        BS1 : [-1,-1,....,-1]
        BS2 : [-1,-1,....,-1]
        BS3 : [-1,-1,....,-1]
        BS4 : [-1,-1,....,-1]
        BS5 : [-1,-1,....,-1]
        ]
        '''
def RateNow(chanlist,user,bsx=BSX,bsy=BSY):
    """
           根据当前的用户分配求当前用户的速率 ,BSchanAllocate是信道分配列表，user表示要获取速率的用户
    """
    BSX +=[0]
    BSY +=[0]
    rate = 0##初始速率设置为0
    for BSn in xrange(len(chanlist)):##以信道分配的矩阵长度作为循环次数
        AvgBand = channelbandwidth
        if BSn!=(len(chanlist)-1):
            pt = pt = microAveragePower###微基站的平均信道功率
            P = picoPower  ##基站总共功率
            radius = 100##m
        else:
            pt =macroAveragePower###微基站的平均信道功率
            P = macroPower  ##基站总共功率
            radius = 500##m
            
        for userindex in xrange(len(chanlist[BSn])):##第BSn个基站信道长度做循环次数
            if user == chanlist[BSn][userindex]:###判断用户是否在当前循环基站分配了信道
                Interf = interfere(BSn, userindex, chanlist, bsx, bsy)##求干扰
                d = distance(user[0],user[1],bsx[BSn],bsy[BSn])###求用户与基站的距离
                sinr = pt*(d)**(-4)/(Interf + P*radius**(-4)/alpha)##求信噪比sinr
                rate += AvgBand*log2(1+sinr)
    
    return rate
    

def channelAllocate(BSCover,bsx=BSX,bsy=BSY):
    """
    
    """
    BSX=BSX+[0]
    BSY=BSY+[0]
    BSchanAllocate = [[-1]*channelnum]*TotalNum  ####定义一个信道分配的矩阵，行代表一个基站，列代表基站的信道

    for n in xrange(len(BSCover)):##n表示当前循环的基站下所有用户的集合编号
    
        if len(BSCover[n]) > 0 : ##当前编号对应的基站中如果有用户的话，继续执行
            ##初始化计算基站信息的数据
            if n!=(len(BSCover)-1): 
                pt = microAveragePower###微基站的平均信道功率
                P = picoPower  ##基站总共功率
                radius = 100##m
            else:
                pt = macroAveragePower##宏基站的平均信道功率
                P = macroPower
                radius = 500##m
    
            AvgBand = channelbandwidth##每个信道的平均带宽

            """第一步：获得当前前基站下：每一个用户与所有信道连接条件下得到的用户速率"""
            R = []#初始化一个速度矩阵，一行代表当前基站下一个用户与所有信道的链接所获得速率值列表，列代表信道
            for userindex in xrange(len(BSCover[n])):##userindex表示对应用户的下标值
                d = distance(BSCover[n][userindex][0],BSCover[n][userindex][1],bsx[n],bsy[n])## 用户与当前基站的距离
                r = []
                for j in xrange(channelnum):
                    
                    Interf = interfere(n, j, BSchanAllocate, BSX, BSY)##n表示的是基站，j 是信道，chanlist是信道分配的列表
#                     sinr = pt*(D[bs.index(user)])**(-4)/(Interf + P*radius**(-4)/alpha)##求sinr
                    sinr = pt*(d)**(-4)/(Interf + P*radius**(-4)/alpha)##求sinr
                    rate = AvgBand*log2(1+sinr)
                    r.append(rate)
                    ##将得到的速率值r，追加到当前 用户速度一维列表中,
                    #每一个速率值对应一个信道:R =[r0,r1,r2,..]
                    
                R.append(r)
            #print len(R)
            
            """第二步：进行信道的分配，使用的贪心算法，用户选择(或者说基站分配)当前速率值最大的信道"""
            for userj in xrange(len(BSCover[n])):
                j = userj##获取当前用户的下标(用户坐标不存在两个相同的)
                print "基站编号: %d"%(n)
                
                Rnow=RateNow(BSchanAllocate, BSCover[n][j], BSX, BSY)##表示用户当下的速率，已改正【【【应该从信道分配list中获取当前用户的当前速率，刚开始用户的求得速率值为0】】】 
                while(Rnow < Rmin):##用户速率大于最低速率，
                    if BSchanAllocate[n].count(-1)>0:#当前基站还有未分配的信道，还有一个else，如果当前基站的信道数量不够该如何处理
                        Rnow += max(R[j])
                        chanid = R[j].index(max(R[j]))##将当前用户速率值最大值对应的第一个(可能会出现速率并列最大的)信道标号赋值给chanid
                        BSchanAllocate[n][chanid]=userj##在基站n的信道s对应位置写入用户坐标
                        print "channelid:%d user:%s"%(chanid,userj)
                        
                        for rm in xrange(len(R)):##循环速率矩阵行，将本基站其他用户对应这条信道的速率设置为0
    #                         row = R.index(rm)#获取行坐标
                            for rn in xrange(len(R[j])):
    #                             col = rm.index(rn)##获取列坐标
                                if (rn==chanid):R[rm][rn]=0##将已经分配的信道对应其他用户的速率矩阵位置设置为0，表示此信道已经分配不能再分配其他人
                                  
                    else: ###如果当前基站的信道已经分配完毕，暂时输出下面的字符串，后续会继续处理这种情况
                        
                        print "All channels are busy"
                        exit(0)
            print "\n"
#         n = n + 1 ##当前基站的分配完毕，n+1进入下一个基站的额信道分配
           
    return BSchanAllocate    

if __name__=="__main__":
    
    BSCover = classifyUser(r=100)
    ##将用户按照基站的覆盖范围分类之后，将宏基站的坐标加入到基站坐标列表中去
#     s = 0
#     for i in BSCover:
#         print i
#         s += len(i)
#         print "len(i)=%d"%len(i)
#     print "sum user:%d"%s

    for i in [0,1]:  
        BSchanAllocate = channelAllocate(BSCover)
        for i in BSchanAllocate:
            print i
                
    