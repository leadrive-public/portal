import smtplib
from email.mime.text import MIMEText
from email.header import Header

from .database import mailSettings as settings

def sendEmail(receivers, subject:'str', content:'str', sender:'str'=None):
    host=settings.host
    port=settings.port
    user=settings.user
    password=settings.password
    senderDefault=settings.email

    smtp=smtplib.SMTP(host=host, port=port)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(user=user, password=password)

    message = MIMEText(content, 'html', 'utf-8')
    if sender==None:
        sender=senderDefault
    message['From']=sender
    message['To']='jun.zhu@leadrive.com'
    message['Subject']=subject

    try:
        print(message.as_string())
        smtp.sendmail(senderDefault, receivers,message.as_string())
        print ("邮件发送成功")
        smtp.quit()
    except smtplib.SMTPException as e:
        print(e)
        print ("Error: 无法发送邮件")

if __name__=='__main__':
    sendEmail(receivers=['jun.zhu@leadrive.com'],subject='测试',content='<h1>测试</h1>', sender='etime@leadrive.com')