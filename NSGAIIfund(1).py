# -*- coding:utf-8 -*-

'''
Created on 2016年1月6日

@author: Graaf.S.Angell
'''
from math import sqrt
import random
#from test.test_inspect import revise
import copy
import math
import multiprocessing
import threading
import time
from NSGA_II import RnWLists


'''
-----------------------------------------------全局变量--------------------------------------------------
'''

#macroNumber = 1 #macro BS数量
#picoNumber = 3  #pico BS数量
#userNumber = 20  # 用户数量  用户编号从0开始
#infofmbs = [64,500,20000]  #macro基站信息[信道数，覆盖范围（米），功率（瓦）]
#infofpbs = [64,100,1000]  #pico基站信息[信道数，覆盖范围（米），功率（瓦）]
#maxchannal = 3   #每个用户可用的最大信道数量
#nmub = 2   #每个用户可连接的最大基站数量
#DM = [[450,400,350,300,250,200,150,100,50],[10,40,70,100,130,160,190,220,250],[20,50,80,110,140,170,200,230,260],[10,40,70,100,130,160,190,220,250]]    #用户与基站之间的距离
#m = 200   #种群个数
#g = 100  #迭代次数
#pm  = 0.05 #变异率


#Qmax = 1000    #功率等级
#B = 150       #信道带宽
#channalNum = 64   #信道数
#Alpha = 10  #接收功率阈值，即接收功率大于等于alpha时传输成功  (????)



'''---------------------------------------------------------------获取距离矩阵----------------------------------------------------------'''


'''

此计算距离函数已经废弃

def culcuDistance(x1, y1,x2,y2):

    计算两点距离的小函数

    d =sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return d
    
'''
'''

此获取DM函数已经废弃 


def getDistanMat (macronum, piconum, usernum):

    获取距离矩阵
    距离矩阵行数为基站，列数为用户

    filnam ='e:\\nsgaii\\m' + str(macronum) + 'p'+str(piconum) + 'u' + str(usernum) + '.txt'    #储存距离矩阵文件的位置
    f = open(filnam, 'r')   #读取文件
    macronum = int(f.readline()) #获取宏基站数
    piconum = int(f.readline()) #获取微微基站数
    usernum = int(f.readline()) #获取用户数
    macroset = [[0,0] for i in range(macronum)]  #储存宏基站坐标
    picoset = [[0,0] for i in range(piconum)]  #储存微微基站坐标
    userset = [[0,0] for i in range(usernum)]  #储存用户坐标
    
    for i in range(macronum):  #获取宏基站坐标
        macroset[i][0] = int(f.readline())
        macroset[i][1] = int(f.readline())

        
        
    for i in range(piconum):  #获取微微基站坐标
        picoset[i][0] = int(f.readline())
        picoset[i][1] = int(f.readline())
        
    BSset = macroset + picoset #宏基站坐标和微微基站坐标合并
    BSnum = macronum+piconum
        
    for i in range(usernum):  #获取用户坐标
        userset[i][0] = int(f.readline())
        userset[i][1] = int(f.readline())
        
    DM = [[0 for i in range(usernum)] for j in range(BSnum)]
    for i in range(BSnum):  #对于每一个基站i
        for j in range(usernum): #对于每一个用户j
            DM[i][j] = culcuDistance(BSset[i][0], BSset[i][1], userset[j][0], userset[j][1])#计算距离，存入DM           
    return DM    
'''

'''--------------------------------------------------------------------基站类----------------------------------------------------------------'''

class BS:  #还需要实现获取可连接用户功能（通过DM距离矩阵）
    '''
    base station  传入参数为基站距离各个用户的的距离
    '''
    def __init__(self,chaNum,coverArea,power,DL):  #信道数，覆盖面积，功率，距离列表
        self.chaNum = chaNum
        self.coverArea = coverArea
        self.power = power
        self.DL = DL   #还是需要存一下距离列表来计算干扰距离
        self.userUnderCover = []  #user under cover在覆盖范围内的用户组
        self.getUser(DL)
    def getUser(self,DL):
        for i in range(len(DL)):   #对于所有用户
            if DL[i] < self.coverArea:  #如果用户距离小于覆盖范围
                self.userUnderCover.append(i)  #那么就把用户编号加入到可连接列表
                
                
                
def SetBS (macronum, piconum, infombs, infopbs, DM):
    '''设置基站信息，输入macro基站数，pico基站数，macro信息，pico信息，距离矩阵'''
    BSList = []
    for i in range(macronum):    #循环macro基站个数次
        m  = BS(infombs[0],infombs[1],infombs[2],DM[len(BSList)])  #建立macr属性的BS对象 根据现有的基站数（len（BSList））来确定该取DM的哪一行
        BSList.append(m)  #加入到基站列表
    for i in range(piconum):  #同上，pico基站个数次
        p  = BS(infopbs[0],infopbs[1],infopbs[2],DM[len(BSList)])
        BSList.append(p)
    
    return BSList

'''----------------------------------------------以上是基站类，用来储存基站信息-------------------------------------------------'''


class User():
    '''
    '''     
    
'''---------------------------------------------------------------个体类--------------------------------------------------------------'''

