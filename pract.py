# -*- coding:utf-8 -*-
# str = raw_input("please inputnumber with space for splite\n")
# list1 = str.split(" ")
# list2 = list()
# print list1
# for i in list1:
#     i = int(i)
#     list2.append(i)
#     
# print (sum(list2))
# str1 = raw_input("")
# list1 = str1.split(" ")
# 
# for i in xrange(len(list1)):
#     list1[i] = int(list1[i])
#    
# print sum(list1)


# inputstr = raw_input()
# list1 = list()
# for strs in inputstr:
#     list1.append(int(strs))
# s =j= 0
# for i in list1:
#     s = s + i*(7**(len(list1)-j-1))
#     if j <= len(list1):
#         j = j + 1              
# 
# print s
def strToNum(numstring):
    #将一个纯数字的字符串转变为数数字list
    list1 = list()
    for chars in numstring:
        list1.append(int(chars))
    return list1
    
def copyArray(arr):
    # 将arr复制到arr1中，不要修改原来的arr，不能直接赋值，会修改原数据，
    arr1 =[num for num in arr]
    arr1.sort()
    return arr1 
       
def find3same(arr):
    # find 3 cards which are the same 
    #return the number of 3same card and the rest of list
    i = 0
    arr1 = copyArray(arr)
    for num in arr1:
        if num!=-1 and arr1.count(num) >= 3:
            i = i + 1
            for j in xrange(3):
                arr1[arr1.index(num)] = -1
    arr1.sort()
    return i,arr1

def findShunZi(arr):
    #find shun zi in arr 
    #return the number of shun zi and the rest of list
    i = 0
    arr1 = copyArray(arr)
    for num in arr1:
        
        if (num!=-1 and (num+1) in arr1) and ((num+2) in arr1):
            i = i + 1
            for j in xrange(3):
                arr1[arr1.index(num+j)]=-1
    arr1.sort()        
    return i,arr1

if __name__ =="__main__":
    # input String which is only including numbers
    inputnum = raw_input()
      
    if len(inputnum) in [2,5,8,11,14]:
        
        # turn the String above into number list
        list1 = strToNum(inputnum) 
              
        if len(list1)==2:
            if(list1[0]==list1[1]): print "yes"
            else:print "no"
              
        elif len(list1)==5:
            #find3same[0]
            if ((find3same(list1)[0]==1) and (find3same(list1)[1][-1]==find3same(list1)[1][-2])) or \
            ((findShunZi(list1)[0]==1)and(findShunZi(list1)[1][-1]==findShunZi(list1)[1][-2])):
                print "yes"
            else: 
                print "no"
                  
        elif len(list1)==8:
              
            if ((findShunZi(list1)[0]+find3same(findShunZi(list1)[1])[0]==2) and (find3same(findShunZi(list1)[1])[1][-1]==find3same(findShunZi(list1)[1])[1][-2])) or \
            ((find3same(list1)[0]+findShunZi(find3same(list1)[1])[0]==2) and (findShunZi(find3same(list1)[1])[1][-1]==findShunZi(find3same(list1)[1])[1][-2])):
                print "yes"
            else: 
                print "no"        
                          
        elif len(list1)==11:
              
            if ((findShunZi(list1)[0]+find3same(findShunZi(list1)[1])[0]==3) and (find3same(findShunZi(list1)[1])[1][-1]==find3same(findShunZi(list1)[1])[1][-2])) or \
            ((find3same(list1)[0]+findShunZi(find3same(list1)[1])[0]==3) and (findShunZi(find3same(list1)[1])[1][-1]==findShunZi(find3same(list1)[1])[1][-2])):
                print "yes"
            else: 
                print "no"    
                                 
        else:
              
            if ((findShunZi(list1)[0]+find3same(findShunZi(list1)[1])[0]==4) and (find3same(findShunZi(list1)[1])[1][-1]==find3same(findShunZi(list1)[1])[1][-2])) or \
            ((find3same(list1)[0]+findShunZi(find3same(list1)[1])[0]==4) and (findShunZi(find3same(list1)[1])[1][-1]==findShunZi(find3same(list1)[1])[1][-2])):
                print "yes"
            else: 
                print "no"   

    else :
        print "please confirm the number the card is in [2,5,8,11,14]"
# A = [1,1,2,2,3,3,9,9]
#   
# a,b = find3same(A)
# print a
# print b
# print A

# a,b = findShunZi(A)
# print a
# print b
# print A





