# -*-coding:utf-8 -*-
from data import UnpackFrame
'''由于本类是基于字符串的处理进行的，所以需要判断字符在[0-9a-z],这个需要加判断审核，建议使用re表达式'''
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
        self.framelen = self.getFramelen() ##表示整帧长度
#         self.field = []##全局列表变量解析之后的报文，是以列表的形式存放在这个self.field中
        self.field = {"HEAD":'',"LEN":'',"CTR":'',"MAM":'',"ADDR":'',"SER":'',"DI":'',"DATA":'',"FCS":''}

    def getFramelen(self):#当前报文的长度
        framelen,_ = self.LEN()
        if len(framelen)==2:
            return int(framelen,16)##当前实例化帧的长度的10进制整形值
        else:
            return int(framelen[:2],16)&0x7f + int(framelen[2:],16)
    
    def HEAD(self):
        leftframehead = self.usefulframe[2:]##去掉头部的7F标记,剩下的字符串中继续进行解析
        self.field["HEAD"] = "7F"
        return leftframehead #返回'1FD5E710231195711100600800100009190069711100600850120115B8C0FF4FB1'
        
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
            len01 = leftframe[:4]##有扩展长度
            self.field["LEN"] = len01
            leftframe =leftframe[4:]
            return len01,leftframe##返回的是包含扩展长度的字符串两个字节4个16进制字符
    
    def CTR(self):
        _,leftframectr = self.LEN()
        ctr0 = leftframectr[:2]#从剩余字符串头部截取两个字符，也就是一个字节就是ctr0
        returnctr = ctr0#只做返回值使用,只表示ctr0字节,类型是字符串
        if int(ctr0,16)&0x80==1:#=1表示无扩展控制码
            self.field["CTR"] = ctr0
            leftframe = leftframectr[2:]
            return returnctr,leftframe
        else:#==0有扩展控制码
            i = 1
            chars = ctr0
            while int(ctr0,16)&0x80==0:#循环判断默认ctr之后的扩展字节是否可扩展
                ctr0 = leftframectr[2*i:2*i+2]#此ctr0并不是指字符串开头
                chars += ctr0##字符串拼接 
                i+=1
                
            self.field["CTR"] = chars #讲扩展的CTR(ctr0,ctr1,...)构成的字符串追加进入域的全局变量中
            leftframe = leftframectr[2*i:]#捕获去掉ctr0,ctr1,...剩余的字符串
            return returnctr,leftframe#返回ctr第一个字节（便于获得首字节的每一位的信息）、后续长度的剩余字符串
        
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
    
    def ADDR(self):#addr是由CTR的b0-b2比特位控制的，当存在CTR1时，CTR1的b2-b0比特位表示的主站寻址方式，只存在ctr0时，b2-b0比特位表示从站的寻址方式，主从的寻址方式都是一样的
        leftframeaddr = self.MAM()##获取MAM()处理后的字符串
        ##提取出ctr1内容部分
        ctr0 = self.field["CTR"][:2]
        if int(ctr0,16)&0x80==0:
            ctr1 = self.field["CTR"][2:4]
            num1  = int(ctr1,16)
        num = int(ctr0,16)
        
        if num is 0x07:#代表寻址方式是广播，长度为0字节
            self.field["ADDR"] = ""#直接返回原字符串
            return leftframeaddr
        elif num==0x06:##代表寻址方式是LA，长度为1
            self.field["ADDR"] = leftframeaddr[:2]
            return leftframeaddr[2:]
        elif num==0x05:##代表寻址方式是ID，长度为12
            self.field["ADDR"] = leftframeaddr[:24]
            return leftframeaddr[24:]
        elif num==0x04:##代表寻址方式是UC，长度为5字节
            self.field["ADDR"] = leftframeaddr[:10]
            return leftframeaddr[10:]    
        elif num==0x03:#长度2字节
            self.field["ADDR"] = leftframeaddr[:4]
            return leftframeaddr[4:]
        elif num==0x02:#长度为4字节
            self.field["ADDR"] = leftframeaddr[:8]
            return leftframeaddr[8:]
        elif num==0x01:#长度为6字节
            self.field["ADDR"] = leftframeaddr[:12]
            return leftframeaddr[12:]
        elif num==0x00:#8字节
            self.field["ADDR"] = leftframeaddr[:16]
            return leftframeaddr[16:]
        else:#0字节
            return leftframeaddr
    
    def SER(self):#长度为1个字节
        leftframeser = self.ADDR()
        self.field["SER"] = leftframeser[:2]
        return leftframeser[2:]
    
    def DI(self):##
        pass
    
    def DATA(self):
        pass
    
    def FCS(self):#获取校验码，长度为2个字节
        fcs = self.usefulframe[-4:]
        return fcs
        


if __name__=="__main__":
    fa = FrameAnnalysis()
    