class Individual:
    '''
    individual  传入参数BS为基站类数组
    '''
    
    def __init__(self, BS, userNum, maxc, Qmax, Alpha, B):
        '''
        传入参数，BS为基站类数组BS[0],BS[1],BS[2]，userNum是用户个数，maxc是每个用户可连接最大信道数，pm变异率
        '''
  
        self.BSNum = len(BS)   #基站数量
        self.BS = BS
        self.maxc = maxc  #用户可连接最大信道数
        self.Qmax = Qmax
        self.power = 0  #总功率
        self.rate = 0  #总速率
        self.userRate = 0 #用户平均速率
        self.rp = 0 # r/p，速率功率比值，一个用来衡量解的优劣性的一个指标
        self.userNum = userNum  #用户数量
        self.userList = [0 for i in range(userNum)]  #用户占用的信道数列表
        self.tump = self.InitialiseGene()  #生成初始化信道分配
        self.genec = self.tump[0]   #个体基因信道分配 
        self.genep = self.tump[1] #个体基因功率系数         
        self.gener = self.tump[2]  #个体每个信道上的速率
        #self.pm = pm
        #self.cd = 0 #拥挤度
        self.Alpha = Alpha  #计算噪声参数
        self.B = B  #带宽
        
        self.rank = 0  #初始支配等级
        self.CrowdingDistance = 0 #拥挤度初始化
        self.SequenceNumber = -1 #当前个体的唯一序号
        self.DominateIndividuals = [] #当前支配的个体序号列表
        self.DominatedNumber = 0 #当前支配该个体的个体数
        
        
    def InitialiseGene(self):  
        '''
        初始化信道分配和功率分配
        
        功率分配的从1开始有点太少了，应该计算出一个最小功率
        '''
        genec = []
        genep = []
        cnum = 0
        for i in range(self.BSNum):  #计算信道总数
            cnum = cnum + self.BS[i].chaNum
        
        p = self.userNum/(cnum*self.BSNum)    #依概率决定是否分配信道，概率为用户数/信道数
        
        for i in range(self.BSNum):  #循环基站个数次
            chan = []   #当前基站的信道分配
            powe = []  #当前基站的功率分配
            wholePower = self.Qmax  #总功率设置为Qmax功率等级
            for j in range (self.BS[i].chaNum):  #循环当前基站信道个数次
                if(random.random() > p)and(len(self.BS[i].userUnderCover)>0):  
                    #如果随机数大于P,并且可选用户列表不为空，则为当前信道分配用户
                    try:
                        user = random.choice(self.BS[i].userUnderCover)
                        '''
                                                                            一个用户可能分配到好几个信道，大于3个也是可能 出现的
                        '''
                        chan.append(user)   #随机在可选用户群中选取一个用户分配给当前信道
                        self.userList[user] += 1   #该用户被分配的信道数+1
                        wp = random.randint(2,int(wholePower/(self.BS[i].chaNum-j)*0.6))-1  #随机生成一个功率值(1到剩余功率的50%+1)
                        #powe.append(random.randint(1,wp)) 
                        powe.append(wp)#将这个功率值分配给这个信道
                        wholePower = wholePower-wp    #可用功率值减少
                    except IndexError:
                        print('user序号')
                        print(user)
                        print('userlist列表')
                        print(self.userList)
                        print('错误，列表溢出，程序终止')
                        exit(0)
                else:
                    chan.append(-1)   #如果不分配信道，设置为-1
                    powe.append(0)   #不用的信道功率设置为0
            
            genec.append(chan)   #当前基站的信道分配加入基因中
            genep.append(powe)  #当前基站的功率分配加入基因中
        
        gener = []  #初始化gener
        for i in range(self.BSNum):
            l = [0 for j in range(self.BS[i].chaNum)]
            gener.append(l)
        
        tump = (genec,genep,gener)
        return(tump)
    
    def AddChannel(self,i):  #这个得改
        '''
        增加用户i的信道分配,i是用户在用户数组中的位置，表示第i个用户
        执行策略1和策略2，策略1算法复杂度较低，只寻找基站有空余信道并且用户i在这个基站覆盖范围下的情况
        ，分配一个空余信道给用户i
        策略2复杂度较高，在没有空余信道情况下才执行，剥夺一个多信道用户的信道，分配给i用户
        策略2也不能保证用户一定能分配到信道 best effort
        '''
        c = self.userList[i]  #获取用户i分配到的信道数
        
        for j in range (self.BSNum):  #策略1，在所有基站搜索是否i处于覆盖范围，并且信道有空余
            if (-1 in self.genec[j]) and (i in self.BS[j].userUnderCover):  
                #如果当前基站有空余信道（值为-1）并且用户在这个基站的覆盖范围
                k = self.genec[j].index(-1)    #就找到空余信道
                self.genec[j][k] = i        #把空余信道分配给用户i
                self.userList[i] += 1        #用户分配的信道数+1
                if self.Qmax<sum(self.genep[j]):
                    self.RevisePower(j)             
                self.genep[j][k] = random.randint(0,int((self.Qmax-sum(self.genep[j]))*0.8))+1  #同时在剩余可用功率中分配给该信道一些功率
                break  #问题解决，跳出循环
        
        if c == self.userList[i]:  #如果之前的循环没有成功分配信道，进入策略2
            #策略2的思想是，将用户根据分配到的信道数多少排序，从分配信道最多的用户调整信道给需要分配信道的用户
            mlist = []     #多信道用户列表
            m = max(self.userList)     #先获取获得信道最大数
            for n in range(m-1):   #m是信道分配数量的最大值，循环m-1次，循环到信道分配数为2为止
                for r in range(self.userNum):  #对于每个用户
                    if self.userList[r] == m:    #如果信道分配数等于m
                        mlist.append(r)    #加入多信道用户列表
                m -= 1    #循环一次之后，寻找信道分配数少1的用户
            mlen = len(mlist)   #可调整用户数量
            for j in range(self.BSNum):   #开始调整信道，对于每个基站
                if i in self.BS[j].userUnderCover:  #如果i用户在这个基站的覆盖范围内
                    for s in range(mlen):    #对于每一个在mlist里的用户
                        if mlist[s] in self.genec[j]:    #如果该用户也在这个基站的信道分配中
                            k = self.genec[j].index(mlist[s])  #定位这个信道的编号
                            self.genec[j][k] = i     #将这个信道转分配给用户i
                            self.userList[mlist[s]] -= 1  #被剥夺信道的用户分配信道数-1
                            self.userList[i] += 1    #用户i的信道数 +1
                            break    #结束本循环
                if c < self.userList[i]:    #如果在当前基站中，用户i获得了信道
                    break    #结束本循环
                        
    def DecChannel(self,i):
        '''
        减少用户i的信道分配
        2017.3.15 策略修改：寻找速率/功率比最低的那个信道删除
        '''
        '''
        for j in range (self.BSNum):  #在所有基站中搜索
            if (i in self.genec[j]):   #如果用户在基站的信道分配列表中
                k = self.genec[j].index(i)  #找到这个用户被分配的第一个信道
                self.genec[j][k] = -1  #信道置空
                self.genep[j][k] = 0  #功率置0
                self.userList[i] -= 1   #该用户分配信道数-1
                break
        '''
        rp = float('inf')
        bf = -1  #基站编号
        sf = -1 #信道编号
        for n in range (self.BSNum):
            for s in range(self.BS[n].chaNum):
                catch = [n,s,i]
                try:
                    if (self.genec[n][s] == i) and (self.gener[n][s]/(self.genep[n][s]*self.BS[n].power)<rp):
                        #如果 信道分配给了用户i，并且信道的速率功率比小于rp，则标记该信道
                        bf = n  #标记这个基站的
                        sf = s  #这个信道
                except ZeroDivisionError:
                    print('出现除以0错误')
                    print(catch)
                    print(self.genec[catch[0]])
                    print(self.genep[catch[0]])
                    exit(0)
        
        self.genec[bf][sf] = -1 #信道置空
        self.genep[bf][sf] = 0 #功率置0
        self.gener [bf][sf] = 0 #速率置为0
        self.userList[i] -= 1 #该用户分配信道数-1
                
                
    def RevisePower(self,i):
        '''
        修复功率，即基站i的总功率不能大于1000
        
        +1那里应该设置个最低功率，1有点太少了
        
        '''
        a = sum(self.genep[i])  #该基站当前功率的总数，应该小于Qmax才对
        if a >= self.Qmax:    #如果a>0，说明功率超过Qmax
            b = (a + len(self.genep[i]))/self.Qmax
            #b是一个比值，表示当前功率比最大功率的比值，加基因长度是为了最终至少每个信道分配1功率
            #事实上应该是len(self.genep[i])*最小功率，这样每个在使用的信道都至少有一个最小功率  
            #2016.6.29修改，用功率等级来控制，功率等级设置较小就行了
            for j in range(len(self.genep[i])):
                if self.genep[i][j] != 0:
                    self.genep[i][j] = int(self.genep[i][j]/b)+1  #就是这里的+1，以后再改吧（应该加最小功率）
        
                     
    def Revise(self):  
        '''
        对个体进行修复,修复的目标是，每个用户至少一个信道（保证一定的带宽），每个用户至多maxc个信道
        每个基站总功率不超过1000
        '''
        self.userList = [0 for i in range(self.userNum)]  #每次修复之前都要重新计算用户占用信道数列表
        for i in range(self.BSNum):  #循环基站数次
            for j in range(self.BS[i].chaNum):  #循环信道数次
                k = self.genec[i][j]   #信道分配给了第K个用户
                if  k != -1:  #如果分配了
                    self.userList[k] += 1  #那么用户k占用的信道数+1
                    
        for i in range(self.BSNum): #先修复一次功率,以免出现溢出
            self.RevisePower(i)
        
        for i in range(self.userNum):   #先修复信道分配
            while(self.userList[i] > self.maxc):  #如果某用户分配了多余maxc条信道，则执行用户信道减少方法
                self.DecChannel(i)
        for i in range (self.userNum):#由于先执行了减少信道，这样增大了空余信道存在的概率，可以提高信道增加的速度
            if self.userList[i] ==0:   #如果某用户没有分配到信道，则执行信道增加方法
                self.AddChannel(i)
                
        for i in range(self.BSNum): #修复功率
            self.RevisePower(i)
        
        self.power = self.CalculateTotalPower()  #计算总功率
        self.rate = self.CalculateTotalRate()  #计算总速率
        self.rp = self.rate/self.power
        
    #def Gsnk(self,s,n,k):
        '''
        计算信道功率增益
        '''
    def CalculateInterfere(self, n, s):
        '''
        计算干扰, 第n个基站的第s个信道收到的干扰
        干扰公式  信道功率*距离^（-4）  加法叠加
        '''
        Interfere = 0  #干扰初始设置为0
        for i in range(self.BSNum):   #对于每个基站
            if (i != n)and(self.genep[i][s] != 0):   #如果不是当前基站n，并且要计算的信道功率不为0（即已经分配）
                k = self.genec[n][s]     #取要计算干扰信道链接的用户K
                Distence = self.BS[i].DL[k]  #计算用户K与要计算干扰的基站的距离
                Interfere = Interfere + self.genep[i][s]/self.Qmax*self.BS[i].power*(Distence**(-4))   #用公式计算干扰，加法叠加
        return(Interfere)
    
    def CalculateRate(self, n, s):
        '''
        计算速率，第n个基站的第s个信道的速率
        速率公式   带宽B*log2（(功率*距离^(-4))/(总功率*覆盖范围^（-4）)/alpha+干扰）
        '''
        channalNum = self.BS[n].chaNum  #获取当前基站信道总数
        Interfere = self.CalculateInterfere(n, s)  #计算干扰
        k = self.genec[n][s]
        Distence = self.BS[n].DL[k] #得到基站到用户的距离
        p = self.genep[n][s]/self.Qmax*self.BS[n].power*(Distence**(-4))   #计算当前信道功率（17.04.18修正为信号强度）
        Noise = self.Qmax*(self.BS[n].coverArea**(-4))/self.Alpha  #计算噪声
        
        Rate = self.B/channalNum*math.log2(1+p/(Noise+Interfere)) #计算速率
        
        self.gener[n][s] = Rate  #把计算好的速率存入gener中
        
        return(Rate)
    def CalculateTotalPower(self):  
        '''
        计算个体的总功率
        '''
        TotalPower = 0
        for i in range(self.BSNum):  #对于每一个基站
            for j in range(self.BS[i].chaNum):  #的每一条信道
                if self.genep[i][j] != 0:     #如果这条信道功率不为0
                    TotalPower = TotalPower + self.genep[i][j]/self.Qmax*self.BS[i].power  #那么就计算功率累加至totalpower
        
        return(TotalPower)
    
    def CalculateTotalRate (self):  
        '''
        计算个体的总速率
        '''
        TotalRate = 0
        for i in range(self.BSNum):  #对于每一个基站
            for j in range(self.BS[i].chaNum):  #的每一条信道
                if self.genec[i][j] != -1:     #如果这条信道不是空置
                    TotalRate = TotalRate + self.CalculateRate(i, j)  #那么就计算功率累加至totalrate
                else:
                    self.gener[i][j] = 0 #空置信道速率为0
                    
        return(TotalRate)
    
    
    def CaculateAll(self):
        '''
        一次计算所有需要计算的数值
        '''
        self.rate = self.CalculateTotalRate()  #算速率
        self.power = self.CalculateTotalPower()  #算功率
        self.userRate = self.rate/self.userNum  #算平均每个用户速率
        self.rp = self.rate/self.power #算速率功率比值

        '''    
    def Mutation(self):  

        个体变异，如果（0,1）随机数p小于变异率，则个体发生变异
        首先随机选择一条子基因，然后在子基因上确定变异的位置
        （其实就是在基因上选择变异位，因为基因有多条，所以称作子基因）
        变异规则：1，如果选择的信道是空信道，随机分配一个可行的用户，随机分配一个可行的功率，然后修复
                          2，如果信道非空，再进行一次判断
                              a，如果随机数p小于变异率/2（其实就是变异条件下的1/2概率，省事）就把信道置空，功率清零
                              b，否则就强行给这个信道随机换一个用户，然后再随机换一个功率

        p = random.random()  #首先生成一个（0,1）之间的随机数
        if p<self.pm:  #如果随机数小于变异率，则执行变异过程
            k = random.randint(0,self.BSNum-1)  #先随机选择子基因
            l = random.randint(0,len(self.genec[k])-1)  #再寻找子基因上的变异位
            if self.genec[k][l] == -1:    #如果信道是空的
                if len(self.BS[k].userUnderCover) != 0:  #可选用户列表不为0才能操作
                    self.genec[k][l] = random.choice(self.BS[k].userUnderCover)  #在可选范围内随机选择一个用户分配给这个信道
                    self.genep[k][l] = random.randint(1,1000-sum(self.genep[k])) #再可选范围内随机分配一个功率
                    self.Revise()  #对基因执行修复
            else:    #如果信道非空
                if p<self.pm/2:   #这是个50%的概率
                    self.genec[k][l] = -1   #信道置空
                    self.genep[k][l] = 0   #功率置0
                    self.Revise()   #修复
                else:    #另外50%
                    self.genec[k][l] = random.choice(self.BS[k].userUnderCover)   #随机找一个可选用户
                    self.genep[k][l] = random.randint(1,1000-sum(self.genep[k])) #随机分配一个可行功率
                    self.Revise()   #修复
        '''
    def MutationOnce(self):  
        '''
        新版变异，变异操作由外部控制，个体自身不携带变异率，通过拥挤度来控制变异
        
        个体变异，如果（0,1）随机数p小于变异率，则个体发生变异
        首先随机选择一条子基因，然后在子基因上确定变异的位置
        （其实就是在基因上选择变异位，因为基因有多条，所以称作子基因）
        变异规则：1，如果选择的信道是空信道，随机分配一个可行的用户，随机分配一个可行的功率，然后修复
                          2，如果信道非空，再进行一次判断
                              a，如果随机数p小于变异率/2（其实就是变异条件下的1/2概率，省事）就把信道置空，功率清零
                              b，否则就强行给这个信道随机换一个用户，然后再随机换一个功率
        '''
        p = random.random()  #首先生成一个（0,1）之间的随机数
        k = random.randint(0,self.BSNum-1)  #先随机选择子基因
        l = random.randint(0,len(self.genec[k])-1)  #再寻找子基因上的变异位
        if self.genec[k][l] == -1:    #如果信道是空的
            if len(self.BS[k].userUnderCover) != 0:  #可选用户列表不为0才能操作
                #print(self.Qmax-sum(self.genep[k]))
                self.genec[k][l] = random.choice(self.BS[k].userUnderCover)  #在可选范围内随机选择一个用户分配给这个信道
                if self.Qmax-sum(self.genep[k])<1:
                    self.RevisePower(k)
                self.genep[k][l] = random.randint(1,self.Qmax-sum(self.genep[k])) #再可选范围内随机分配一个功率

        else:    #如果信道非空
            if p<0.5:   #这是个50%的概率
                self.genec[k][l] = -1   #信道置空
                self.genep[k][l] = 0   #功率置0
            else:    #另外50%
                self.genec[k][l] = random.choice(self.BS[k].userUnderCover)   #随机找一个可选用户
                if self.Qmax - sum(self.genep[k])<1:
                    self.RevisePower(k)
                self.genep[k][l] = random.randint(1,self.Qmax-sum(self.genep[k])) #随机分配一个可行功率
                
    def Mutation(self, n=1):
        '''
        多次变异
        '''
        for i in range(n):
            self.MutationOnce()
    

