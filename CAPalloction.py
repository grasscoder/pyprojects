# -*- coding:utf-8 -*-
from random import random,uniform
import numpy as np
import matplotlib.pyplot as plt
# from coverage import Draw ##用户和基站的坐标已改成从文件中直接读取，不需要使用的时候随机生成了2017年5月15日09:19:37改
from SINR import distance
from numpy import log2
from memory_profiler import profile
# from pso import PSO 


"""
一个cell中的包含一个宏基站、两个微基站，每个基站的信道数量都是64个，
用户设备使用的信道的为此用户有效信道，其他的是为干扰。
一个用户在一个地点只能连接一个离他最近基站，
这样的话如果存在剩余信道的话，基站只能把剩余信道分配给它覆盖范围内的信道
求SINR值时，使用的信道功率是平均功率
"""

#---------------------------初 始 化 信 息------------------------------
##用户最大速率，即MOS(4.5)时对应的速率
maxRate = 1500 #kbit/s
MacroNum = 1
PicoNum = 6
FemtoNum = 2
RelayNum = 2
TotalNum =  MacroNum+PicoNum+FemtoNum+RelayNum##基站总数
usernum = np.random.randint(50,51)
# usernum = np.random.randint(65,66)
# print "usernum=%d"%usernum

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
maxUserConnectchanNum = 5 ##用户最大链接信道的数量
# macropathLoss = 128.1 + 37.6*np.log10(d) ###d表示用户与基站的距离
# micropathLoss = 145.4+37.5*np.log10(d)   ###/km

macroAveragePower = macroPower/channelnum  ##宏基站的信道平均功率
microAveragePower = picoPower/channelnum  ##微基站的信道平均功率
# print "宏基站信道平均功率：%s,picomeanPower:%s"%(macroAveragePower,microAveragePower)
channelbandwidth = bandwidth/channelnum  ##每个信道的带宽

#-----------------------------用 户 的 坐 标 位 置 和 基 站 的 坐 标 位 置 --------------------------------
'''这些信息已经改成从文件中获取，不需要每次运行的时候重新生成了'''
# UserX,UserY, BSX,BSY = Draw(samples_num= usernum,R = 500)#接收用户坐标和基站坐标(不包括宏基站)2017年5月15日09:20:02改

