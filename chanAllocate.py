# -*-coding:utf-8 -*-
'''
Created on 2017年5月5日

@author: Administrator
'''
# def channelAllocate(BSCover,bsx=BSX+[0],bsy=BSY+[0]):
#     """
#     
#     """
#     BSchanAllocate = [[-1]*channelnum]*TotalNum  ####定义一个信道分配的矩阵，行代表一个基站，列代表基站的信道
#     n = 0##由于list会出现多个相同值(基站范围内不一定总是存在用户)取下标得到第一此出现的值，故循环n,作为全局的控制变量
#     for bs in BSCover:##bs表示当前循环的基站下所有用户的集合bs = [user(0),user(1),user(1),...,user(n)]
#     
#         if len(bs) > 0  and n<=TotalNum : ##判断bs中如果有用户的话,且不是最有一个基站，最后一个基站是宏基站
#             ##初始化计算基站信息的数据
#             if n!=(len(BSCover)-1): 
#                 pt = microAveragePower###微基站的平均信道功率
#                 P = picoPower  ##基站总共功率
#                 radius = 100##m
#             else:
#                 pt = macroAveragePower##宏基站的平均信道功率
#                 P = macroPower
#                 radius = 500##m
#     
#             AvgBand = channelbandwidth##每个信道的平均带宽
# 
#             """第一步：获得当前前基站下：每一个用户与所有信道连接条件下得到的用户速率"""
#             R = []#初始化一个速度矩阵，一行代表当前基站下用户与所有信道的链接所获得速率值列表，列代表信道
#             for user in bs:
#                 d = distance(user[0],user[1],bsx[n],bsy[n])## 用户与当前基站的距离
#                 r = []
#                 for j in xrange(channelnum):
#                     
#                     Interf = interfere(n, j, BSchanAllocate, BSX, BSY)##n表示的是基站，j 是信道，chanlist是信道分配的列表
# #                     sinr = pt*(D[bs.index(user)])**(-4)/(Interf + P*radius**(-4)/alpha)##求sinr
#                     sinr = pt*(d)**(-4)/(Interf + P*radius**(-4)/alpha)##求sinr
#                     rate = AvgBand*log2(1+sinr)
#                     r.append(rate)
#                     ##将得到的速率值r，追加到当前 用户速度一维列表中,
#                     #每一个速率值对应一个信道:R =[r0,r1,r2,..]
#                     
#                 R.append(r)
#             #print len(R)
#             
#             """第二步：进行信道的分配，使用的贪心算法，用户选择(或者说基站分配)当前速率值最大的信道"""
#             for userj in bs:
#                 j = bs.index(userj)##获取当前用户的下标(用户坐标不存在两个相同的)
#                 print "基站编号: %d"%(n)
#                 
#                 Rnow=RateNow(BSchanAllocate, userj, BSX, BSY)##表示用户当下的速率，这样做是有问题的!？？【【【应该从信道分配list中获取当前用户的当前速率，刚开始用户的求得速率值为0】】】 
#                 while(Rnow < Rmin):##用户速率大于最低速率，
#                     if BSchanAllocate[n].count(-1)>0:#当前基站还有未分配的信道，还有一个else，如果当前基站的信道数量不够该如何处理
#                         Rnow += max(R[j])
#                         chanid = R[j].index(max(R[j]))##将当前用户速率值最大值对应的第一个(可能会出现速率并列最大的)信道标号赋值给chanid
#                         BSchanAllocate[n][chanid]=userj##在基站n的信道s对应位置写入用户坐标
#                         print "channelid:%d user:%s"%(chanid,userj)
#                         
#                         for rm in xrange(len(R)):##循环速率矩阵行，将本基站其他用户对应这条信道的速率设置为0
#     #                         row = R.index(rm)#获取行坐标
#                             for rn in xrange(len(R[j])):
#     #                             col = rm.index(rn)##获取列坐标
#                                 if (rn==chanid):R[rm][rn]=0##将已经分配的信道对应其他用户的速率矩阵位置设置为0，表示此信道已经分配不能再分配其他人
#                                   
#                     else: ###如果当前基站的信道已经分配完毕，暂时输出下面的字符串，后续会继续处理这种情况
#                         
#                         print "All channels are busy"
#                         exit(0)
#             print "\n"
#         n = n + 1 ##当前基站的分配完毕，n+1进入下一个基站的额信道分配
#            
#     return BSchanAllocate    