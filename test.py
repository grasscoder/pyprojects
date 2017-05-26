# -*- coding:utf-8 -*-
from math import *
'''
Created on 2017��4��20��

@author: Administrator
'''
# macropathLoss = 128.1 + 37.6*np.log10(d) 

r = (150*10**6/(64.0*log(2)))*log(1 + (20/64.0)*(128.1+37.6*log10(10))/9)
print str(r/8)+" byte/s"



# -*- coding:utf-8 -*-
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    # 返回构造的TreeNode根节点
      
    #def reConstructBinaryTree(self, pre, tin):
        # write code here
        #if len(pre)==0:return None
        #elif len(pre)==1;return TreeNode(pre[0])
        #else:
            # gen = TreeNode(pre[0])
            #t = tin.index(pre[0])#t指向根的下标
            #gen.left =  reConstructBinaryTree(self,pre[1:1+len(tin[:tin.index(pre[0])])],tin[:tin.index(pre[0])])
            #gen.right = reConstructBinaryTree(self,pre[1+len(tin[:tin.index(pre[0])]):],tin[tin.index(pre[0])+1:])
            
            #  gen.left = self.reConstructBinaryTree(pre[1:tin.index(pre[0])+1],tin[:tin.index(pre[0])])            
            #   gen.right = self.reConstructBinaryTree(pre[tin.index(pre[0])+1:],tin[tin.index(pre[0])+1:] )
        #return gen
        
#     def reConstructBinaryTree(self, pre, tin):
#         # write code here
#         if len(pre) == 0:
#             return None
#         if len(pre) == 1:
#             return TreeNode(pre[0])
#         else:
#             flag = TreeNode(pre[0])
#             flag.left = self.reConstructBinaryTree(pre[1:tin.index(pre[0])+1],tin[:tin.index(pre[0])])
#             flag.right = self.reConstructBinaryTree(pre[tin.index(pre[0])+1:],tin[tin.index(pre[0])+1:] )
#         return flag