''' 
# ------------------------------------此 函 数 已 经 废 弃----------------------------------------   
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
 
#-----------------------------定 义 一个 文 件 读 取 的 函 数 ------------------------------------------
def readFile(*filename):
    '''函数的功能是从文件中读取用户信道和基站坐标的信息'''
    with open(filename[0],'r') as f:
        userx =[]
        usery =[]
        for line in f:
            L = line.rstrip("\n").split(" ")##去掉文件中每一行的换行符，并且按照空格分割成list
            userx.append(float(L[1]))
            usery.append(float(L[2]))
            
    with open(filename[1],'r') as f1:
        bsx = []
        bsy = []
        for line1 in f1:
            L1 = line1.rstrip("\n").split(" ")
            bsx.append(float(L1[1]))
            bsy.append(float(L1[2]))
    return userx,usery,bsx,bsy##基站坐标中不含有宏基站坐标
            

#---------------------------------定 义 分 类 函 数----------------------------------------------
def classifyUser(r,ux,uy,bsx,bsy):##定义一个分类函数
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

#----------------------------定 义 获 取 用 户 与 基 站 距 离 的 函  数 ----------------------------------
def getDL(ux,uy,bsx,bsy):
    '''求一个用户到所有基站的距离列表'''
    if len(bsx)==len(bsy):
        dm=[]
        for i in xrange(len(bsx)):
            d = distance(ux,uy,bsx[i],bsy[i])
            dm.append(d)
    else:
        print "len(bsx)!=len(bsy),please recheck"
        exit(0)
    return dm
#---------------------------------定 义 求 干 扰 的 函 数 -------------------------------------------
def interfere(n,s,chanlist,bsx,bsy):
    '''
    ##不同基站相同信道才会产生干扰，除此之外只有噪声,基站BS_n 在信道chan_s上的干扰,不同基站只要分配了相同编号的信道，
    ##无论是否给同一个用户都会相互干扰，只是相同编号的信道分配给同一个用户干扰最大
    chanlist 是信道的分配矩阵 等同于下面的BSchanAllocate，已分配信道的位置将-1修改为用用户坐标(UserX,UserY)，未分配信道值为-1
    
         信道分配矩阵的每一行必须与基站坐标的每一行对应起来，最后一行是宏基站的信道分配
    '''
    
    interf = 0.0
    if (len(chanlist)==len(bsx)):###必须保证信道分配矩阵 的行数与基站的数量相同，便于计算距离获取基站的坐标值
        k = chanlist[n][s]
        if k==-1:return interf  ###所求的信道没有分配不存在干扰，即interf=0
        for i in xrange(len(chanlist)):#循环基站数量次
            if(i!=n and chanlist[i][s]!=-1):##如果不是参数中的基站,且信道已经分配给用户(信道值为-1说明：此信道未分配，值为用户坐标说明此信道已经分配给该坐标用户)
#                 k = chanlist[n][s] #定位连接基站n分配信道s的用户(可能出现这样的情况这个用户本身值是-1，假如它分配给用户求其他信道对它的干扰)
#                 print "k=%d"%k
                d = distance(k[0],k[1],bsx[i],bsy[i])
                if i!=(len(chanlist)-1):#最后一个基站为宏基站，如果不是最后一个基站，功率p为微基站功率
                    p = microAveragePower
                else:  #否则为宏基站功率
                    p = macroAveragePower
                interf += p*(d**(-4))
    
        return interf

#----------------------------重 新 定 义 一 个 求 干 扰 的 函 数 ------------------------------------
def interfere1(n, s, user, chanlist, bsx, bsy):
    '''
    chanlist 是信道的分配矩阵 等同于下面的BSchanAllocate，已分配信道的位置将-1修改为用用户坐标(UserX,UserY)，未分配信道值为-1
           信道分配矩阵的每一行必须与基站坐标的每一行对应起来，最后一行是宏基站的信道分配
           假设基站 n 的信道 s 分配给用户user的前提下求信噪比的值:user为假设为当前基站和信道分配的用户，类型为tuple-->(userx,usery)
    '''
    interf = 0.0
    if (len(chanlist)==len(bsx)):###必须保证信道分配矩阵 的行数与基站的数量相同，便于计算距离获取基站的坐标值
        k = user###连接基站n分配信道s的用户(假如此信道分配给用户，求其他信道对当前用户占用信道的干扰)
        for i in xrange(len(chanlist)):#循环基站数量次
            if(i!=n and chanlist[i][s]!=-1):##如果不是参数中的基站,且信道已经分配给用户(信道值为-1说明：此信道未分配，值为用户坐标说明此信道已经分配给该坐标用户)
                d = distance(k[0],k[1],bsx[i],bsy[i])
                if i!=(len(chanlist)-1):#最后一个基站为宏基站，如果不是最后一个基站，功率p为微基站功率
                    p = microAveragePower
                else:  #否则为宏基站功率
                    p = macroAveragePower
                interf += p*(d**(-4))
    
        return interf


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
    
#-------------------------定 义 求 当 前 用 户 速 率 的 函 数 ----------------------------------------
def RateNow(chanlist,user,bsx,bsy):
    """
           根据当前的用户分配求当前用户的速率 ,BSchanAllocate是信道分配列表，user表示要获取速率的用户
    """
    rate = 0##初始速率设置为0
    if (len(chanlist)==len(bsx)):
        for BSn in xrange(len(chanlist)):##以信道分配的矩阵长度作为循环次数
            AvgBand = channelbandwidth
            if BSn!=(len(chanlist)-1):
                pt =  microAveragePower###微基站的平均信道功率
                P = picoPower  ##基站总共功率
                radius = 100##m
            else:
                pt =macroAveragePower###微基站的平均信道功率
                P = macroPower  ##基站总共功率
                radius = 500##m
                
            for userindex in xrange(len(chanlist[BSn])):##第BSn个基站信道长度做循环次数
                if user == chanlist[BSn][userindex]:###判断用户是否在当前循环基站分配了信道
                    Interf = interfere1(BSn, userindex, user, chanlist, bsx, bsy)##求干扰
                    
                    d = distance(user[0],user[1],bsx[BSn],bsy[BSn])###求用户与基站的距离
                    sinr = pt*(d)**(-4)/(Interf + P*radius**(-4)/alpha)##求信噪比sinr
                    
                    rate += AvgBand*log2(1+sinr)
    else: 
        print "function RateNow : len(bsx)!=len(chanlist)"
        print "len(bsx)=%d,len(chanlist)=%d"%(len(bsx),len(chanlist))
        exit(0)
    return rate
    
#------------------------定 义 求 用 户 信 道 速 率 的 函 数 -----------------------------------------
def userChanRate(userlist,chanlist,bsxi,bsyi):
    '''----------------由于求信噪比所需基站编号n无法得到，所以放弃此方法---------------'''
#     '''
#     userlist 只是一个基站包含多个用户的列表，是一维列表；chanlist是信道分配的列表就是下面代码中引用的BSchanAllocate 矩阵
#     bsxi,bsyi是分别是基站的坐标位置，只是一个点
#     给定一个基站下的用户组合列表，输出每个用户对应每一条信道的速率矩阵。有多少个用户速率矩阵就有多少行，
#     每行64个元素代表每个信道对应某个用户的速率值
#     '''
#     R = []#初始化一个速度矩阵，一行代表当前基站下一个用户与所有信道的链接所获得速率值列表，列代表信道
#     for userindex in xrange(len(userlist)):##userindex表示对应用户的下标值
#         d = distance(userlist[userindex][0],userlist[userindex][1],bsxi,bsyi)## 用户与当前基站的距离
#         r = []
#         for j in xrange(channelnum):
#             Interf = interfere(n, j, BSchanAllocate, bsx, bsy)##n表示的是基站，j 是信道，chanlist是信道分配的列表
# #           print "Interf=%.2f"%Interf
#             sinr = pt*(d)**(-4)/(Interf + P*radius**(-4)/alpha)##求sinr
#             rate = AvgBand*log2(1+sinr)
#             r.append(rate)
#                 ##将得到的速率值r，追加到当前 用户速度一维列表中,
#                 #每一个速率值对应一个信道:R[i] =[r0,r1,r2,..]
#         R.append(r)###最后得到的R速率矩阵，跟当前基站内用户数量直接相关，
    pass

