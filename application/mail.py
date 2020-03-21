import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import threading

from .database import mailSettings as settings

class SendMailThread(threading.Thread):
    def __init__(self, receivers, subject:'str', content:'str', sender:'str'=None):
        threading.Thread.__init__(self)
        self.receivers=receivers
        self.subject=subject
        self.content=content
        self.sender=sender
    def run(self):
        host=settings.host
        port=settings.port
        user=settings.user
        password=settings.password
        senderDefault=settings.email
        smtp=smtplib.SMTP(host=host, port=port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user=user, password=password)
        message = MIMEText(self.content, 'html', 'utf-8')
        if self.sender==None:
            self.sender=senderDefault
        message['From']=self.sender
        for receiverIndex in range(len(self.receivers)):
            receiver=self.receivers[receiverIndex]
            if receiverIndex==0:
                messageTo=receiver
            else:
                messageTo+=';'+receiver
        message['To']=messageTo
        message['Subject']=self.subject
        try:
            print(message.as_string())
            smtp.sendmail(senderDefault, self.receivers, message.as_string())
            print ("邮件发送成功")
            smtp.quit()
        except smtplib.SMTPException as e:
            print(e)
            print ("Error: 无法发送邮件")

def sendEmail(receivers, subject:'str', content:'str', sender:'str'=None):
    sendMailThread=SendMailThread(receivers=receivers, subject=subject, content=content, sender=sender)
    sendMailThread.start()

if __name__=='__main__':
    sendEmail(receivers=['jun.zhu@leadrive.com'],subject='测试',content='<h1>测试</h1>', sender='etime@leadrive.com')