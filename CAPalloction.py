# -*- coding:utf-8 -*-
from random import random,uniform
import numpy as np
import matplotlib.pyplot as plt
from coverage import Draw
from SINR import distance
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
def r_nks(BSid,transP,):###求信噪比函数
    """
    信噪比的公式为：r_nks = ptn/(sum(ptm)+ptotal*)
    """
     
    return 1 

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
userID = [i for i in range(usernum)]##用户编号
macroR = 500.0     ##宏基站的覆盖半径/m
microR = 100.0     ##微基站的覆盖半径/m
channelnum = 64    ##信道数量
bandwidth = 150.0 ##带宽/MHz,w->dbm:dbm = 10log10(w/1mw)=30+10log10(W),#print 40+10*np.log10(15)=51.
macroPower = 20.0  ##宏基站功率/w
picroPower = 1.0   ##微基站功率/w
noisePower = 9.0   ##dB
minRate = [1200 for i in xrange(usernum) ]##单位byte/s
# macropathLoss = 128.1 + 37.6*np.log10(d) ###d表示用户与基站的距离
# micropathLoss = 145.4+37.5*np.log10(d)   ###/km

macroAveragePower = macroPower/channelnum  ##宏基站的信道平均功率
microAveragePower = picroPower/channelnum  ##微基站的信道平均功率
channelbandwidth = bandwidth/channelnum  ##每个信道的带宽
# macroChannelSet = [i for i in xrange(64)]  ##宏基站信道编号
# picroChannelSet = [i for i in xrange(64)]  ##微基站信道编号
ChannelSet = [[i for i in xrange((channelnum))] for j in xrange(TotalNum)]#生成基站的信道列表，每一行是一个基站的信道集合 ，第0行代表宏基站
# for s in ChannelSet:
#     print s
# print len(ChannelSet)


#### 接收用户的坐标位置和基站的坐标位置
UserX,UserY, BSX,BSY = Draw(samples_num= usernum,R = 500)#接收用户坐标和基站坐标(不包括宏基站)

#初始化一个列表，每一行代表一个基站范围内的用户列表
BS = [0]*(TotalNum-1)


##用户编号与他们到其他基站的距离
# for k,i,j in zip(userID,UserX,UserY):
#     PBS1.append(k if distance(i,j,0,0)<=100) 
#     PBS2.append((k,distance(i,j,250,250))) 
#     PBS3.append((k,distance(i,j,-250,-250))) 
#     k = k + 1
###以用户所在基站范围为标准将用户分类
for i in xrange(len(BSX)):
    BS [i] = [(x,y) for x,y in zip(UserX ,UserY) if distance(x, y, BSX[i], BSY[i])<=100]
 
temp  =[]
for i in BS:
    temp += i
#过滤掉重复的坐标
temp = list(set(temp))
# 最后一行是不在其他基站范围，只在宏基站内的用户坐标
BS.append([(x,y) for x,y in zip(UserX,UserY) if (x,y) not in temp])

##用户离哪个基站近，哪个基站就优先分配信道给用户满足用户的最低速率要求

######### 信道分配的实现
"""
距离用户近的且存在 未分配信道 的基站优先随机分配信道给用户，直到满足用户的最低速率要求，然后分配下一个用户
用户速率初始值为0,的
"""
##UsertoBSList 是一个用户与基站的对应信道的分配表
UsertoBSList = []

# for uid in userID:
#     sumrate = 0
#     while(sumrate<minRate[uid] and BS1touser):
#         rate = channelbandwidth*np.log2(1+0)
#         sumrate += rate


























