#------------------------------定 义 求 用 户 占 用 信 道 数 量 函 数--------------------------
def userAllocatedChanNum(chanlist,user):
    '''
           此函数的功能是获取用户user分配的信道数量
    '''
    num = 0
    for i in xrange(len(chanlist)):
        num += chanlist[i].count(user)
    return num  
            
    
##-----------------------------定 义 求 信 道 分 配 的 函 数 ----------------------------------------------

# @profile

def channelAllocate(BSCover,BSchanAllocate,bsx,bsy):
    """
   BSCover:用户分类的列表，bsx,bsy表示的是基站的坐标（）这个坐标必须包括宏基站坐标       
          对基站 范围内的用户进行信道分配，每一分配一个基站内的用户，初始化一个信道分配的列表，如果对应基站的信道分配给用户，则在这个基站对应的新到位置写入用户的坐标
    首先初始化一个信道矩阵，每一行代表一个基站(一共11个基站，宏基站在最后进行分配，所以n的值[0,10])         
    """
    if len(BSCover)!=len(bsx):
        print "channelAllocate Needs len(BSCover)==len(bsx,bsy)"
        exit(0)
    #BSchanAllocate = [[-1]*channelnum]*TotalNum ##  
    ####定义一个信道分配的矩阵，行代表一个基站，列代表基站的信道
    
    connectChanNum = {}##用户连接信道的最大数量

    for n in xrange(len(BSCover)):##n表示当前循环的基站下相应所有用户集合的编号，即基站编号
        '''第一步：初始化一些后续步骤所所需的量'''
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

            """第二步：获得当前前基站下：每一个用户与所有信道连接条件下得到的用户速率"""
            R = []#初始化一个速度矩阵，一行代表当前基站下一个用户与所有信道的链接所获得速率值列表，列代表信道
            for userindex in xrange(len(BSCover[n])):##userindex表示对应用户的下标值
                d = distance(BSCover[n][userindex][0],BSCover[n][userindex][1],bsx[n],bsy[n])## 用户与当前基站的距离
                r = []
                for j in xrange(channelnum):
                    
                    Interf = interfere1(n, j, BSCover[n][userindex], BSchanAllocate, bsx, bsy)##n表示的是基站，j 是信道，chanlist是信道分配的列表
