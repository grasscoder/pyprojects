# def strCount(strs):
#     L = list(strs)
#     T = set(L)
#     return len(T)
# #     
if __name__=="__main__":
    
    num = input()
    i = 0
    
    while(num!=1):
        temp = num % 2
        if temp==1:i=i+1
        num = num/2
    print i+1