'''---------------------------------------------以上是individual类-------------------------------------------------'''


'''
def IfDominated(x,y):  #写完了，再想想能否解决相似个体繁殖问题

    判断两个个体是否互相支配，传入参数是两个individual对象

    #print("x的power = %f，y的power = %f"%(x.power, y.power))
    #print("x的rate = %f，y的rate = %f"%(x.rate, y.rate))
    if (x.power<y.power) and (x.rate>=y.rate):
        return 1   #x支配y
    elif (x.power>=y.power) and (x.rate<y.rate):
        return -1    #y支配x
    else :
        return 0   #x，y没有支配关系
'''
    
'''
def Ranking(POPUL):  #未测试

    分层函数，输入种群population，返回当前非支配层ranknd
    双重循环轮流比较，如果某个个体被支配过，则rank值置为-1
    所有rank值为-1的个体均不能进入非支配层
    
    最终把rank值为-1的个体放入unranked，其余进入ranked
    
    支配关系，如果A支配B，B支配C，那么A一定支配C  A.属性>C.属性（传递关系）
    如果A与B无支配关系，B与C无支配关系，那么A与C不一定没有支配关系
    
    由此可得一个原则，对于一个非支配层，新加入的一个个体，只有如下三种情况
    1.被非支配层中的某个或某些个体支配
    2.支配该非支配层中某个或某些个体
    3.不支配该层中任何个体，也不被该层中任何个体支配
    
    既支配该层中某些个体，又被该层中另一些个体支配的个体是不存在的（由于传递关系）

    for indi in POPUL:
        indi.rank = 0  #先把rank值置为0
    m = len(POPUL)
    for i in range(m-1):   #循环m-1次
        if POPUL[i].rank == -1: #如果当前个体已经被支配，则不进行比较，跳过
            continue
        for j in range(i+1,m):  #循环i+1到m次
            flag = IfDominated(POPUL[i], POPUL[j])  #获得比较结果
            if flag == 1:  #如果x支配y
                POPUL[i].rank = 1  #xrank值置为1
                POPUL[j].rank = -1 #yrank值置为-1 表示被支配
            elif flag == -1:  #如果x被y支配
                POPUL[i].rank = -1  #xrank值置为-1 表示被支配
                POPUL[j].rank = 1 #yrank值置为1
                break  #并且直接结束循环，另外，如果比较没有支配关系，则不做任何操作
    ranked = []
    unranked = []
    for indi in POPUL:
        if indi.rank == -1:  #被支配的，加入unranked
            unranked.append(indi)
        else:
            ranked.append(indi) #其他的，加入ranked
    #print("当前非支配层有%d个个体"%len(ranked))
    if len(ranked) == 0:
        print("分层出错")
        for indi in POPUL:
            print(indi.rank)
        exit()
    #print("当前剩余有%d个个体"%len(unranked))
    tump = (ranked, unranked) #返回元组 ranked是非支配层，unranked是剩余的
    return tump
    '''