#                     print "Interf=%f"%Interf
                    sinr = pt*(d)**(-4)/(Interf + P*radius**(-4)/alpha)##求sinr
#                     print"sinr=%f"%sinr
                    rate = AvgBand*log2(1+sinr)
                    
                    r.append(rate)
                    ##将得到的速率值r，追加到当前 用户速度一维列表中,
                    #每一个速率值对应一个信道:R[i] =[r0,r1,r2,..]
                R.append(r)###最后得到的R速率矩阵，跟当前基站内用户数量直接相关，
            
            """第三步：进行信道的分配，使用的贪心算法，用户选择(或者说基站分配)当前速率值最大的信道"""
            for userj in xrange(len(BSCover[n])):

                ##print "基站编号: %d"%(n)
                
                Rnow=RateNow(BSchanAllocate, BSCover[n][userj], bsx, bsy)##表示用户当下的速率，已改正【【【应该从信道分配list中获取当前用户的当前速率，刚开始用户的求得速率值为0】】】 
                i = 0 ##作为一个计数器使用记录当前用户分配的信道数量
                while(Rnow < Rmin):##用户速率大于最低速率，
                    
                    if BSchanAllocate[n].count(-1)>0:#当前基站还有未分配的信道，还有一个else，如果当前基站的信道数量不够该如何处理
                        
                        Rnow += max(R[userj])
                        chanid = R[userj].index(max(R[userj]))##将当前用户速率值最大值对应的第一个(可能会出现速率并列最大的)信道标号赋值给chanid
                        
                        BSchanAllocate[n][chanid]=BSCover[n][userj]##在基站n的信道s对应位置写入用户坐标
                        i += 1 ##用户信道分配的计数器
                        ##print "channelid:%d occupied by user:%s"%(chanid,BSCover[n][userj])
                        
                        for rm in xrange(len(R)):##循环速率矩阵行，将本基站其他用户对应这条信道的速率设置为0
                            R[rm][chanid] = 0##将已经分配的信道对应其他用户的速率矩阵位置设置为0，表示此信道已经分配不能再分配其他人 
                            
                    else: ###如果当前基站的信道已经分配完毕,将次用户坐标追加到（就是最后在给这个用户分配信道）临近的一个有空余信道的基站内.重新分配此基站的信道，需将原来分配的信道重新初始化为-1
                        '''如果出现当前基站信道不够分配的的情况，将基站中未分配的用户添加到别的基站用户集合中，从头开始重新分配信道'''
                        try:
                            currentBS = n##记录当前用户所在的基站编号
                            currentUser = userj##记录当前的基站范围的用户编号
                            userset = BSCover[currentBS][currentUser]##获取当前用户坐标
                            newDL = getDL(userset[0],userset[1],bsx,bsy)#####求当前用户与其他所有基站的距离列表
                            temp = min(newDL)##获取当前用户与基站距离的最小值
                            indexD = newDL.index(temp)##获取用户与基站最小距离的下标（如果小功率基站信道数量不够，距离最近的附近基站会向用户分配信道）
                            while currentBS==indexD:##判断如果当前基站是否为用户原来所在的基站，增大他的值，继续寻找
                                newDL[indexD] = 1500
                                temp = min(newDL)
                                indexD = newDL.index(temp)
                            if BSchanAllocate[indexD].count(-1)>0:##新基站有空余信道
                                BSCover[indexD].append(userset)
                                channelAllocate(BSCover[:], bsx[:], bsy[:])###递归信道分配,从追加用户的基站开始重新分配
                            else:                    
                                print "All channels are busy"
                                exit(0)
                        except:
                            print "Error" 
                            exit(0)       
    return BSchanAllocate    
