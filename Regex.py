# -*-coding:utf-8 -*-
import re
'''
Created on 2017年6月21日

@author: Administrator
'''
s = "dog cat dog"
#----------------re.match()---------------------
##1.re.match()只匹配字符串的开头部分，可以成功查找到开头的dog
match = re.match(r'dog',s)

#group()方法返回查找到的匹配模式
# print"re.match():"+ match.group(0)

##但要匹配的字符串如果是cat查找失败
match = re.match(r'cat','dog cat dog')
# print match.group(0)

m=re.match("(\w+)\s(\w+)","abcd efgh, chaj")##\s 会被识别为空格符，匹配字符串中的空格符
# print m.group()  

m=re.match(r"(..)+","a1b2c3")##如果一个组匹配多个，那么仅仅返回匹配的最后一个的，下同
print m.group(1)#结果c3
m=re.findall(r"(..)+","a1b2c3")#结果['c3']
print m

#---------------re.search()---------------------
##2.使用re.search()---匹配任意位置,但是当它 查找到一个匹配项时，就会停止继续查找
s1 = s+" cat"
match = re.search(r'cat',s1)
# print"re.search():"+match.group(0)
# print"re.search():"+match.group()#group()默认值为0，返回正则表达式pattern匹配到的字符串，所以输出结果同上
r = re.search(r"[abc^]*","abcf^c")
# print r.group()
#-------------------re.findall()------------------------
#匹配所有的对象，可以非常简单的得到所有匹配的列表
match  = re.findall(r'dog',s)
# print match#返回list对象，没有group()方法












