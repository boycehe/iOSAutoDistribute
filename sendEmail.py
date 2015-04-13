#Filename sendEmail.py
import smtplib
from email.MIMEText import MIMEText

mailto_list=["xxx@gmail.com"]
mail_host="smtp.gmail.com"
mail_user= "xxxxx"
mail_pwd = "xxxx"
mail_postfix="gmail.com"

def send_mail(to_list,sub,content):
        me = "hello"+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content)
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            s = smtplib.SMTP()
            s.connect(mail_host)
            s.login(mail_user,mail_pwd)
            s.sendmail(me,to_list,str(msg))
            s.close()
            return True
        except Exception,e:
            print str(e)
            return False
#if __name__ == '__main__':
#    if send_mail(mailto_list,"hello","<a href='http://www.cnblogs.com/xiaowuyi'>xiaowuyi</a>"):
#        print "send email Successfully"
#    else:
#        print "send email Fail"
