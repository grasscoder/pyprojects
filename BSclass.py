# -*- coding:utf-8 -*-
'''
Created on 2017年5月1日

@author: Administrator
'''
'''
--------------------------------------------类  分 界  线--------------------------------------------

'''
# class BS(object):
#     """定义一个抽象 基站类"""
#     def __init__(self,channelnum,totalpower,coverage,dtoAlluser):
#         """channelnum信道数量   totalPower基站总功率，Coverage基站覆盖范围半径 ,dtoAlluser基站到各个用户的距离列表
#         #是一个列表，每一列代表:当前基站与用户(用户编号用列表中对应的下标表示)的距离
#         dtoAlluser[i]#表示当前基站到用户i的距离
#         """
#         self.channelnum = channelnum #信道数量
#         self.totalpower = totalpower ##基站总功率
#         self.channelpower = [0]*channelnum ##每条信道的功率初始化为0
#         self.coverage = coverage #基站的覆盖半径
#         self.dtoAlluser = dtoAlluser #基站到所有用户的距离列表
#         self.underCover = [] ##在当前基站覆盖下的用户集合列表
#         
#     def getuser(self):#获取在当前基站下的用户集合
#         """得到当前基站覆盖范围内的用户"""
#         
#         for d in xrange(len(self.dtoAlluser)):##在距离列表中，按其长度做循环
#             if self.dtoAlluser[d] <= self.coverage:##判断距离小于基站覆盖半径
#                 self.underCover.append(d)#把用户编号追加到当前基站的用户列表中去
#         return self.underCover
#     
#     def userintwo(self):
#         """处于两个基站交叉区域的用户"""
#         pass
#     
#     def interence(self):
#         #同一个基站分配信道，所以不存在不同基站的相同信道的干扰。只有噪声
#         inter = 0
#         return inter
#     
#     def userRate(self):
#         #当前基站范围内的用户与当前基站的所有信道的速率
#         R = [[0]]
#         p = self.totalpower/channelnum
#         N = 9.0
#         Interfe = self.interfere()
#         for i in self.underCover:##当前基站的用户数量作为外循环，i表示用户编号
#             r = []
#             for j in xrange(channelnum):#以当前的基站信道数量作为内循环
#                 r.append(p*(self.dtoAlluser[i])**(-4)/(Interfe+N))
#             R.append(r)    
#         return R
#       
#     def chanAllocate(self):
#         '''只为只在当前基站中的用户分配信道，如果出现基站交叉范围共存的用户先不管，依旧按照本基站的原则分配信道'''
#         R = self.userRate()## R每一行代表：一个用户与当前基站所有信道的速率值 
#         for i in self.underCover:##按用户分配信道
#             pass
# 
# class User(object):
#     """定义一个用户类"""
#     def __init__(self):#初始化
#         self.chanNum = 0   ##用户占用的信道数量
#         self.inBScover = [] ##用户所在的基站,如果在多个基站交叉区域，则列表中会出现他所在的所有基站
#         self.chanlist = [] ##用户占用的信道列表，实际上应该是一个矩阵，每一行代表占用的一个基站的信道
#         self.rate = 0
#         self.Rmin = 1200 #kbps
#         