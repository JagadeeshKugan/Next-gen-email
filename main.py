import os
import time
import kivy 
from  plyer import filechooser
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang.builder import Builder
from demo.demo import sample_data
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.floatlayout import MDFloatLayout
import speech_recognition as sr
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import BooleanProperty, DictProperty, ListProperty, ObjectProperty, OptionProperty, StringProperty
from kvs.support.compose import mailer
from kvs.support.helper import Helper
from kivy.graphics import  Line,Ellipse,Color
from kvs.pages.register.auth import auther
from kivy.uix.widget import Widget
from kivymd.uix.snackbar.snackbar import MDSnackbar,MDSnackbarText
Window.size = (320,600)
Builder.load_file('kvs/widget/chat_list_item.kv')
Builder.load_file('kvs/widget/avatar.kv')
Builder.load_file('kvs/widget/navdrawer.kv')
Builder.load_file('kvs/pages/message.kv')
Builder.load_file('kvs/pages/inputpage.kv')


store = JsonStore('login.json')


'''class Check(Screen):
    text1 = StringProperty()
    Builder.load_file('kvs/pages/check.kv')
    def record(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as speech2txt:
                print("listening..")
                r.adjust_for_ambient_noise(speech2txt, duration= 0.2)
                speech2txt = r.listen(speech2txt)
                print("recognining..")
                myspeech = r.recognize_google(speech2txt,)
                myspeech = myspeech.lower()
                self.text1 = str(myspeech)
                print("done", myspeech)
        except sr.RequestError:
            print(sr.RequestError)
        except sr.UnknownValueError:
            print(sr.UnknownValueError)
            pass'''

class Drawe(Widget):
    Builder.load_file("kvs/widget/drawe.kv")
    def on_touch_down(self, touch):
         with self.canvas:
            Color(0,0,0)
            d = 30.
            
            touch.ud['line'] = Line(points=(touch.x, touch.y))
    def on_touch_move(self, touch):
        
        touch.ud['line'].points += [touch.x,touch.y]
