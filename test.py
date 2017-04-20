# -*- coding:utf-8 -*-
'''
Created on 2017��4��20��

@author: Administrator
'''
# macropathLoss = 128.1 + 37.6*np.log10(d) 
from math import *
r = (150*10**6/(64.0*log(2)))*log(1 + (20/64.0)*(128.1+37.6*log10(500))/9)
print str(r/8)+" byte/s"









