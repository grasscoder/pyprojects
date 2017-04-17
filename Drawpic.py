import matplotlib
### coding=gbk
'''
    Python 科学计算学习：numpy快速处理数据测试
'''

import matplotlib.pyplot as plt  
import numpy as np
from __builtin__ import int
 
if __name__ == '__main__':    
    f = open('E:data.txt', 'r')
    linesList = f.readlines()
#     print(linesList)
    linesList = [line.strip().split(",") for line in linesList]
    f.close()    
    print(linesList)
    #print(linesList)
#     years = [string.atof(x[0]) for x in linesList]
    years = [x[0] for x in linesList]
    print(years)
    price = [x[1] for x in linesList]##不需要强制转化为整形
    print(price)
    plt.plot(years, price, 'b*')#,label=$cos(x^2)$)
    plt.plot(years, price, 'r')
    plt.xlabel("years")
    plt.ylabel("housing average price(*2000 yuan)")
    plt.ylim([300, 700])
    plt.title('line_regression & gradient decrease')
    plt.legend()###显示图示
    plt.show()###显示图像


# plt.figure(figsize=(8,4))
# x = np.linspace(0, 10, 1000)
# y = np.sin(x)
# z = np.cos(x**2)
# plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2)
# plt.plot(x,z,"b--",label="$cos(x^2)$")
# plt.show()

 
# fig = plt.figure()
# ax = fig.add_subplot(111)
# t = ax.scatter(np.random.rand(20), np.random.rand(20))
# fig.show()


# x= [1,2,3]
# y=[4,5,2]
# x2=[1,2,3]
# y2=[10,12,11]
# plt.plot(x,y,label="first line")
# plt.plot(x2,y2,label="senond")
# plt.xlabel("plot num")
# plt.ylabel("variance")
# plt.title("first graph")
# plt.legend()
# plt.show()