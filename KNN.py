# -*- coding:utf-8 -*-
from numpy import *
import operator

#加载数据的方法，返回样本数据(每一行是一个样本)和样本标签
def createDataSet():
    group = array([[90,100],[88,90],[85,95],[10,20],[30,40],[50,30]])#样点数据
    labels =["A","A","A","D","D","D"]
    return group,labels
#分类方法，传入数据集需是array
def classify0(inX,dataSet,labels,k):#inX 为输入样本
    dataSetSize = dataSet.shape[0] ##输入数据矩阵的行数
    diffMat = tile(inX,(dataSetSize,1))-dataSet #求矩阵差
    sqDiffmat  =diffMat**2 
    sqDistance = sqDiffmat.sum(axis = 1)#求平方和
    distance = sqDistance**0.5 #
    sortedDistance = distance.argsort()
    
    classCount = {}
    for i in xrange(k):
        voteLabel = labels[sortedDistance[i]]
        classCount[voteLabel] = classCount.get(voteLabel,0) + 1
        sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse = True)
        return sortedClassCount[0][0]

