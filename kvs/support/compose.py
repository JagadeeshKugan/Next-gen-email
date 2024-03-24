import smtplib
import mimetypes
import email
import email.mime.application
import email.mime.image
class mailer:
   
    def send(from_, to, content,fileloc,password):
        msg = email.mime.Multipart.MIMEMultipart()
        msg['Subject'] = "Sample"
        msg['From'] = from_
        msg['To'] = to

        # The main body is just another attachment
        body = email.mime.Text.MIMEText(content)
        msg.attach(body)
        filename= fileloc
        fp=open(filename,'rb')
        img = fp.read()
        att = email.mime.image(img,name="attached")
        #email.mime.application.MIMEApplication(fp.read(),_subtype="jpg")
        fp.close()
        att.add_header('Content-Disposition','attachment',filename=filename)
        msg.attach(att)
        passwrd = password
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.starttls()
        mailserver.login(from_, passwrd)
        mailserver.sendmail(from_,to,str(msg))
        mailserver.quit()
        return "sent"