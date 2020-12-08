import os
from time import sleep
from PIL import Image 
import os
import yaml
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# CREATE FOLDERS 

class imageTo3d():
    def __init__(self, foldername, typeOf3d, email, waitTime):
        self.foldername = foldername
        self.typeOf3d = typeOf3d
        self.email = email
        self.waitTime = waitTime
        #swing or zoomin
        self.createYMLS()
        #print('RAN')

    def runModel(self):
        #ADD TO QUE
        os.chdir('./model')
        print("MODEL JAWN {}".format(os.getcwd))
        os.system("./imageto3d/bin/python main.py --config ymls/{}.yml".format(self.foldername)) #FOR LOCAL USE
        #os.system("python3 main.py --config ymls/{}.yml".format(self.foldername))   #FOR SERVER USE
    
    def createYMLS(self):
        with open('./model/{}.yml'.format(self.typeOf3d)) as file:
            swingList = yaml.load(file, Loader=yaml.FullLoader)
            swingList['src_folder'] = 'image/{}'.format(self.foldername)
            try:
                os.mkdir('./video/{}'.format(self.foldername))
            except:
                None
            swingList['video_folder'] = 'video/{}'.format(self.foldername)
            with open(('./model/ymls/{}.yml'.format(self.foldername)), 'w') as f:
                data = yaml.dump(swingList, f)
                f.close()
            file.close()
    def sendEmail(self):
        #CAN SEND FROM YOUR OWN EMAIL AND PASSWORD
        sender_email = ""
        sender_name = 'Image To 3D'
        password = ''
        receiver_email = self.email
        filename = self.foldername
        os.chdir("..")
        # Email body
        email_html = open('./app/templates/public/email.html')
        email_body = email_html.read()
        exactFileName = ''
        for i in os.listdir('./model/video/{}'.format(filename)):
            if filename in os.path.splitext(i)[0]:
                exactFileName = i
        filepath = 'model/video/{}/{}'.format(filename, exactFileName)
        msg = MIMEMultipart()
        msg['To'] = receiver_email
        msg['From'] = sender_email
        msg['Subject'] = 'Your 3D Image is Ready'
        msg.attach(MIMEText(email_body, 'html'))
        with open(filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Encode file in ASCII characters
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
                "Content-Disposition", 
                "attachment; filename= {}".format(exactFileName)
        )
        msg.attach(part)
        #INPUT MAIL SERVER
        server = smtplib.SMTP_SSL('', 465)
        server.login(sender_email, password)
        context = ssl.create_default_context()
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

