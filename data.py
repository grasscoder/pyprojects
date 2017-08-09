# -*-coding:utf-8 -*-
from CRC16 import CRC16
'''
Created on 2017年8月3日

@author: Administrator
'''
class UnpackFrame(object):
    '''
    定义报文类，报文属性包括报文字符和报文长度，需要做的是筛选正确的报文，即从数据包的中筛选出以7F开头的所有报文，
    报文满足CRC16校验
    '''
    def __init__(self,testBuffer):
        self.testBuffer = testBuffer #初始化赋值
#         self.dataLenth = lenofRead #报文长度
        self.crclist  = []##需要校验的各个域以16进制的形式添加到次列表中
    def Startwith7F(self):#7F过滤器
        '''将报文以7F为分界点断开字符串,得到列表'''
        strlist = self.testBuffer.upper().replace(" ","").replace("7F"," 7F").strip().split(' ')#以空格拆分字符串
#         print strlist
        return strlist
    
    def lenFilter(self): # 字符串长度过滤器
        '''7F 1F D5 E7 102311957111006008001000091900697111006008501201 15 B8 C0FF 4FB1'''
        '''7F1FD5E710231195711100600800100009190069711100600850120115B8C0FF4FB1'''
        datalist = self.Startwith7F()
        newdatalist = []
        for data in datalist:#处理以7F开头的报文
#             self.frame  = [0x7f]##需要校验的各个域以16进制的形式添加到次列表中
            try:
                if int(data[2:4],16)&0x80==1:#判断当前报文的长度域LEN是否可扩展，1可扩展0不可扩展，16表示16进制
                    datalen = int(data[2:4],16)+int(data[4:6],16)
#                     self.frame.append(int(data[2:4],16))
#                     self.frame.append(int(data[4:6],16))
                else:
                    datalen = int(data[2:4],16)#不可扩展情况直接等于第一个字节的值
#                     self.frame.append(int(data[2:4],16))
            except IndexError,e:# 下标越界异常
                print e+"下标越界溢出,未获得有效报文"#处理方式
                continue#跳出本次循环，进入下一循环
            
            ##下面开始按照上面的得到的datalen的值进行长度搜索,满足长度搜索的报文添加到newlist中，等待进入下一步CRC过滤
            try:
                #包括7F在内，总共获取总长度为(datalen+1)*2的长度的字符串，后面跟着的两个字节就是校验位;
                #如果获取长度报错，也就是当前字符串没有那么长，就说明这个报文应该被抛弃
                #再者只需要从data的最后取出长度为4的字符串（也就是两个字节的长度，因为FCS的固定长度为2字节也就是四个字符串），判断剩下的长度是不是等于len域的值即可
                da = data[-4:]#获取最后四个字符串,即校验码，格式是字符串类型，需要手动转为16进制使用int()函数
                
                #下面要做的是判断LEN域的值是否都等于除了[LEN:Data域]长度
#                 _da = data[:]
                if len(data[2:len(data)-4])/2 == datalen: 
#                     print  len(data[2:len(data)-4])/2 == datalen 
                    newdatalist.append(data)#符合要求的data添加到新的列表中，便于后续CRC校验筛选
                else:
                    print"当前帧因长度不符合要求因此被抛弃"
            except IndexError,i:
                print i+"下标越界溢出"
                
            ###准备生成CRC校验的列表，现在列表中只包含Head域和LEN域，而且需要确定当前在列表中的两个域中长度，以便于后续的字符串按两位截取
#             for i in xrange(0,len(data),2):#两个字母一组拆分，注意转为16进制
            
            try:
                #每一个经过上面两层筛选的字符串都会产生一个frame列表，也就是CRC数组
                crclist=[int(data[i]+data[i+1],16) for i in xrange(0,len(data)-1,2)]
                #最后两个字节作为校验码,校验的区域为head到数据域，校验位置不算
                crclist = crclist[:-2] 
            except ValueError,v:
                print v+"出现非十六进制范围内的字符"
            
            self.crclist.append(crclist)
        return newdatalist,self.crclist #newdatalist与self.frame的值一一对应
                
    def CRC_16(self):#获取校验码的字符串类型判断与帧校验位的四个字符是否相等
        #allLegealframe包括上面两部所有筛选通过的字符串对应解析的CRC列表
        _,allcrclist = self.lenFilter()#调用上面的函数，获取返回值
        frame = []
        test = CRC16()#实例化一个对象
        for i in xrange(len(allcrclist)):
            fcs = hex(test.createcrc(allcrclist[i]))[2:].upper()#得到校验字符串,str类型
            if _[i][-4:]==fcs:#判断字符串是否相等
                frame.append(_[i])
        return frame


if __name__=="__main__":
    test = CRC16()
    s = "7F 1F D5 E7 102311957111006008001000091900697111006008501201 15 B8 C0FF 4FB1"

#     s = "7F1FD5E710231195711100600800100009190069711100600850120115B8C0FF4F"
    data = "7F1FD5E710231195711100600800100009190069711100600850120115B8C0FF4FB1"
    uf = UnpackFrame(data)
    print uf.CRC_16()
    
    """这个能处理正确报文从中间阶段分散在两个帧中的情况，策略是：以空格拆分字符串时，保留最后一个不符合要求的但是头上带7F的字符串，与后面 获取的字符串拼接。
    根据ctr1 b6后续帧标识判断是否有后续帧"""
    