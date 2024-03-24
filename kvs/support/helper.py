import argparse
import hashlib
import os
import cv2
from PIL import Image
from pytesseract import Output
from plyer import stt,tts
import speech_recognition as sr
import numpy as np
import imaplib,email
from imap_tools import MailBox,AND
import html2text
from passlib.hash import pbkdf2_sha256
import random,re
import pytesseract
from kvs.support.process_image import get_greyscale, resize_with_aspect_ratio

class Helper:
        
    def speak(content):
        try:
            tts.speak(message =content) 
        except NotImplementedError:
            print("error")
            
           
    def takecmd():
        r = sr.Recognizer()
        
        try:
            
            print("done")
            with sr.Microphone() as speech2txt:
                print("listening..")
                r.pause_threshold = 0.8
                r.adjust_for_ambient_noise(speech2txt, duration= 0.2)
                speech2txt = r.listen(speech2txt)
                Helper.speak("recognizing")
                myspeech = r.recognize_google(speech2txt,)
                myspeech = myspeech.lower()
                
                print("done", myspeech)
                
                return myspeech
        except sr.WaitTimeoutError:
             print(sr.WaitTimeoutError)
        except sr.RequestError:
            print(sr.RequestError)
            Helper.speak("Check internet connection")
        except sr.UnknownValueError:
            print(sr.UnknownValueError)
            Helper.speak("Please repeat")
            return "null"
        return "null"
    
    def clean(text):
    # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)
   
    def recievemail():
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        emailid = "finalyearproject625@gmail.com"
        password = "nxrb xosp fbsu nafx"
        data = []
        with  MailBox('imap.gmail.com').login(emailid,password=password) as mail:
            for msg in mail.fetch():
                fromva = msg.from_
                print(msg.date,msg.subject)
                print(msg.text or msg.html)
                print(msg.attachments)
                print("below")
                date = msg.date
                subject = msg.subject
                text = msg.text
                att_files = []
                text_img = ""
                att_files += [att.payload for att in msg.attachments if att.filename.endswith('.jpg' or 'jpeg')]
                for att in msg.attachments:
                    print(att.filename, att.content_type)
                    dire =os.getcwd()+"\\images\\"+str(att.filename)
                    with open(os.getcwd()+"\\images\\"+str(att.filename), 'wb') as f:
                        print(dire,"ddire")
                        if os.path.isfile(dire):
                            print("done old")
                            text_img = Helper.detect_words(path=dire)
                        else:
                            f.write(att.payload)
                            text_img = Helper.detect_words(path="ff")
                    
                    if os.path.isfile(dire):
                        os.remove(dire)
                    print(text_img,"ff")
                try:
                    re.sub("(?P<url>https?://[^\s]+)","link ", text).group("url")
                except AttributeError:
                    re.sub("(?P<url>https?://[^\s]+)", "link",text)
                val = {
                    "From": fromva,
                    "Date": date,
                    "Subject":subject,
                    "Content": text,
                    "atta": att_files,
                    "text_img":text_img
                }
                data.append(val)
            print(data,"data  ")
        return data
    

    def detect_words(path):

        if path:
            #path = os.getcwd()
            # Read image 
            path = "C:\\Users\\91637\\Desktop\\project\\images\\success.jpg"
            
            #We then read the image with text
            images=cv2.imread(path)
            print(images)
            pytesseract.pytesseract.tesseract_cmd  ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            #convert to grayscale image
            gray=cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
            
            #checking whether thresh or blur
            
            thresh = cv2.threshold(gray, 0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
           
                
            #memory usage with image i.e. adding image to memory
            
            text = pytesseract.image_to_string(thresh)
            
            print(text)
            
            


            '''img = cv2.imread(path)
            img_draw_boxes = get_greyscale(img)
            img_predict = get_greyscale(img)

            # Draw boxes around words
            data = tesseract.image_to_data(img_draw_boxes, output_type = Output.DICT)
            n_boxes = len(data["text"])
            for i in range(n_boxes):
                if float(data["conf"][i]) > 60:
                    # Detects the dimensions of the box that needs to be drawn
                    (x, y, w, h) = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
                    # Draws a green box around the word
                    img = cv2.rectangle(img_draw_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)

            resize = resize_with_aspect_ratio(img_draw_boxes, height=900)
            #cv2.imshow("Detected Words", resize)
            lang ="eng"
            # Find words in image and turn it into a string
            custom_config = f"-l {lang} --oem 1 --psm 3"
            text = pytesseract.image_to_string(img_predict, config=custom_config)'''

            
            return text
        '''imap.login(emailid,password)
        
        imap.select("INBOX")
        status, data = imap.search(None,"ALL")
                
        tmp, data = imap.search(None,  'FROM', '"Jagan Chandru"')
        for num in data[0].split():
            tmp, data = imap.fetch(num, '(RFC822)')
            print('Message: {0}\n'.format(num))
            pprint.pprint(data[0][1])
            break
        imap.close()
        
        for num in data[0].split():
            
            stat, data  = imap.fetch(num, "(RFC822)")
            print(stat," doin")
            email_msg = email.message_from_bytes(data[0][1])
            print("From : ",email_msg["From"])
            print("Date : ",email_msg["Date"])
            print("Subject : ",email_msg["Subject"])
            print("se ",email_msg )
            print("Body : ",email_msg.get_payload()[0].get_payload())
            print()

        for block in messages:
            print(f"block {block}")
            mail_id += block.split()
        for  i  in mail_id:
            res,msg =imap.fetch(i, "(RFC822)")
            message = email.message_from_bytes(msg[0][1])
            print(f"MEssage no:{i} ")
            print(f"from :{message.get('From')} ")
            print(f"TO :{message.get('To')} ")
            print(f"BCc :{message.get('Bcc')} ")
            print(f" Date :{message.get('Date')} ")
            print(f" subj :{message.get('Subject')} ")

            print("content ")
           
            if message.is_multipart():
                print('Multipart types:')
                for part in message.walk():
                    print(f'- {part.get_content_type()}')
                multipart_payload = message.get_payload()
                for sub_message in multipart_payload:
                    # The actual text/HTML email contents, or attachment data
                    #print(f'Payload\n{sub_message.get_payload()}')
                    mail_content =''
                    if sub_message.get_content_type() == 'text/plain':
                        mail_content += sub_message.get_payload()
                        print(mail_content)
                        
                    elif sub_message.get_content_type() == 'text/html':
                        text = f"{sub_message.get_payload()}"
                        html = text.replace("b'", "")
                        h = html2text.HTML2Text()
                        h.ignore_links = True
                        output = (h.handle(f'''''').replace("\\r\\n", ""))
                        output = output.replace("'", "")
                        print(f"output : {output}")
            else:  # Not a multipart message, payload is simple string
                #print(f'Payload\n{message.get_payload()}')
                text = f"{message.get_payload(decode=True)}"
                #Helper.speak(text.replace(" ' ",""))
                print(" NOOT MULTI",text)
        imap.close()
        imap.logout()'''
    def Hash(input_text):
        hash = pbkdf2_sha256.hash(input_text, rounds=20000, salt_size=16)
        print(hash)
        return hash
    def rand():
        a = random.randint(1000,9999)
        return a