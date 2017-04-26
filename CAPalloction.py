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

macroR = 500.0     ##宏基站的覆盖半径/m
microR = 100.0     ##微基站的覆盖半径/m
channelnum = 64    ##信道数量
bandwidth = 150.0 ##带宽/MHz,w->dbm:dbm = 10log10(w/1mw)=30+10log10(W),#print 40+10*np.log10(15)=51.
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
# macroChannelSet = [i for i in xrange(64)]  ##宏基站信道编号
# picroChannelSet = [i for i in xrange(64)]  ##微基站信道编号
# ChannelSet = [[-1 for i in xrange((channelnum))] for j in xrange(TotalNum)]#生成基站的信道列表，每一行是一个基站的信道集合 ，第0行代表宏基站
 

    
def sinr(BSid,Userchannellist,chan):###BSid基站类型：0:picoBS;1:MacroBS，已分配信道列表Userchannellist,chan要给用户分配的信道
    
    """
    信噪比公式 sinr =  P(n,s)*D(n,k)**(-4)/(Interference+Noise)
    Interference = sum(P(m,s)*D(m,k)**(-4)) if m!=n
    Noise = P(total)*L(n)/a
    D(n,k):用户k到链接基站n的距离
    L(n):基站n的覆盖半径
    """
    
def classifyUser(ux,uy,bsx,bsy,r):##定义一个分类函数
    '''
        将用户按照：是否处于某个基站覆盖范围分类,r基站的半径
    
    '''
    if(len(ux)>len(uy)):ux = ux[:len(uy)]
    elif(len(ux)<len(uy)):uy = uy[:len(ux)]
    if(len(bsx)>len(bsy)):ux = ux[:len(uy)]
    elif(len(bsx)<len(bsy)):uy = uy[:len(ux)]
    #初始化一个列表，每一行代表一个基站范围内的用户列表
    BSCoverage = []
    for i in xrange(len(BSX)):##处于两个基站交叉区域的用户会出现在两个基站的list中
        BSCoverage.append( [(x,y) for x,y in zip(ux ,uy) if distance(x, y, bsx[i], bsy[i])<=r])
    temp  =[]
    for i in BSCoverage:
        temp += i
    #过滤掉重复的坐标
    temp = list(set(temp))
    #筛选只在宏基站内的用户坐标, 最后一行为只分布在宏基站范围内的用户
    BSCoverage.append([(x,y) for x,y in zip(UserX,UserY) if (x,y) not in temp])
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

def interfere(n,s,chanlist,BSX,BSY):
    '''
    ##不同基站相同信道才会产生干扰，除此之外只有噪声,基站BS_n 在信道chan_s上的干扰,不同基站只要分配了相同编号的信道，
    ##无论是否给同一个用户都会相互干扰，只是相同编号的信道分配给同一个用户干扰最大
    chanlist 是信道的分配列表 等同于下面的BSchanAllocate
    '''
    interf = 0
    for i in xrange(len(TotalNum)):#循环基站数量次
        if(i!=n and chanlist[s]!=-1):##如果不是参数中的基站,且信道已经分配给用户
            
            k = chanlist[n][s] #定位连接基站n分配信道s的用户
            d = distance(k[0],k[1],BSX[i],BSY[i])
            p = microAveragePower
            interf += p*(d**(-4))
                         
    return interf

# 用户的坐标位置和基站的坐标位置
UserX,UserY, BSX,BSY = Draw(samples_num= usernum,R = 500)#接收用户坐标和基站坐标(不包括宏基站)

##基站到用户的距离DM,行代表某个基站，列代表用户
DM = getDM(UserX,UserY,BSX,BSY)


#调用分类函数将用户按它所在的基站分类
BSCover = classifyUser(UserX,UserY,BSX,BSY, r=100)
"""
BSCover 一行代表一个基站 下的所有用户
"""
BSchanAllocate = [[-1]*channelnum]*TotalNum  ####定义一个信道分配的矩阵，行代表一个基站，列代表基站的信道

