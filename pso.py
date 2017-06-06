# -*-coding:utf-8 -*-
import random  
import copy  
import numpy as np  
import matplotlib.pyplot as plt
from CAPalloction import readFile,classifyUser,getPower,channelAllocate,turnInToParticle,chanNumOfEachUser

#----------------------PSO参数设置---------------------------------  
class PSO(): 
    def __init__(self,pN,dim,max_iter):  
        self.w = 0.8    
        self.c1 = 1.4961#2     
        self.c2 = 1.4961#2     
        self.r1= 0.6  
        self.r2=0.3
        self.channelnum = 64  
        self.pN = pN                #粒子数量  
        self.dim = dim              #搜索维度  
        self.max_iter = max_iter    #迭代次数  
        self.X = np.zeros((self.pN,self.dim))       #所有粒子的位置和速度  
        self.V = np.zeros((self.pN,self.dim))  
        self.pbest = np.zeros((self.pN,self.dim))   #个体经历的最佳位置 
        self.gbest = np.zeros((1,self.dim))         #全局最佳位置 
        self.p_fit = np.zeros(self.pN)              #每个个体的历史最佳适应值  
        self.fit = 1e10             #全局最佳适应值  
        self.filename = ['user.txt','bs.txt']
        self.UserX,self.UserY,self.BSX,self.BSY = readFile(*self.filename)
        self.BSCover = classifyUser(100,self.UserX,self.UserY,self.BSX,self.BSY)
        self.BSchanAllocate=[[-1 for i in xrange(self.channelnum)] for j in xrange(len(self.BSCover))]#初始化信道分配 
#---------------------目标函数Sphere函数-----------------------------  
    def function(self,p):  #p不是列表，是numpy.ndarray,列表是不能进行数值运算的
        '''
        首要解决的问题是 目标函数的的表达式:
        由于粒子由是不同信道的功率等级（比例）表示的,p = array([p1,p2,....,p704]),
        '''
        thissum = 0  
        length = len(p)  
        p = p**2  
        for i in range(length):  
            thissum += p[i]  
        return thissum 

#---------------------初始化种群----------------------------------  
    def init_Population(self): 
        ####将宏基站的坐标加入到基站的坐标列表中
        self.BSX = self.BSX+[0.0]
        self.BSY = self.BSY+[0.0]
        for i in xrange(5):
            self.BSchanAllocate = channelAllocate(self.BSCover,self.BSchanAllocate,self.BSX,self.BSY)
        
        for i in xrange(self.pN):
            self.X[i] = turnInToParticle(getPower(self.BSchanAllocate))#初始化粒子位置
            for j in range(self.dim):
                self.V[i][j] = random.uniform(0,1) #初始化粒子的速度
            self.pbest[i] = self.X[i] ##每个粒子的最佳位置 
            tmp = self.function(self.X[i])#调用目标函数，计算当前粒子的适应值，目标函数是处理每一个粒子的，在这个表达式中显而易见
            self.p_fit[i] = tmp  ##每个粒子最佳适应值
            if(tmp < self.fit):  #判断小于全局最佳适应值，将当前粒子的最佳适应值赋值给全局最佳适应值
                self.fit = tmp   #
                self.gbest = self.X[i]

#---------------------初始化种群----------------------------------
    '''第二种初始化的方案:只有分配的信道才分配功率等级，从代码中控制V[i][j]的初始化，只有对应分配的信道才有速率值，否则没有'''  
    def init_Population2(self): 
        ####将宏基站的坐标加入到基站的坐标列表中
        self.BSX = self.BSX+[0.0]
        self.BSY = self.BSY+[0.0]
        for i in xrange(5):
            self.BSchanAllocate = channelAllocate(self.BSCover,self.BSchanAllocate,self.BSX,self.BSY)
        
        for i in xrange(self.pN):
            self.X[i] = turnInToParticle(getPower(self.BSchanAllocate))#初始化粒子位置
            for j in xrange(self.dim):##以粒子的维度为循环次数
                if self.X[i][j]!=0:##在x[i]不为0的位置，随机初始化一个速度值
                    self.V[i][j] = random.uniform(0,1) #初始化粒子的速度
            self.pbest[i] = self.X[i] ##每个粒子的最佳位置 
            tmp = self.function(self.X[i])#调用目标函数，计算当前粒子的适应值，目标函数是处理每一个粒子的，在这个表达式中显而易见
            self.p_fit[i] = tmp  ##每个粒子最佳适应值
            if(tmp < self.fit):  #判断小于全局最佳适应值，将当前粒子的最佳适应值赋值给全局最佳适应值
                self.fit = tmp   #
                self.gbest = self.X[i]
        flag = True
        if flag:
            print self.X[0][:20]
            print self.V[0][:20]
            flag = False         
                
#--------------------------粒子的惯性权重-----------------------------
    def inertia_Weight(self,t):
        """保证惯性权重开始:0.9全局搜索能力强，最后为0.1:局部搜索能力强"""
        k = (0.9-0.1)/(1-self.max_iter)
        b = (0.9*self.max_iter-0.1)/(self.max_iter-1)
        y = k*t + b
        return y

#----------------------更新粒子位置----------------------------------  
    def iterator(self):  
        fitness = []  
        for t in range(self.max_iter):  
            for i in range(self.pN):         #更新gbest\pbest  
                temp = self.function(self.X[i])  
                if(temp<self.p_fit[i]):      #更新个体最优  
                    self.p_fit[i] = temp  
                    self.pbest[i] = self.X[i]  
                    if(self.p_fit[i] < self.fit):#更新全局最优  
                        self.gbest = self.X[i]  
                        self.fit = self.p_fit[i]
            self.w = self.inertia_Weight(t)##调用类内部的函数,改变w的值，收敛速度明显加快
            for i in range(self.pN):  
                self.V[i] = self.w*self.V[i] + self.c1*self.r1*(self.pbest[i] - self.X[i])+ self.c2*self.r2*(self.gbest - self.X[i])  
                  
                self.X[i] = self.X[i] + self.V[i]  
            fitness.append(self.fit)  
#             print(self.fit)                   #输出最优值  
        return fitness
    
#----------------------------------粒子群类构造结束-------------------------------------------------
    def printXV(self):
        print self.X[0][:20]
        print self.V[0][:20]

if __name__=="__main__":    
    #----------------------程序执行-----------------------
    max_iter = 200  
    my_pso = PSO(pN=15,dim=704,max_iter=max_iter)  
    my_pso.init_Population2()  
    fitness = my_pso.iterator()  
    my_pso.printXV()
    #----------------------画 图--------------------------  
    plt.figure(1)  
    plt.title("Figure1")  
    plt.xlabel("iterators", size=14)  
    plt.ylabel("fitness", size=14)  
    t = np.array([t for t in range(0,max_iter)]) ##200 为max_iter 
    fitness = np.array(fitness)  
    plt.plot(t,fitness, color='b',linewidth=3)  
    plt.show()
















