# -*- coding:utf-8 -*-
#from collections import OrderedDict
string = raw_input()
st = string.strip().split(" ")
L =[int(i) for i in st]
d = dict()
for i in L:
    if i not in d:
        d[i] = L.count(i)
temp = 0
key = 0
d = sorted(d.items())
# print max(d[1])
# print d

for i,val in d:
    if temp<val:
        temp = val
        key = i
            
print key 