def Ranking(Population):
    '''
    分层
    '''
    m = len(Population)
    for i in range(m):  #对种群中个体清零操作
        Population[i].SequenceNumber = i
        Population[i].rank = -1
        Population[i].DominateIndividuals = []
        Population[i].DominatedNumber = 0
        
    for i in range(m-1):  #二重循环使每个个体之间都进行比较
        for j in range(i+1, m):
            if (Population[i].rate>=Population[j].rate)and(Population[i].power<Population[j].power):
                #如果个体i支配了个体j
                #Population[i].DominateIndividuals.append(Population[j].SequenceNumber)
                Population[i].DominateIndividuals.append(Population[j])#j加入i的支配列表
                Population[j].DominatedNumber+=1 #j的被支配数+1
            elif(Population[i].rate<=Population[j].rate)and(Population[i].power>Population[j].power):
                #Population[j].DominateIndividuals.append(Population[i].SequenceNumber)
                Population[j].DominateIndividuals.append(Population[i])#i加入j的支配列表
                Population[i].DominatedNumber+=1
                
    count = 0  #计数器
    tire = 0 #层数
    ranked = []
    while count<m:  #循环，直至所有个体均被分层，实质上是每层一次循环
        NewTire = []
        for i in range(m):  #对于每个个体
            if Population[i].DominatedNumber == 0:  #如果支配该个体数目为0 
                Population[i].rank = tire  #分配当前非支配层
                NewTire.append(Population[i])#该个体加入非支配层
                Population[i].DominatedNumber = -1  #变量设置一个无关值
                count +=1  #分配了个体，计数器加1
        for i in range(m): #对于每一个个体
            if (Population[i].rank == tire)and(len(Population[i].DominateIndividuals)>0):  #如果该个体是当前非支配层
                for j in Population[i].DominateIndividuals:  #查找其支配的个体
                    #Population[Population[i].DominateIndividuals[j]].DominatedNumber-=1  #其支配的个体的被支配数减1
                    j.DominatedNumber -=1  #被支配的个体被支配数减1
                    #Population[i].DominateIndividuals[j].DominatedNumber -=1
        tire+=1  #循环结束，层数+1
        ranked.append(NewTire)
    '''
    print('当前种群有%d个个体，当前共有%d层' %(m,len(ranked)))
    z = 0
    for i in range(len(ranked)):
        print('第%d层有%d个个体' %(i,len(ranked[i])))
        z += len(ranked[i])
    print(z)
    input('pause')
    '''
    for i in range(len(ranked)):  #---------------------------------------------------------------------------------------------------极度重要！！！！！
        for j in range(len(ranked[i])):  #-----------------------------------------------------------------2017.04.19终于解决了速度慢的问题  40min--------->40sec
            ranked[i][j].DominateIndividuals = []  #分层结束之后支配个体列表置空，在Crossover时deepcopy支配列表中全部个体导致执行速度变的非常非常非常慢
    return ranked                

    '''
def GetMaxMin(POPUL):

    从种群中获取最大值和最小值，计算拥挤度要用

    maxrate =0  #最大速率，初值为0
    maxpower = 0  #最大功率，初值为0
    minrate = float("inf")  #最小速率，初值为无穷大
    minpower = float("inf") #最小功率，初值为无穷大
    for i in range(len(POPUL)):  #循环整个种群
        if POPUL[i].rate>maxrate:  #如果速率大于最大速率
            maxrate = POPUL[i].rate  #最大速率更新
        if POPUL[i].power>maxpower:  #原理同上
            maxpower = POPUL[i].power  
        if POPUL[i].rate<minrate: #原理同上
            minrate = POPUL[i].rate
        if POPUL[i].power<minpower: #原理同上
            minpower = POPUL[i].power
    mlist = [maxrate,maxpower,minrate,minpower]  #放入一个列表
    return mlist#返回这个最值列表
    '''
    '''
    
def CrowDist(ranked,mlist):

    计算拥挤度函数 Crowing-Distance
    输入参数为需要计算拥挤度的层级，最大最小速率功率

    num = len(ranked)
    for i in range(num):
        ranked[i].cd = 0
    ranked.sort(key = lambda x:x.rate)  #计算速率拥挤度
    ranked[0].cd = float("inf")
    ranked[-1].cd = float("inf")
    for i in range(1,num-2):
        ranked[i].cd = ranked[i].cd +(ranked[i+1].rate-ranked[i-1].rate)/(mlist[0]-mlist[2]+0.0001)
        #两端拥挤度设置为最大，中间的用（前一位值-后一位值）/（种群最大值-种群最小值）
    
    ranked.sort(key = lambda x:x.power)  #计算功率拥挤度
    ranked[0].cd = float("inf")
    ranked[-1].cd = float("inf")
    for i in range(1,num-2):
        ranked[i].cd = ranked[i].cd +(ranked[i+1].power-ranked[i-1].power)/(mlist[1]-mlist[3]+0.0001)
        #两端拥挤度设置为最大，中间的用（前一位值-后一位值）/（种群最大值-种群最小值）    
    
    ranked.sort(key = lambda x:x.cd,reverse = True) #按照拥挤度从小到大排序
    '''

