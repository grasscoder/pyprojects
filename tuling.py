# -*-coding:utf-8 -*-
import itchat,time,re
from itchat.content import *
import urllib,urllib2
import json

def sendMessage(msg):
    info = msg['Text'].encode('UTF-8')
    url = 'http://www.tuling123.com/openapi/api'##接口url
    data = {u'key':"fb6a17ef837e4012a125f3aeddc9f47c","info":info,u"loc":'',"userid":''}
    data = urllib.urlencode(data)
    url2 = urllib2.Request(url,data)
    response = urllib2.urlopen(url2)
    apicontent = response.read()
    s = json.loads(apicontent,encoding='utf-8')
    print "s==",s
    if s['code']==100000:
        itchat.send(s['text'],msg['FromUserName'])

@itchat.msg_register([TEXT])
def text_reply(msg):
    msgType = msg['MsgType']
    if msgType==1:##文字消息
        sendMessage(msg)
#     info = msg['Text'].encode('UTF-8')
#     url = 'http://www.tuling123.com/openapi/api'##接口url
#     data = {u'key':"fb6a17ef837e4012a125f3aeddc9f47c","info":info,u"loc":'',"userid":''}
#     data = urllib.urlencode(data)
#     url2 = urllib2.Request(url,data)
#     response = urllib2.urlopen(url2)
#     apicontent = response.read()
#     s = json.loads(apicontent,encoding='utf-8')
#     print "s==",s
#     if s['code']==100000:
#         itchat.send(s['text'],msg['FromUserName'])
    elif msgType == 3:##图片消息
        info = '不要给我发图片消息'.encode('UTF-8')
#         url = 'http://www.tuling123.com/openapi/api'##接口url
#         data = {u'key':"fb6a17ef837e4012a125f3aeddc9f47c","info":info,u"loc":'',"userid":''}
#         data = urllib.urlencode(data)
#         url2 = urllib2.Request(url,data)
#         response = urllib2.urlopen(url2)
#         apicontent = response.read()
#         s = json.loads(apicontent,encoding='utf-8')
        s = {'text':'不要给我发图片消息'.encode("UTF-8")}
        if s['code']==100000:
            itchat.send(info,msg['FromUserName'])

if __name__=="__main__":
    itchat.auto_login(enableCmdQR = 2,hotReload = True)
    itchat.run(debug = True)






