# -*-coding:utf-8 -*-
import numpy as np

def distance(x,y,baseX=0,baseY=0):
    """求一个点到另一个点的距离"""
    d =  np.sqrt((x-baseX)**2+(y-baseY)**2)
    return d
def UserRate(Bandwidth,Signal,Interfere,Noise=9.0):
    # 香浓公式
    B = Bandwidth
    S = Signal
    N = Noise
    I = Interfere
    C = B*np.log2(1+S/(N+I))
    return C

def macropathLoss(d):
    return 128.1 + 37.6*np.log10(d)

def micropathLoss(d):
    return 145.4+37.5*np.log10(d)

def sinr(a): #channelpower,numPico,userposition):
    """
    宏基站分配某个或者几个信道给一个用户，满足他的最低速率要求，如果                  
    """
    return a

def microSinr():
    pass
    
    








