def CaculateCrowdingDistance(ranked):
    '''
    计算拥挤度算子，ranked是分层之后的种群二维数组，每一个list是一层
    '''
    for i in range(len(ranked)):#每层都计算一次
        n = len(ranked[i])  #当前层个数
        for j in range(n):
            ranked[i][j].CrowdingDistance = 0  #先执行清零
        if n >3:  #如果该层个体数量大于3，执行计算拥挤度操作
            MaxRateIndividual = max(ranked[i], key = lambda x:x.rate)
            MinRateIndividual = min(ranked[i], key = lambda x:x.rate)
            MaxPowerIndividual = max(ranked[i], key = lambda x:x.power)
            MinPowerIndividual = min(ranked[i], key = lambda x:x.power)
            
            RateDifference = MaxRateIndividual.rate - MinRateIndividual.rate
            PowerDifferent = MaxPowerIndividual.power - MinPowerIndividual.power
            #获取最大cost和最小cost的差值，获取最大服务器数量和最小服务器数量的差值
            
            if RateDifference !=0:
                ranked[i].sort(key = lambda x : x.rate, reverse = False)
                ranked[i][0].CrowdingDistance+=1
                ranked[i][-1].CrowdingDistance+=1  #两端加1
                for j in range(1,n-1):
                    ranked[i][j].CrowdingDistance += (ranked[i][j+1].rate-ranked[i][j-1].rate)/RateDifference #计算Cost拥挤度
                    
            if PowerDifferent !=0:
                ranked[i].sort(key = lambda x : x.power , reverse = True)
                ranked[i][0].CrowdingDistance+=1
                ranked[i][-1].CrowdingDistance+=1  #两端加1
                for j in range(1,n-1):
                    ranked[i][j].CrowdingDistance += (ranked[i][j-1].power-ranked[i][j+1].power)/PowerDifferent #计算ServiceNumber拥挤度
            
            ranked[i].sort(key = lambda x : x.CrowdingDistance, reverse = True) #距离大的排前面
            
        else:  #如果该行个体数量少于等于3，不需要比较拥挤度了
            ranked[i][0].CrowdingDistance = 1
            ranked[i][-1].CrowdingDistance = 1
            ranked[i].sort(key = lambda x : x.CrowdingDistance, reverse = True)
            
    return ranked

    '''
def Choose(POPUL, m):

    选择函数，选择m数量的个体作为下一代

    NewPOP = []  #初始下一代个体为空
    unranked  = copy.deepcopy(POPUL)
    while len(NewPOP)<m:   #如果下一代个体数量不够
        rank = Ranking(unranked)  #获取非支配层
        ranked = rank[0]
        unranked = rank[1]
        if m-len(NewPOP)>=len(ranked):  #如果剩余空间可以放入整个支配层
            NewPOP = NewPOP + ranked  #直接放入
        else:  #否则
            mlist = GetMaxMin(ranked)  #获取当前非支配层的最大最小值
            CrowDist(ranked, mlist)  #进行拥挤度排序
            #print("拥挤度排序执行完成")
            for i in range(m-len(NewPOP)):  #根据剩余空间大小
                NewPOP.append(ranked[i])  #获取足够多的个体
        #print("当前新种群中有%d个个体"%len(NewPOP))
    return NewPOP   #返回下一代种群
    '''

