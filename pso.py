# -*-coding:utf-8 -*-
import random  
import copy  
import numpy as np  
# import matplotlib.pyplot as plt
from CAPalloction import readFile,classifyUser,getPower,interfere1,RateNow,channelAllocate,turnInToParticle,chanNumOfEachUser,ParticleInToMatrix
from SINR import distance
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
        self.X = np.zeros((self.pN,self.dim))       #所有粒子的位置  
        self.V = np.zeros((self.pN,self.dim))       #素有例子的速度
        self.pbest = np.zeros((self.pN,self.dim))   #个体经历的最佳位置 
        self.gbest = np.zeros((1,self.dim))         #全局最佳位置 
        self.p_fit = np.zeros(self.pN)              #每个个体的历史最佳适应值  
        self.fit = 1e10             #全局最佳适应值  
        self.filename = ['user.txt','bs.txt']
        self.UserX,self.UserY,self.BSX,self.BSY = readFile(*self.filename)##读取文件中的基站坐标不包含宏基站的坐标
        self.BSCover = classifyUser(100,self.UserX,self.UserY,self.BSX,self.BSY)
        self.BSchanAllocate = [[-1 for i in xrange(self.channelnum)] for j in xrange(len(self.BSCover))]#初始化信道分配 
#         self.BSchanAllocation = channelAllocate(self.BSCover,self.BSchanAllocate,self.BSX,self.BSY) #初始化信道分配1
        
#--------------------构造信噪比函数----------------------------------
    '''函数的作用是求信噪比，干扰函数使用CAPalloction导入的Interfere1函数'''
    
    def SINR(self, n, s, k, X):
        """注意此时的功率不是信道分配时的平均功率，而是按照功率等级划分的功率,所以需要传入的参数还有功率等级。"""
        """定义一个求信噪比的函数:基站n将信道s分配给用户k,X表示一个粒子(功率等级的粒子),不是初始化由各个粒子组成的矩阵"""
        '''interfere1(n, s, user, chanlist, bsx, bsy)函数参数'''
        SINRlist = []##定义一个sinr列表，初始化为空，后续会在里面包含每一个用户的SINR值，其长度等于用户数量
        bsx = self.BSX + [0]#将宏基站的坐标加入到基站坐标bsx,bsy中
        bsy = self.BSY + [0]
        XP = np.array(ParticleInToMatrix(X)) #将得到的粒子转为原来的功率等级矩阵(有没有必要转成ndarray有待考虑)
        channelofEacheruser = chanNumOfEachUser(self.BSchanAllocate)##每个用户的信道数量
        for indexi in xrange(len(self.BSchanAllocate)):#对于同一个用户占用多个信道的情况后续处理，暂时当做每个不同信道的用户当做不同的用户，即便是同一个用户
            if self.BSchanAllocate[indexi].count(-1) < 64:##当前基站存在信道分配
                currentBSX = bsx[indexi]#获取当前用户所在的基站的坐标值
                currentBSY = bsy[indexi]
                if indexi!=len(self.BSchanAllocate)-1:
                    P = 1.0
                    L = 100.0
                else:
                    P = 20.0
                    L = 500.0
                for indexj in xrange(len(self.BSchanAllocate[indexi])):
                    p = []
                    sameuser = []
                    if self.BSchanAllocate[indexi][indexj]!=-1:#说明此信道已经分配用户
                        u = self.BSchanAllocate[indexi][indexj]
                        p1 = XP[indexi][indexj]#得到对应信道分配的功率等级
                        inter = interfere1(indexi, indexj, u, self.BSchanAllocate, bsx, bsy)
                        d = distance(u[0],u[1],currentBSX,currentBSY)
                        sinr = P*p1*d**(-4)/(inter+P*(L**(-4)))
        
        
        
        
        

#---------------------目标函数Sphere函数-----------------------------  
    def function(self,x):  #p不是列表，是numpy.ndarray,列表是不能进行数值运算的
        '''
        首要解决的问题是 目标函数的的表达式:
        由于粒子由是不同信道的功率等级（比例）表示的,p = array([p1,p2,....,p704]),
        '''
        thissum = 0  
        length = len(x)  
        x = x**2  
        for i in range(length):  
            thissum += x[i]  
        return thissum 

#----------------------------初始化种群----------------------------------
    def init_Population(self): 
        ####将宏基站的坐标加入到基站的坐标列表中
        self.BSX = self.BSX+[0.0]
        self.BSY = self.BSY+[0.0]
        for i in xrange(5):
            self.BSchanAllocate= channelAllocate(self.BSCover,self.BSchanAllocate,self.BSX,self.BSY)##循环5次的原因是想多次进行信道分配达到一个先对原来分配来说更好的一点的信道分配方案
        
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
        for i in xrange(len(self.X[0])/11):
            print self.X[0][64*i:63+64*i]
        

if __name__=="__main__":    
    #----------------------程序执行-----------------------
    max_iter = 200  
    my_pso = PSO(pN=15,dim=704,max_iter=max_iter)  
    my_pso.init_Population2()  
    fitness = my_pso.iterator()  
    my_pso.printXV()
    #----------------------画 图--------------------------  
#     plt.figure(1)  
#     plt.title("Figure1")  
#     plt.xlabel("iterators", size=14)  
#     plt.ylabel("fitness", size=14)  
#     t = np.array([t for t in range(0,max_iter)]) ##200 为max_iter 
#     fitness = np.array(fitness)  
#     plt.plot(t,fitness, color='b',linewidth=3)  
#     plt.show()
















