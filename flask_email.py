# -*-coding:utf-8 -*-
'''
Created on 2017��4��20��

@author: Administrator
'''
from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    MAIL_SERVER='smtp.163.com',
    MAIL_PROT=25,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'hu600hu@163.com',
    MAIL_PASSWORD = 'hql19900313',
    MAIL_DEBUG = True
)

mail = Mail(app)

@app.route('/')
def index():
# sender 发送方，recipients邮件接收方列表
    msg = Message("发一张 图片给你看看我的头像，在附件中",sender='xiangcai@163.com', recipients=['976825033@qq.com'])
# msg.body 邮件正文
    msg.body = "给你发一封测试邮件，用代码写的"
# msg.attach 邮件附件添加
# msg.attach("文件名", "类型", 读取文件)
#     with app.open_resource("F:\\1.jpg","rb") as fp:
#         msg.attach("image.jpg", "image/jpg", fp.read())
#     with app.open_resource("F:\\new.docx","rb") as fp:
#         msg.attach("pic.docx", "txt/docx", fp.read())
    with app.open_resource("F:\\new.rar","rb") as fp:
        msg.attach("pic.rar", "zip/rar", fp.read())

    try:
        mail.send(msg)
    except Exception,e:
        
        print "send error"+str(e)
        return "send error"+str(e)
    else:
        return "Sent successfully"

if __name__ == "__main__":
    app.run()
