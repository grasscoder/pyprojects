# -*-coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from numpy import pi,sin,cos
from SINR import distance
from cProfile import label

def DrawCircle(radius, xShift = 0, yShift = 0, color='g--'):
    '''
             画一个圆圈，半径为radius，圆心(xShifting，yShifting),圆圈的颜色color,labelname是图例中现实的名称，
    mark是圆心的显示样式,函数最终会画出指定半径和指定样式的圆心和圆圈
    '''
    t = np.linspace(0, 2*pi, 360)
    x = sin(t)*radius + xShift
    y = cos(t)*radius + yShift
#     plt.figure(figsize=(9,8.1))
#     plt.title("BaseStation Coverage")
#     plt.xlabel("x")
#     plt.ylabel("y")
#     plt.legend()
    plt.plot(x,y,color)
    
    #不在这里画圆心,否则图例显示多个相同的图例
    #plt.plot(xShift,yShift,mark,label=labelname)##偏移量(xshift,yshift)表示圆心的位置，用绿点表示圆心

def Distance_points(x,y,value):
    """
    x and y are Lists,judge any of distances  (x[i],y[i]) with (x[j],y[j]) in x,y is bigger than value
    """
    if(len(x)>len(y)):x = x[:len(y)]
    elif len(y)>len(x): y = y[:len(x)]
    
    for i in xrange(len(x)-1):
        for j in xrange(i+1,len(y)):
            if distance(x[i],y[i],x[j],y[j])<value:return False
#             else:print distance(x[i],y[i],x[j],y[j])
    return True

def PicoCircle(range1,range2,num=6):
    ##range1/range2表示的是生成圆的 圆心 所在的范围,小圆半径默认100,PicoBS数量默认6个
    """
    function is used to draw a little circle in the range[range1,range2]
    
    """
    xp = [0]
    yp = [0]
    while(len(xp)<num+1):
        _t = np.random.random()*2*pi-pi
        R = np.random.randint(100,400) #半径随机整数
        _x = R*cos(_t)
        _y = R*sin(_t)
        
        if range1<=np.sqrt(_x**2+_y**2)<=range2:
            xp.append(_x)
            yp.append(_y)
            if not Distance_points(xp, yp, 150):##保证pico基站之间的距离大于150
                xp.pop()
                yp.pop()
#         else:
#             while(not(range1<=np.sqrt(_x**2+_y**2)<=range2)):
#                 _t = np.random.random()*2*pi - pi
#                 R = np.random.randint(100,400)
#                 _x = R*cos(_t)
#                 _y = R*sin(_t)
#     for i in xrange(1,len(x)):
#         DrawCircle(100, x[i], y[i], "g--", BSname+str(i), "k^")
    return xp[1:],yp[1:]    #返回 除宏基站的坐标之外的值 生成的 x,y list 的值

def Relays(xp,yp,num=2):
    """
            中继节点的数量默认为2个，
    """
    range1 = 100 #范围1
    range2 = 400 #范围2
#     xp,yp = PicoCircle(range1, range2)
    xp.insert(0,0)
    yp.insert(0,0)
    l = len(xp)
    while(len(xp)<l+num+1):
        _t = np.random.random()*2*pi-pi
        R = np.random.randint(range1,range2) #半径随机整数
        _x = R*cos(_t)
        _y = R*sin(_t)
        
        if range1<=np.sqrt(_x**2+_y**2)<=range2:
            xp.append(_x)
            yp.append(_y)
            if not Distance_points(xp, yp, 150):##保证pico基站之间的距离大于150
                xp.pop()
                yp.pop()
    return xp[-num:],yp[-num:]
#     print xp,yp
#     print xp[-num:],yp[-num:]
    
    
def RandomNum(num):
    """
            单位圆内生成  num 个随机分布在圆内的随机数的坐标
    """
    ##np.random.random(n)生成n个[0.0,1)之间的随机数
    ##pi*(2*r-1)范围[-pi,pi),保证x,y范围是[-1,1),这样能保证在整个圆内分布，而不是在一个圆心角度范围分布
    t = np.random.random(size=num) * 2 * pi - pi
    
    x = cos(t)  ##保证随机生成的t，求值得到的x,y在单位圆的范围内
    y = sin(t)  
    i_set = np.arange(0,num,1)  #从0-sample_num,步长为1，结果是个列表
     
    for i in i_set:  
        leng = np.sqrt(np.random.random()) #生成0.0-1.0之间的随机数，不能取到1.0，使得随机点出现在圆内，而不是只分布在圆圈上 
        x[i] = x[i] * leng  
        y[i] = y[i] * leng
    return x,y #返回单位圆内的随机点的坐标 list

def Draw(samples_num=60,R=500): #samples_num = 60  ### 样本数量,#R = 500 ##宏基站的大圆的半径
    """
    given sample number,draw these sample points.
    """
    ##要想画在同一张图上，就必须在同一个figure对象之下   
    plt.figure(figsize=(10,10.1),dpi=125,facecolor="#abf2fa") ##创建图表对象 ，figsize参数指定Figure对象(图像)的宽度和高度，其单位为英寸,dpi参数指定Figure对象的分辨率，即每英寸所表示的像素数，这里使用缺省值80
    DrawCircle(R, 0, 0, "k-") #"k^"表示黑色三角圆心，画一个半径500的圆心位于原点的黑色的宏基站圆
    plt.plot(0,0,"g^",label = "MacroBS")##画出宏基站的圆心，图例显示为：MacroBS
    
    x,y = RandomNum(samples_num)
    plt.plot(R*x,R*y,'ro',label='Users')  ### r*图上的圆点，表示的用户分布位置,x,y分别是向量
    
    ##生成Pico基站的圆心坐标
    xp,yp = PicoCircle(100, 400)
    
    for i in xrange(len(xp)):
        DrawCircle(100, xp[i], yp[i])
    plt.plot(xp,yp,"k^",label="PicoBS")
    #生成中继节点
    xR,yR = Relays(xp,yp,num=2)
    for i in xrange(len(xR)):
        DrawCircle(100, xR[i], yR[i])
    plt.plot(xR,yR,"b^",label="Relay")
    
    ax=plt.gca()  
    ax.set_yticks(np.linspace(-500,600,12))  
    ax.set_yticklabels( ('-500', '-400', '-300', '-200', '-100',  '0',  '100',  '200', '300','400','500','600'))
    ax.set_xticks(np.linspace(-500,500,11))  
    ax.set_xticklabels( ('-500', '-400', '-300', '-200', '-100',  '0',  '100',  '200', '300','400','500'))

#     plt.xlim(-R-1,R+1)  ## 图片上x显示的范围
#     plt.ylim(-R-1,R+100)  ## 图片上y的范围
    plt.xlabel('x')  
    plt.ylabel('y')  
    plt.title("BaseStation & User")
    plt.grid(True)  #显示网格线
    plt.savefig('imag.png')  
    plt.legend(loc="upper right",bbox_to_anchor=(1, 1),ncol=1, borderaxespad=0) ##显示图例 
    plt.show()  
    return R*x,R*y #返回宏基站圆的随机坐标

if __name__=="__main__":
    
    Draw()