def Choose(ranked, m):
    '''
    选择函数， 输入分层计算好拥挤度的种群，以及需要选取的个体数量
    '''
    Population = []
    count = 0
    while count<m:
        if len(ranked[0])<=m-count:  #如果ranked第一层数量小于剩余容量
            count += len(ranked[0]) #count数量加当前层个体数
            Population += ranked.pop(0)  #这一层全加进去
            
        else:
            for i in range(m-count): #否则缺多少加多少
                
                Population.append(ranked[0][i])
            count = m #缺多少加多少的结果就是count足够了 
    
    #print('选择之后的种群数量%d' %(len(Population)))
    #input('暂停显示选择结果')
    return Population


def Crossover(x, y, n, P = 0.95):
    '''
    交叉函数,输入两个个体X,Y，执行交叉，返回clist是两个子代个体
    对每个子基因执行单点交叉，全部执行完毕之后修复个体
    默认交叉率为0.95
    '''
    Timer = 0
    Begin = time.clock()
    xc = copy.deepcopy(x)  # 深拷贝父代个体x
    yc = copy.deepcopy(y) #深拷贝父代个体y

    if random.random()<=0.95:  #如果满足交叉率条件
        
        t = x.BSNum  #获取子基因个数
        for i in range(t):   #循环子基因个数次，每个基因进行交叉
            l = len(x.genec[i])  #获取当前子基因长度
            
            r = random.randint(1,l-1)  #获取一个随机数，即交叉点
            for j in range(r,l-1):  #交叉点后的进行交叉
                xc.genec[i][j] = y.genec[i][j]  #交叉信道
                xc.genep[i][j] = y.genep[i][j]  #交叉功率
                yc.genec[i][j] = x.genec[i][j]  #同上
                yc.genep[i][j] = x.genep[i][j]  #同上
        
        
        xc.Revise()  #修复
        yc.Revise()   
    End = time.clock()
    Timer = End-Begin
        
    clist = [x,y,xc,yc,Timer]   #两个新生个体
    return clist   #返回


def Crossover2(x, y, n, p = 0.95):
    '''
    重写的交叉函数，可以多点交叉
    
    交叉函数,输入两个个体X,Y，执行交叉，返回clist是两个子代个体
    对每个子基因执行单点交叉，全部执行完毕之后修复个体
    '''
    xc = copy.deepcopy(x)  # 深拷贝父代个体x
    yc = copy.deepcopy(y) #深拷贝父代个体y
    if random.random()<=0.95:
        t = x.BSNum  #获取子基因个数
        l = len(x.genec[0])  #获取当前子基因长度
        for i in range(t):   #循环子基因个数次，每个基因进行交叉
            List = [k for k in range(l)]  #基因位置编号
            slice = random.sample(List, n) #随机选取n个
            flag = 0
            for j in range(l):  #循环子基因个数次            
                if j in slice:    #如果i在选择的序列中
                    flag = 0 if flag == 1 else 1  #改变交叉标志
                if flag == 1:   #交叉标志是1的话
                    temp = xc.genec[i][j]
                    xc.genec[i][j] = yc.genec[i][j]
                    yc.genec[i][j] = temp
                    
                    temp = xc.genep[i][j]
                    xc.genep[i][j] = yc.genep[i][j]
                    yc.genep[i][j] = temp
        xc.Revise()
        yc.Revise()
    clist = [x,y,xc,yc]   #两个新生个体
    return clist   #返回
    '''
def nsgaii(m,BSList,g, userNumber, maxchannal = 3,  Qmax = 1000, Alpha = 10, B = 150):

    遗传算法, m个个体，迭代g次

    
    POPUL = []   
    for i in range (m):  #产生m个个体形成种群
        indi = Individual(BSList, userNumber,maxchannal, Qmax, Alpha, B)
        #    def __init__(self, BS, userNum, maxc, Qmax, Alpha, B):
        indi.CalculateTotalRate  #计算一下速率，为gener赋值
        indi.Revise()
        indi.rate = indi.CalculateTotalRate()
        indi.userRate = indi.rate/indi.userNum
        indi.power = indi.CalculateTotalPower()
        POPUL.append(indi)
    
    for i in range(g):  #开始迭代
        NewPopulation = []
        #print("开始第%d次迭代"%(i+1))
        for j in range(int(m/2)):
            k = random.randint(0, len(POPUL)-1)
            X = POPUL.pop(k)
            k = random.randint(0, len(POPUL)-1)
            Y = POPUL.pop(k)   #随机选择XY交叉
            n = random.randint(1, int(len(X.genec[0])/10))#交叉次数为基因长度除以10，随机
            Children = Crossover2(X, Y, n) #其中包括父代两个个体和子代两个个体一共四个[X, Y, X2, Y2]
            if random.random()>=Children[0].CrowdingDistance/2:  #依照拥挤度概率变异
                Children[0].Mutation(int(len(X.LinkUse)/20))
            if random.random()>=Children[1].CrowdingDistance/2:
                Children[1].Mutation(int(len(X.LinkUse)/20))
            
            NewPopulation += Children #加进去
            #son = Crossover(POPUL[j], POPUL[j+1]) #产生子代、
            #POPUL.append(son[0]) #子代加入种群            
            #POPUL.append(son[1])
            
        #print("第%d次迭代结束"%(i+1))    
        POPUL = Choose(POPUL, m)  #对种群进行选择
        #print('userList为')
        #print(POPUL[-1].userList)
        
    return POPUL
    '''