#------------------------------产 生 随 机 功 率 矩 阵 的 函 数 -----------------------------
def getPower(chanlist):
    '''
            此函数的功能是根据基站信道的分配列表，得到信道的功率分配矩阵。值得注意的是:初始条件下信道的分配是基站的平均功率
            按照在瓶平均功率条件下的信道分配方案，调整信道功率的大小，会得到一系列的初始化粒子，保证每个基站的信道功率和不能超过此基站的总功率
             产生 num 个初始化粒子
            改：根据信道分配得到对应信道的的功率分配 【比例】，由于不同基站的基站功率不同为了方便，使用功率比例(等级)2017年5月26日15:58
    '''
    p = [[0 for i in xrange(len(chanlist[j]))] for j in xrange(len(chanlist))]#初始化一个功率比例值全为0的功率分配矩阵
    for i in xrange(len(chanlist)):##以基站个数做循环
            
        if chanlist[i].count(-1) < len(chanlist[i]):##如果基站存在信道分配
            k = len(chanlist[i]) - chanlist[i].count(-1)##此基站分配的信道数量
            randp = []
            for n in xrange(k):
                t = 15/64.0*uniform(0.001,1-sum(randp))##保证所有的已分配信道该比例之和小于1，缺点就是第一个产生的比例值总是最大的
                randp.append(t)
            n = 0;
            for j in xrange(len(chanlist[i])):
                if chanlist[i][j]!=-1:
                    p[i][j] = randp[n]
                    n = n + 1
    return p
def turnInToParticle (p):
    '''
            将功率矩阵转换为粒子，p为粒子功率等级分配的矩阵
    '''
    temp = []
    for i in p:
        temp = temp + i
    return temp
        
def ParticleInToMatrix(p):#函数的作用是:将一个粒子群的粒子转换为原来的二维数组(矩阵)
    '''p表示一个功率等级的粒子'''
    PRankmatrix = []#功率等级矩阵
    for i in xrange(len(p)/64):
        PRankmatrix.append(p[64*i:63+64*i])
    return PRankmatrix 
       
#------------------------------主 函 数 ---------------------------------------
if __name__=="__main__":
    
    filename = ['user.txt','bs.txt']
    UserX,UserY,BSX,BSY = readFile(*filename)
    BSCover = classifyUser(100,UserX,UserY,BSX,BSY)
    ####将宏基站的坐标加入到基站的坐标列表中
    BSX = BSX+[0.0]
    BSY = BSY+[0.0]
    #---------------------------得到An_k_s----------------------------
    An_k_s=[[0 for i in xrange(channelnum)] for j in xrange(TotalNum)] 
    BSchanAllocate=[[-1 for i in xrange(channelnum)] for j in xrange(len(BSCover))]#初始化信道分配
    for i in xrange(5):
        BSchanAllocate = channelAllocate(BSCover,BSchanAllocate,BSX,BSY)
    
    
    for i in xrange(len(BSchanAllocate)):
        print BSchanAllocate[i]
        for j in xrange(len(BSchanAllocate[i])):
            if BSchanAllocate[i][j]!=-1:
                An_k_s[i][j]=1

    ##既然信道分配已经确定了，那么平均功率所组成的一个粒子可以算作一个初始化粒子，然后针对这些已经分配信道的的用户的信道功率多做几次（20次）功率随机分配，就会产生许多不同的初始化
   
#     P = []
#     for i in xrange(15):
#         p = turnInToParticle(getPower(BSchanAllocate))
#         P.append(p)
#     for j in P:
#         print j
    p = getPower(BSchanAllocate)
    for i in xrange(len(p)):
        print p[i]
        if i==len(p)-1:
            print sum(p[i])

