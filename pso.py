# -*-coding:utf-8 -*-
import random  
import copy  
import numpy as np  
import matplotlib.pyplot as plt
from CAPalloction import readFile,classifyUser,getPower,channelAllocate,turnInToParticle
  

                  
class Bird(object):##定义一个鸟类（粒子类）
    
    def __init__(self, speed, position, fit, lBestPosition, lBestFit):
        '''
                         初始化的信息：speed粒子的速率，position：粒子的位置，fit适应度，lBestPostion粒子经理的最佳位置，
        lBestFit粒子的最佳是硬度值
        '''
        self.speed = speed
        self.position = position
        self.fit = fit
        self.lBestFit = lBestFit
        self.lBestPosition = lBestPosition

#----------------------PSO参数设置---------------------------------  
class PSO(): 
     
    def __init__(self,pN,dim,max_iter):  
        self.w = 0.8    
        self.c1 = 2     
        self.c2 = 2     
        self.r1= 0.6  
        self.r2=0.3
        self.channelnum = 64  
        self.pN = pN                #粒子数量  
        self.dim = dim              #搜索维度  
        self.max_iter = max_iter    #迭代次数  
        self.X = np.zeros((self.pN,self.dim))       #所有粒子的位置和速度  
        self.V = np.zeros((self.pN,self.dim))  
        self.pbest = np.zeros((self.pN,self.dim))   #个体经历的最佳位置和全局最佳位置  
        self.gbest = np.zeros((1,self.dim))  
        self.p_fit = np.zeros(self.pN)              #每个个体的历史最佳适应值  
        self.fit = 1e10             #全局最佳适应值  
          
#---------------------目标函数Sphere函数-----------------------------  
    def function(self,x):  #x是列表
        '''
        首要解决的问题是 目标函数的的表达式
        '''
        sum = 0  
        length = len(x)  
        x = x**2  
        for i in range(length):  
            sum += x[i]  
        return sum 

#---------------------初始化种群----------------------------------  
    def init_Population(self): 
        filename = ['user.txt','bs.txt']
        UserX,UserY,BSX,BSY = readFile(*filename)
        BSCover = classifyUser(100,UserX,UserY,BSX,BSY)
        BSchanAllocate=[[-1 for i in xrange(self.channelnum)] for j in xrange(len(BSCover))]#初始化信道分配
        ####将宏基站的坐标加入到基站的坐标列表中
        BSX = BSX+[0.0]
        BSY = BSY+[0.0]
        for i in xrange(5):
            BSchanAllocate = channelAllocate(BSCover,BSchanAllocate,BSX,BSY)
        
        for i in xrange(self.pN):
            self.X[i] = turnInToParticle(getPower(BSchanAllocate))#初始化粒子位置
            for j in range(self.dim):
                self.V[i][j] = random.uniform(0,1) 
            self.pbest[i] = self.X[i]  
            tmp = self.function(self.X[i])#目标函数
            self.p_fit[i] = tmp  
            if(tmp < self.fit):  
                self.fit = tmp  
                self.gbest = self.X[i]
                
#         for i in range(self.pN):  
#             for j in range(self.dim):  
#                 self.X[i][j] = random.uniform(0,1)  #初始化种群的位置
#                 self.V[i][j] = random.uniform(0,1)  #初始化种群的速度
#             self.pbest[i] = self.X[i]  
#             tmp = self.function(self.X[i])  
#             self.p_fit[i] = tmp  
#             if(tmp < self.fit):  
#                 self.fit = tmp  
#                 self.gbest = self.X[i]  
#                 
        
      
#----------------------更新粒子位置----------------------------------  
    def iterator(self):  
        fitness = []  
        for t in range(self.max_iter):  
            for i in range(self.pN):         #更新gbest\pbest  
                temp = self.function(self.X[i])  
                if(temp<self.p_fit[i]):      #更新个体最优  
                    self.p_fit[i] = temp  
                    self.pbest[i] = self.X[i]  
                    if(self.p_fit[i] < self.fit):  #更新全局最优  
                        self.gbest = self.X[i]  
                        self.fit = self.p_fit[i]  
            for i in range(self.pN):  
                self.V[i] = self.w*self.V[i] + self.c1*self.r1*(self.pbest[i] - self.X[i])+ self.c2*self.r2*(self.gbest - self.X[i])  
                  
                self.X[i] = self.X[i] + self.V[i]  
            fitness.append(self.fit)  
            print(self.fit)                   #输出最优值  
        return fitness
if __name__=="__main__":    
    #----------------------程序执行-----------------------
    max_iter = 200  
    my_pso = PSO(pN=15,dim=704,max_iter=max_iter)  
    my_pso.init_Population()  
    fitness = my_pso.iterator()  
    
    #----------------------画 图--------------------------  
    plt.figure(1)  
    plt.title("Figure1")  
    plt.xlabel("iterators", size=14)  
    plt.ylabel("fitness", size=14)  
    t = np.array([t for t in range(0,max_iter)]) ##200 为max_iter 
    fitness = np.array(fitness)  
    plt.plot(t,fitness, color='b',linewidth=3)  
    plt.show()
