class Inputpage(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class Message(Screen):
    value = StringProperty()
    timestamp = StringProperty()
    profile = DictProperty()
    
    friend_name = StringProperty()
    def on_enter(self, *args):
        global gett
        #gett = Helper.recievemail()
    
    def check(self):
        Helper.speak("what do you want to do ?")
        le = Helper.takecmd()
        print(str(le))
        if "compose"  in le:
            self.manager.current = "compose"
        elif "read" in str(le):
            Helper.speak("Tell the number to open")
            num = Helper.takecmd()
            li = [1,2,3,4,5,6,7,8,9]
            for val in li:
                #print(val)
                if str(val) in num:
                    numb = val
            print(num)
            numb = 5
            print(numb)
            if numb :
                MainApp.create_chat(self=self,profile=sample_data[int(numb)-1])
            else:
                Helper.speak("please tell a number")
        elif "log out" or "Logout" in  le:
            store.delete('email')
            store.delete('code')

            self.manager.current = "loginwithcode"
        else:
            Helper.speak("Press again")
       

class NavBar(Screen):
    pass

class MailScreen(Screen):
    from_mail = StringProperty()
    _subject = StringProperty()
    content = StringProperty()
    date = StringProperty()
    img = StringProperty()
    gett = DictProperty()
    Builder.load_file('kvs/pages/mailscreen.kv')
    #language = StringProperty("eng")
    
    def checker(self,gett):
        #pass
       
        Helper.speak("Shall i read the content ?")
        ye = Helper.takecmd()
        if"yes" or "Yes" in ye:
            Helper.speak(" Mail from user " +gett["From"] )
            Helper.speak(" subject from user " +gett["Subject"] )
            Helper.speak(" Body of the message from user " +gett["Body"] )
            Helper.speak(" It was sent you on  " +gett["date"] )
            Helper.speak("image content "+ gett["text_img"] if gett["text_img"] else "nil")
           # Helper.speak("do you want to go back ?")
            spe = Helper.takecmd()
            if  "yes" or "Yes" in  spe:
                self.manager.current = "message"
           
        elif "no" or "No" in ye:
            Helper.speak("Navigating to back screen")
            self.manager.current = "message"

class Compose(Screen):
    email_input = StringProperty()
    subject = ObjectProperty()
    Builder.load_file('kvs/pages/compose.kv')
    def filechoose(self):
        global filpath
        filpath = filechooser.open_file(on_select = self.select)
        self.ids.file.text = str(filpath)
    def select(self,selection):
        print(selection)

    def listenup(self):
        Helper.speak("say the To email address")
        to1 = Helper.takecmd()
        print(to1)
        to = to1.replace(" ","")
        self.ids.to_Email_input.text =to
        content = self.ids.input.text
        if content =="":
            Helper.speak("Please enter content"+str(to))
            cont = Helper.takecmd()
            content = cont
            self.ids.input.text =content
        Helper.speak("say send")
        speech = Helper.takecmd()
        if speech == "send":
            Compose.sendemail()
    def sendemail(self):
        fromid = email_id  #"finalyearproject625@gmail.com"
        to = str(self.ids.to_Email_input.text)
        content = self.ids.input.text
        passwrd = codedata
        fileway = filpath
        if to and content:
            
            index = to.find("@gmail.com")
            if index == -1:
                to = to +"@gmail.com"
                
            print(to+" "+content)
            if to != "":
                res = mailer.send(from_=fromid, to=to, content=content,fileloc=fileway,password=codedata)
            print(res)
            Helper.speak("sent successfully to "+to)
        else:
            Helper.speak("say the To email address")
            to1 = Helper.takecmd()
            print(to1)
            to2 = to1.replace(" ","")
            self.ids.to_Email_input.text =to2
            content = self.ids.input.text
            if content =="":
                Helper.speak("Please enter content"+type(to))
                cont = Helper.takecmd()
                contt = cont
                self.ids.input.text =contt
            Helper.speak("say send")
            speech = Helper.takecmd()
            if speech == "send":
                mailres = mailer.send(from_=fromid,to=to2, content=contt, )
                print(mailres)
                if mailres == "sent":
                    Helper.speak("sent successfully to "+to)
        self.ids.to_Email_input.text =""
        self.ids.input.text =""
        self.manager.current = "message"



class Splashscreen(Screen):
    Builder.load_file('kvs/pages/splash.kv')
    pass



class Register(Screen):
    Builder.load_file('kvs/pages/register.kv')
    def registeruser(self):
        email = self.ids.email.text
        passwordd = self.ids.password_in.text
        code = self.ids.code_in.text
        global codedata
        if email and passwordd and code:
            data = {
                "email":email,
                "password": passwordd,
                "code": code        }
        else:
            Helper.speak("tell me your  email address")
            print("doing")
            emailid =  Helper.takecmd()
            
            emailid = str(emailid)
            emailid.replace(" ","")
            index = emailid.find("@gmail.com")
            if index == -1:
                emailid = emailid +"@gmail.com"
            
            Helper.speak("Now, your password")
            

            password = Helper.takecmd()
            password = str(password)
            Helper.speak("Now, your email code")
            codeval = Helper.takecmd()
            self.ids.email.text = emailid
            self.ids.password_in.text = password
            self.ids.code_in.text = codeval
            
            passcode = password.split()
            print(passcode,"DD")
            fin = ""
            for i in passcode:
                if passcode.index(i) != (len(passcode)-1):
                    fin += i[:1]
                else:
                    fin += i
            Helper.speak("wait, Registering user")
            print(fin)
            data = {
                "email":emailid,
                "password": fin,
                "code": codeval  
            }
           
        Helper.speak("say register to complete")
        reg = Helper.takecmd()
        if str(reg) == "register":
            res,codewrd = auther.register(data)
            if res == "success":
                global email_id 
                store.put('email', email = emailid, code=codeval)
                store.put('code',codenum = codewrd)

                email_id = data["email"]
                codedata = codeval
                MainApp.show_toast(self=self,msg="User registered successfully!")
                self.manager.current = "message"
            else:
                MainApp.show_toast(self=self,msg="error occured. USer already exist")
                Helper.speak("error occured")
        
    #pass

class Logincode(Screen):
    Builder.load_file("kvs/pages/loginwithcode.kv")
    codein = StringProperty()
    def login(self):
        
        cc = self.ids.code_in.text
        #resu = auther.loginwithcode(cc)
        if cc:
            print("login")
           

            resu = auther.loginwithcode(cc)
            time.sleep(10)
                
            
            
            if resu != []:
                res=resu[0]
                stat=resu[1],
                code=resu[2], 
                email=resu[3],
        elif self.codein:
            print(self.codein,"LL")
            resu = auther.loginwithcode(self.codein)
        
        print(resu)
        if res == "success"and stat:
            store.put('email', email = email, code=code)
            store.put('code',codenum = cc)
            codedata = code
            email_id = email
            print(codedata," dddd ",email_id)
            MainApp.show_toast(self=self,msg="Login Successful!")
            self.manager.current = "message"
        else:
            MainApp.show_toast(self=self,msg="Error while Login")
        print()
    def listener(self):
        Helper.speak("hi, i can listen now")
        #time.sleep(2)
        Helper.speak("do you want to login ?")
        ye = Helper.takecmd()
        ye = str(ye)
        if  "yes" or  "Yes" in ye:
            Helper.speak("say the code") 
            cod = Helper.takecmd()
            self.ids.code_in.text = cod
            self.codein = cod
            Logincode.login(self=self)

           
        elif ye == "no" or ye == "No":
            Helper.speak("Do you want to register?")
            

            cmt = Helper.takecmd()
            if "no" in cmt:
                exit()
            elif str(cmt) == "yes":
                self.manager.current = "register"

        else:
            Helper.speak("error occured. Press again")

#Login class 
class Login(Screen):
    email = ObjectProperty()
    password = ObjectProperty()
    Builder.load_file('kvs/pages/login.kv')


    def on_enter(self, *args):
        Helper.speak("Press bottom to listen")
        return super().on_enter(*args)
        
    def listener(self):
        Helper.speak("hi, i can listen now")
        #time.sleep(2)
        Helper.speak("do you want to login ?")
        ye = Helper.takecmd()
        ye = str(ye)

        if "Yes" or  "yes" in ye:
            Helper.speak("do you want to login by code?")
            mode = Helper.takecmd()
            if "yes" in mode:
                self.manager.current = "loginwithcode"
            elif "no" in  mode:
                Helper.speak("tell me your login email address")
                print("doing")
                emailid =  Helper.takecmd()
                
                emailid = str(emailid)
                emailid.replace(" ","")
                index = emailid.find("@gmail.com")
                if index == -1:
                    emailid = emailid +"@gmail.com"
                
                Helper.speak("Now, your password")
                
                password = Helper.takecmd()
                password = str(password)
                self.ids.email.text = emailid
                self.ids.password_input.text = password
                self.ids.tts.text = "validating.."
                passcode = password.split()
                fin = ""
                for i in passcode:
                    if passcode.index(i) != (len(passcode)-1):
                        fin += i.index(0)
                    else:
                        fin += i
                
                print(fin)
                res,code = self.login(emailid=emailid,password=fin)
                if res == "success":
                    
                    codedata = code
                    print(codedata)
                    Helper.speak("say login to complete")
                    speech = Helper.takecmd()
                    print (speech+ " "+password)
                    if speech == "login":
                        store.put('email', email = emailid, code=code)
                        #store.put('code',codenum = )
                        self.manager.current = "message"
                else:
                    Helper.speak("Invalid credentials")
            else:
                Helper.speak("Error, press again")
        elif ye == "no" or ye == "No":
            Helper.speak("Do you want to register?")
           

            cmt = Helper.takecmd()
            if str(cmt)=="close":
                exit()
            elif str(cmt) == "yes":
                self.manager.current = "register"

        else:
            Helper.speak("error occured. Press again")
        



    def login(self, emailid, password):
        if emailid != "" or password != "":
            val,status,code =  auther.login({"email":emailid, "password": password})
            if status:
                return val,code
        else:
            return "null"
    def check(self):
        emailid = self.ids.email.text
        passwordd = self.ids.password_input.text
        if emailid and passwordd :
            res,code =self.login(emailid=emailid,password=passwordd)
            if  res == "success":
                codedata = code
                self.manager.current = "message"
        else:
            Helper.speak("Enter Credentials") 
    


class ChatListItem(MDCard):
    value= StringProperty()
   
    timestamp = StringProperty()
    profile = DictProperty()
    
    friend_name = StringProperty()
    

class MainApp(MDApp):
    
    

    def build(self):
        '''initiqalize app'''
        #global
        global val
        val = []
        if store.exists('code'):
            print('tite exists:', store.get('code'))
            codenum = store.get('code')['codenum']
            
            val = auther.loginwithcode(codenum)
            print(val)
            if val is None: 
                print("error")
            else:
                codedata = val[2]
                email_id = val[3]
        self.wm =  ScreenManager(transition=FadeTransition())
        
       # wm =  WindowManager(transition=FadeTra)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = 'Olive'
       # self.theme_cls = 'Teal'
        self.theme_cls_accent_hue = '400'

        self.title = "Email App"
        screens = [Splashscreen(name="splash"),
                   Login(name="login"),
                    
                    Message(name = "message"),
                    MailScreen(name="mailscreen"),
                    Register(name="register"),
                    NavBar(name="navbar"), 
                   
                    Logincode(name="loginwithcode"),
                    Inputpage(name="input"),
                    Compose(name="compose"),]
        
        
        for screen in screens:
            self.wm.add_widget(screen)
        if val:
            self.wm.current="message"
        else:
            self.wm.current="loginwithcode"
        self.chat_list_builder()
        return self.wm
    
    #def on_start(self):
        Clock.schedule_once(self.logine, 5)
    
    #def logine(self,*args):
     #    self.wm.current = "login" 
    

    def chat_list_builder(self):
        for profile in sample_data:
            
            self.chatitem = ChatListItem()
            self.chatitem.value =  profile["From"][:1].capitalize()
            self.chatitem.friend_name = profile["Subject"][:25] if profile["Subject"] != "" else "No subject"
            self.chatitem.timestamp = profile['Date']
            self.chatitem.profile =profile
            
            #lastMessage, time, isRead, sender = message.split(';')
            #elf.chatitem.msg = lastMessage
            #                self.chatitem.timestamp = time
            #   self.chatitem.isRead = isRead
                #self.chatitem.sender = sender
            self.wm.screens[2].ids['chatlist'].add_widget(self.chatitem)
    def show_toast(self, msg):
        duration = 5
        ss = MDSnackbar( MDSnackbarText(
        text=msg,
        ),
        y=(24),
        pos_hint={"center_x": 0.5},
        size_hint_x=0.5,)
        ss.open()



    def create_chat(self, profile):
        '''Get all messages and create a chat screen'''
        self.chat_screen = MailScreen()
        
    
       # self.msg_builder(profile, self.chat_screen)
        self.chat_screen.from_mail = profile['From']
        self.chat_screen._subject = profile['Subject']
        self.chat_screen.content = profile['Body']
        self.chat_screen.date=profile['Date']
        self.chat_screen.gett = profile
        #self.chat_screen.img = profile['text_img']
        self.wm.switch_to(self.chat_screen)

    def msg_builder(self, profile, screen):
        '''Create a message bubble for creating chat.
        for prof in profile['msg']:
            for messages in prof.split("~"):
                if messages != "":
                    message, time, isRead, sender = messages.split(";")
                    self.chatmsg = ChatBubble()
                    self.chatmsg.msg = message
                    self.chatmsg.time = time
                    self.chatmsg.isRead = isRead
                    self.chatmsg.sender = sender
                    screen.ids['msglist'].add_widget(self.chatmsg)
                else:
                    print("No message")

                print(self.chatmsg.isRead)'''
    def change_screen(self, screen):
        '''Change screen using the window manager.'''
        self.wm.current = screen
	

if __name__ == "__main__":
    MainApp().run()