def NsgaiiConvergence(m,BSList,g, userNumber, savepath, step , flag = 0, maxchannal = 3, Qmax = 2000, Alpha = 10, B = 150):
    '''
    用来保留个体解情况的函数，每隔一定step步长保留一组值，观察收敛情况
    遗传算法, m个个体，迭代g次  uerNumber用户数量，savepath保存结果位置， step步长，每隔多长保留一次结果
    '''
    TimerRevise = 0
    TimerCrossover = 0
    TimerCrossoverRevise = 0
    TimerMutation = 0  
    TimerRanking = 0  #四个计时器，修复计时器，交叉计时器，变异计时器，分层计时器
    CrossoverTimes = 0
    
    POPUL = []   
    RateValues = []
    PowerValues = []
    print('清空原有数据')
    RnWLists.clearTxt(savepath)
    for i in range (m):  #产生m个个体形成种群

        indi = Individual(BSList, userNumber,maxchannal, Qmax, Alpha, B)
        #    def __init__(self, BS, userNum, maxc, Qmax, Alpha, B):
        indi.CalculateTotalRate  #计算一下速率，为gener赋值
        indi.Revise()
        indi.CaculateAll()
        
        RateValues.append(indi.rate)  #储存值
        PowerValues.append(-indi.power)
        POPUL.append(indi)
    
    if flag == 0:
        Convergence = [RateValues, PowerValues]
        print('写入初始种群')
        RnWLists.writeTxt(savepath, Convergence, 1) #写入
    
    GeneLength = len(POPUL[0].genec[0])  #获取单条基因长度
    ranked = Ranking(POPUL)  #分层
    Newpopulation = CaculateCrowdingDistance(ranked) #计算初始拥挤度
    
    for iter in range(g):  #开始迭代
        
        print("开始第%d次迭代"%(iter+1))
        Newpopulation = []
        for j in range(int(m/2)):
            k = random.randint(0, len(POPUL)-1)
            X = POPUL.pop(k)
            #print('选取个体X')
            k = random.randint(0, len(POPUL)-1)
            Y = POPUL.pop(k)   #随机选择XY交叉
            #print('选取个体Y')       
            n = random.randint(1, int(GeneLength/30))#交叉次数为基因长度除以10,取整
            #print('第%d次交叉' %(j))
            
            Begin = time.clock()
            Children = Crossover(X, Y, n) #其中包括父代两个个体和子代两个个体一共四个(x,y,xc,yc)
            End = time.clock()
            TimerCrossoverRevise += Children[4]
            Children.pop()
            CrossoverTimes +=1
            TimerCrossover += End-Begin   #交叉计时
            
            if random.random()<=(1-Children[0].CrowdingDistance/2)/17:  #依照拥挤度概率变异
                
                Begin = time.clock()
                Children[0].Mutation(int(GeneLength/30))
                End = time.clock()
                TimerMutation += End-Begin  #变异计时
                #print('个体X变异') 
                
                Begin = time.clock()
                Children[0].Revise
                End = time.clock()
                TimerRevise += End-Begin  #修复计时
                #print('个体X修复') 
                
            if random.random()<=(1-Children[1].CrowdingDistance/2)/17:
                
                Begin = time.clock()
                Children[1].Mutation(int(GeneLength/30))  #对父代变异，因为子代拥挤度值无效
                End = time.clock()
                TimerMutation += End-Begin  #变异计时
                #print('个体Y变异') 
                
                Begin = time.clock()
                Children[1].Revise
                End = time.clock()
                TimerRevise += End-Begin  #修复计时
                #print('个体修复') 
                
            Newpopulation += Children
            #print('新种群加入四个个体') 
        
        
        
        print("第%d次迭代结束"%(iter+1))
        #print('开始分层操作') 
        Begin = time.clock()
        ranked = Ranking(Newpopulation)  #分层
        #print('分层操作结束') 
        Newpopulation = CaculateCrowdingDistance(ranked) #计算拥挤度
        #print('计算拥挤度结束') 
        POPUL = Choose(Newpopulation, m)  #对种群进行选择
        #print('选择操作结束') 
        End = time.clock()
        TimerRanking += End-Begin  #分层计时
        
        
        if flag == 0 and (iter+1)%step == 0:
            RateValues = []
            PowerValues = [] 
            for k in range(m):
                RateValues.append(POPUL[k].rate)
                PowerValues.append(-POPUL[k].power)
            Convergence = [RateValues, PowerValues]
            print('间隔%d次迭代写入，这是第%d次' %(step, int(iter+1)/step))
            RnWLists.writeTxt(savepath, Convergence, 1) #写入
        #print('userList为')
        #print(POPUL[-1].userList)
    
    
    TimerRevise = int(TimerRevise)
    TimerCrossover = int(TimerCrossover)
    TimerMutation = int(TimerMutation)
    TimerRanking = int(TimerRanking)
    TimerCrossoverRevise = int(TimerCrossoverRevise)
    print('修复用时%d分%d秒' %(int(TimerRevise/60), TimerRevise%60))
    print('交叉用时%d分%d秒,执行%d次' %(int(TimerCrossover/60), TimerCrossover%60, CrossoverTimes))
    print('交叉修复用时%d分%d秒' %(int(TimerCrossoverRevise/60), TimerCrossoverRevise%60))
    print('变异用时%d分%d秒' %(int(TimerMutation/60), TimerMutation%60))
    print('分层用时%d分%d秒' %(int(TimerRanking/60), TimerRanking%60))
    
    return POPUL
    '''
class IterationThread(threading.Thread):

    多线程执行迭代用的------------------------------------------多线程不能并行，所以作废了，改用多进程

    def __init__(self, SubPopulation):
        threading.Thread.__init__(self)
        self.SubPopulation = SubPopulation
        self.GeneLength = len(SubPopulation[0].genec[0])
        self.NewSubPopulation = []
        
    def run(self):
        for j in range(int(len(self.SubPopulation)/2)):
            k = random.randint(0, len(self.SubPopulation)-1)
            X = self.SubPopulation.pop(k)
            #print('选取个体X')
            k = random.randint(0, len(self.SubPopulation)-1)
            Y = self.SubPopulation.pop(k)   #随机选择XY交叉
            #print('选取个体Y')       
            n = random.randint(1, int(self.GeneLength/30))#交叉次数为基因长度除以10,取整
            #print('第%d次交叉' %(j))
            Children = Crossover2(X, Y, n) #其中包括父代两个个体和子代两个个体一共四个[x,y,xc,yc]
            
            if random.random()<=(1-Children[0].CrowdingDistance/2)/17:  #依照拥挤度概率变异
                Children[0].Mutation(int(self.GeneLength/30))
                #print('个体X变异') 
                Children[0].Revise
                #print('个体X修复') 
            if random.random()<=(1-Children[1].CrowdingDistance/2)/17:
                Children[1].Mutation(int(self.GeneLength/30))  #对父代变异，因为子代拥挤度值无效
                #print('个体Y变异') 
                Children[1].Revise
                #print('个体修复') 
            self.NewSubPopulation += Children
            #print('新种群加入四个个体') 
    '''            


