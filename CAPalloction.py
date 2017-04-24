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
picroPower = 1.0   ##微基站功率/w
noisePower = 9.0   ##dB
Rmin = 1200 ##单位byte/s
Rmax = 4500 ##单位byte/s
# macropathLoss = 128.1 + 37.6*np.log10(d) ###d表示用户与基站的距离
# micropathLoss = 145.4+37.5*np.log10(d)   ###/km

macroAveragePower = macroPower/channelnum  ##宏基站的信道平均功率
microAveragePower = picroPower/channelnum  ##微基站的信道平均功率
channelbandwidth = bandwidth/channelnum  ##每个信道的带宽
# macroChannelSet = [i for i in xrange(64)]  ##宏基站信道编号
# picroChannelSet = [i for i in xrange(64)]  ##微基站信道编号
ChannelSet = [[-1 for i in xrange((channelnum))] for j in xrange(TotalNum)]#生成基站的信道列表，每一行是一个基站的信道集合 ，第0行代表宏基站

def interfere(BS_n,chan_s):
    ##不同基站相同信道才会产生干扰，除此之外只有噪声,基站BS_n 在信道chan_s上的干扰
    interence = 0
    for i in xrange(len(TotalNum)):#循环基站数量次
        if(i!=BS_n):##如果
            pass
    return interence
    
def sinr(BSid,Userchannellist,chan):###BSid基站类型：0:picoBS;1:MacroBS，已分配信道列表Userchannellist,chan要给用户分配的信道
    
    """
    信噪比公式 sinr =  P(n,s)*D(n,k)**(-4)/(Interference+Noise)
    Interference = sum(P(m,s)*D(m,k)**(-4)) if m!=n
    Noise = P(total)*L(n)/a
    D(n,k):用户k到链接基站n的距离
    L(n):基站n的覆盖半径
    """
    
def classifyUser(ux,uy,bsx,bsy,r):
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
    
#### 接收用户的坐标位置和基站的坐标位置
UserX,UserY, BSX,BSY = Draw(samples_num= usernum,R = 500)#接收用户坐标和基站坐标(不包括宏基站)
#调用分类函数将用户按它所在的基站分类
BSCover = classifyUser(UserX,UserY,BSX,BSY, r=100)





        

    
























































