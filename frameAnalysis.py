# -*-coding:utf-8 -*-
from data import UnpackFrame

class FrameAnnalysis(object):
    '''定义协议解析帧，解析报文中的每一个域的信息，只获取对应域的字节长度，不涉及获取域内信息'''
    def __init__(self, usefulframe):
        '''构造函数 usefulframe 是域解析中得到的报文(帧),这个变量是一个字符串类型'''
        '''7F1FD5E710231195711100600800100009190069711100600850120115B8C0FF4FB1'''
        headlen = 1
        mamlen = 1
        serlen = 1
        fcslen = 2
        self.usefulframe =  usefulframe##将需要解析的帧赋值给对象的属性进行初始化
        self.framelen = 0 ##表示整帧长度
#         self.field = []##全局列表变量解析之后的报文，是以列表的形式存放在这个self.field中
        self.field = {"HEAD":'',"LEN":'',"CTR":'',"MAM":'',"ADDR":'',"SER":'',"DI":'',"DATA":'',"FCS":''}

    def getFramelen(self):#当前报文的长度
        self.framelen,_ = self.LEN()
        return int(self.framelen,16)##当前实例化帧的长度的10进制整形值
        
    def HEAD(self):
        leftframehead = self.usefulframe[2:]##去掉头部的7F标记,剩下的字符串中继续进行解析
        self.field["HEAD"] = "7F"
        return leftframehead # 返回'1FD5E710231195711100600800100009190069711100600850120115B8C0FF4FB1'
        
    def LEN(self):
        '''1FD5E710231195711100600800100009190069711100600850120115B8C0FF4FB1'''
        '''先通过堆LEN域LEN0字节的解析，才能去判断是否有LEN1字节的存在'''
#         self.leftframe = self.usefulframe[2:]
        leftframelen = self.HEAD()#以HEAD返回值为操作变量进行后续操作
        len0 = leftframelen[:2]#获取剩余字符串的LEN0域，通过LEN0域获解析以便得到是否存在LEN1字节
        if int(len0,16)&0x80==0:##判断首位是否为0,0代表无扩展，1代表扩展
            self.field["LEN"] = len0
            leftframe = leftframelen[2:]
            return len0,leftframe
        else:
            len0 = leftframe[:4]
            self.field["LEN"] = len0
            leftframe =leftframe[4:]
            return len0,leftframe
    
    def CTR(self):
        _,leftframectr = self.LEN()
        ctr = leftframectr[:2]#从剩余字符串头部截取两个字符，也就是一个字节
        returnctr = ctr#只做返回值使用,只表示ctr0字节
        if int(ctr,16)&0x80==1:#=1表示无扩展控制码
            self.field["CTR"] = (ctr)
            leftframe = leftframectr[2:]
            return returnctr,leftframe
        else:#有扩展控制码
            i = 1
            chars = ctr
            while int(ctr,16)&0x80==0:#循环判断默认ctr之后的扩展字节是否可扩展
                ctr = leftframectr[2*i:2*i+2]
                chars += ctr##字符串拼接 
                i+=1
            self.field["CTR"] = chars #讲扩展的CTR(ctr0,ctr1,...)构成的字符串追加进入域的全局变量中
            leftframe = leftframectr[2*i:]#捕获去掉ctr0,ctr1,...剩余的字符串
            ##提取出ctr1内容部分
            ctr1 = self.field["CTR"][2:4]
            num  = int(ctr1,16)
            if num==0x07:#代表寻址方式是广播
                print "广播占得字节长度无"
                pass
            elif num==0x06:##代表寻址方式是LA
                self.field["ADDR"] = leftframe[:2]
                
            elif num==0x05:##代表寻址方式是ID
                self.field["ADDR"] = leftframe[:24]
                
            elif num==0x04:##代表寻址方式是UC
                n= 2##这个不对2<=n<=8
                self.field["ADDR"] = leftframe[:n]
            else:
                pass##预留
            
#             return returnctr,self.leftframe[2*i:]#返回ctr第一个字节（便于获得首字节的每一位的信息）、后续长度的剩余字符串
        
    def MAM(self):#MAM域占一个字节
        '''E7 10231195711100600800100009190069711100600850120115B8C0FF4FB1'''
#         ctr =  self.field[:-1][:2]#获取当前self.field最后一个元素的值，也就是ctr,并截取该字符串的前两位（因为ctr可能会有扩展字节）
        ctr,leftframemam = self.CTR()#获取CTR处理后的字符串，得到一个包含MAM、ADDR、SER、DI、DATA、FCS域的字符串
        #处理剩余字符串，从剩余字符串中提取MAM域
        
        if ctr&0x20==1:##根据ctr第五（从0到7）个比特位判断是否存在多级地址,第五比特位0表示存在多级地址，1表示不存在
            #不存在多级地址的处理流程
            self.field["MAM"] = ""#不存在多级地址，当前对象的field域，追加空串
            return leftframemam #不存在多级地址情况下，直接返回当前字符串
        else:##存在多级地址如下处理
            self.field["MAM"] = leftframemam[:2]#MAM占一个字节
            return leftframemam[2:]#返回去掉多级地址的的字符串            
    
    def ADDR(self):#addr是由CTR1控制的，也就是说当存在CTR1时，ADDR也就存在,ADDR的具体形式由见表2-4寻址方式定义
        leftframeaddr = self.MAM()##获取MAM()处理后的字符串
        
        
    
    def SER(self):#长度为1个字节
        pass
    
    def DI(self):##
        pass
    
    def DATA(self):
        pass
    
    def FCS(self):#获取校验码，长度为2个字节
        fcs = self.usefulframe[-4:]
        return fcs
        


if __name__=="__main__":
    fa = FrameAnnalysis()
    