def RunSubPopulation(SubPopulation):
    '''
    为了多进程执行写的函数
    '''
    GeneLength = len(SubPopulation[0].genec[0])
    NewSubPopulation = []
    for j in range(int(len(SubPopulation)/2)):
        k = random.randint(0, len(SubPopulation)-1)
        X = SubPopulation.pop(k)
        k = random.randint(0, len(SubPopulation)-1)
        Y = SubPopulation.pop(k)   #随机选择XY交叉 
        #n = 1
        n = random.randint(1, int(GeneLength/30))#交叉次数为基因长度除以10,取整
        Children = Crossover2(X, Y, n) #其中包括父代两个个体和子代两个个体一共四个[x,y,xc,yc]
        
        if random.random()<=(1-Children[0].CrowdingDistance/2)/17:  #依照拥挤度概率变异
            Children[0].Mutation(int(GeneLength/30))
            Children[0].Revise
        if random.random()<=(1-Children[1].CrowdingDistance/2)/17:
            Children[1].Mutation(int(GeneLength/30))  #对父代变异，因为子代拥挤度值无效
            Children[1].Revise
        NewSubPopulation += Children
    return NewSubPopulation


def NsgaiiConvergenceMultiProcessing(m,BSList,g, userNumber, savepath, step , flag = 0, ProcessNumber = 3, maxchannal = 3, Qmax = 2000, Alpha = 10, B = 150):
    '''
    用来保留个体解情况的函数，每隔一定step步长保留一组值，观察收敛情况
    遗传算法, m个个体，迭代g次  uerNumber用户数量，savepath保存结果位置， step步长，每隔多长保留一次结果
    '''
    
    POPUL = []   
    RateValues = []
    PowerValues = []
    if m%ProcessNumber != 0:
        print("错误，种群数量(m)不能被线程数(ProcessNumber)整除，退出")
        exit(0)
    SubPopulationLength = int(m/ProcessNumber)
    if flag == 0:
        print('清空原有数据')
        RnWLists.clearTxt(savepath)
    for i in range (m):  #产生m个个体形成种群

        indi = Individual(BSList, userNumber,maxchannal, Qmax, Alpha, B)
        #    def __init__(self, BS, userNum, maxc, Qmax, Alpha, B):
        indi.CalculateTotalRate  #计算一下速率，为gener赋值
        indi.Revise()
        indi.CaculateAll()
        
        RateValues.append(indi.rate)  #储存值
        PowerValues.append(-indi.power)
        POPUL.append(indi)
    
    if flag == 0:
        Convergence = [RateValues, PowerValues]
        print('写入初始种群')
        RnWLists.writeTxt(savepath, Convergence, 1) #写入
    
    GeneLength = len(POPUL[0].genec[0])  #获取单条基因长度
    ranked = Ranking(POPUL)  #分层
    Newpopulation = CaculateCrowdingDistance(ranked) #计算初始拥挤度

    pool = multiprocessing.Pool(ProcessNumber)
    
    for iter in range(g):  #开始迭代
        
        print("开始第%d次迭代"%(iter+1))
        Newpopulation = []
        SubPopulations = []  #储存子种群
        Threads = []
        
        for i in range(ProcessNumber):
            a = []
            SubPopulations.append(a) #创建空链表储存个体
            
        for i in range(int(m/ProcessNumber)):  #分子种群，用来多线程处理
            for j in range(ProcessNumber):
                SubPopulations[j].append(POPUL[i*ProcessNumber+j]) #其实就是把整个种群轮流放入几个子种群
        
        '''
        for i in range(ProcessNumber): #创建线程
            a = IterationThread(SubPopulations[i])
            Threads.append(a)
        '''

        SubPopulations = pool.map(RunSubPopulation,SubPopulations) #在进程池中运行多个进程并行计算

        
        '''
        for i in range(ProcessNumber):  #线程开始
            Threads[i].start()
            print("Thread %d is beginning" %(i))
            
        for i in range(ProcessNumber):  #等待子线程结束
            Threads[i].join()
            print("Thread %d is finish" %(i))

        for i in range(ProcessNumber): #合并
            Newpopulation += Threads[i].NewSubPopulation
        '''       
        for i in range(ProcessNumber): #合并
            Newpopulation += SubPopulations[i]
            
            
        countNum = int(len(Newpopulation)/2)
        if countNum != m:
            print("种群数量不正常，多进程出现错误")
        print("第%d次迭代结束, 种群数量为%d" %(iter+1, countNum))
        #print('开始分层操作') 
        ranked = Ranking(Newpopulation)  #分层
        #print('分层操作结束') 
        Newpopulation = CaculateCrowdingDistance(ranked) #计算拥挤度
        #print('计算拥挤度结束') 
        POPUL = Choose(Newpopulation, m)  #对种群进行选择
        #print('选择操作结束') 
        
        if flag == 0 and (iter+1)%step == 0:
            RateValues = []
            PowerValues = [] 
            for k in range(m):
                RateValues.append(POPUL[k].rate)
                PowerValues.append(-POPUL[k].power)
            Convergence = [RateValues, PowerValues]
            print('间隔%d次迭代写入，这是第%d次' %(step, int(iter+1)/step))
            RnWLists.writeTxt(savepath, Convergence, 1) #写入
        #print('userList为')
        #print(POPUL[-1].userList)
        
    return POPUL

'''---------------------------------------------测试运行-------------------------------------------------'''

'''

macroNumber = 1
picoNumber = 3
userNumber = 20
    
DM = getDistanMat (macroNumber,picoNumber,userNumber)
BSList = SetBS(macroNumber, picoNumber, infofmbs, infofpbs, DM)
print("执行初始化")
POPUL = nsgaii(m,BSList,g)
print("执行完成")
        
'''