for bs in xrange(BSCover):##bs表示当前循环的基站下所有用户的集合bs = [user(0),user(1),user(1),...,user(n)]
    n = BSCover.index(bs)##获取当前基站对应的下标值，以定位当前基站(BSX[n],BSY[n])
    if len(bs)!=0 : ##判断bs中如果有用户的话,且不是最有一个基站，最后一个基站是宏基站
        ##求得基站范围内的用户与当前基站的距离
        D = []
        for useri in bs:
            d = distance(useri[0],useri[1],BSX[n],BSY[n])
            D.append(d)
        
        if n!=(len(BSCover)-1): 
            pt = microAveragePower###微基站的平均信道功率
            P = picoPower  ##基站总共功率
            radius = 0.1##km
        else:
            pt = macroAveragePower##宏基站的平均信道功率
            P = macroPower
            radius = 0.5##km
        Interf = 0 ##干扰
        AvgBand = channelbandwidth##每个信道的平均带宽
        ##利用循环求得
        '''
        #初始化一个信道分配矩阵，每一行代表一个基站的信道的分配，未分配的信道记为-1,如果某个信道分配给用户了，则标记为 用户   坐标 
        BSchanAllocate = [
        
        BS0 : [-1,-1,....,-1]
        BS1 : [-1,-1,....,-1]
        BS2 : [-1,-1,....,-1]
        BS3 : [-1,-1,....,-1]
        BS4 : [-1,-1,....,-1]
        BS5 : [-1,-1,....,-1]
        .
        ]
        '''
        
        for user in bs:
            R = []#初始化一个速度列表，当前循环的基站下覆盖的各个用户：假设信道分配给每一个用户的情形下得到的速率
            for j in xrange(channelnum):
                Interf = interfere(n, s, chanlist, BSX, BSY)
                sinr = pt*(D[bs.index(user)])**(-4)/(Interf + P*radius**(-4)/alpha)
                r = AvgBand*log2(1+sinr)
                R.append(r)
        
        
        
        
'''
--------------------------------------------类  分 界  线--------------------------------------------

'''
class BS(object):
    """定义一个抽象 基站类"""
    def __init__(self,channelnum,totalpower,coverage,dtoAlluser):
        """channelnum信道数量   totalPower基站总功率，Coverage基站覆盖范围半径 ,dtoAlluser基站到各个用户的距离列表
        #是一个列表，每一列代表:当前基站与用户(用户编号用列表中对应的下标表示)的距离
        dtoAlluser[i]#表示当前基站到用户i的距离
        """
        self.channelnum = channelnum #信道数量
        self.totalpower = totalpower ##基站总功率
        self.channelpower = [0]*channelnum ##每条信道的功率初始化为0
        self.coverage = coverage #基站的覆盖半径
        self.dtoAlluser = dtoAlluser #基站到所有用户的距离列表
        self.underCover = [] ##在当前基站覆盖下的用户集合列表
        
    def getuser(self):#获取在当前基站下的用户集合
        """得到当前基站覆盖范围内的用户"""
        
        for d in xrange(len(self.dtoAlluser)):##在距离列表中，按其长度做循环
            if self.dtoAlluser[d] <= self.coverage:##判断距离小于基站覆盖半径
                self.underCover.append(d)#把用户编号追加到当前基站的用户列表中去
        return self.underCover
    
    def userintwo(self):
        """处于两个基站交叉区域的用户"""
        pass
    
    def interence(self):
        #同一个基站分配信道，所以不存在不同基站的相同信道的干扰。只有噪声
        inter = 0
        return inter
    
    def userRate(self):
        #当前基站范围内的用户与当前基站的所有信道的速率
        R = [[0]]
        p = self.totalpower/channelnum
        N = 9.0
        Interfe = self.interfere()
        for i in self.underCover:##当前基站的用户数量作为外循环，i表示用户编号
            r = []
            for j in xrange(channelnum):#以当前的基站信道数量作为内循环
                r.append(p*(self.dtoAlluser[i])**(-4)/(Interfe+N))
            R.append(r)    
        return R
      
    def chanAllocate(self):
        '''只为只在当前基站中的用户分配信道，如果出现基站交叉范围共存的用户先不管，依旧按照本基站的原则分配信道'''
        R = self.userRate()## R每一行代表：一个用户与当前基站所有信道的速率值 
        for i in self.underCover:##按用户分配信道
            pass

class User(object):
    """定义一个用户类"""
    def __init__(self):#初始化
        self.chanNum = 0   ##用户占用的信道数量
        self.inBScover = [] ##用户所在的基站,如果在多个基站交叉区域，则列表中会出现他所在的所有基站
        self.chanlist = [] ##用户占用的信道列表，实际上应该是一个矩阵，每一行代表占用的一个基站的信道
        self.rate = 0
        self.Rmin = 1200 #kbps
        
if __name__=="__main__":
    