import email
from turtle import title
from tkinter import Label
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
import kivy
from matplotlib.pyplot import text
from kivymd.uix.list import IconRightWidget, ThreeLineAvatarIconListItem
import mysql.connector as mysql
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.toast import toast
from  kivymd.uix.floatlayout import MDFloatLayout
from  kivymd.uix.behaviors import FakeRectangularElevationBehavior
from  kivy.uix.screenmanager import NoTransition
import re
from main_classes import LoginWindow, ProfileCard, ProfilePage, NavBar, MessageScreen, ChatScreen, ChatListItem, ChatBubble, Message, login_page, popFun, P, PopupWindow, VerificationPage, SearchPopupMenu  
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty
from kivy.core.window import Window
from kivymd.uix.picker import MDThemePicker
from demo.demo import profiles
import socket_client
import sys
kivy.require('1.0.8')
from  kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
import re
import random, string
from kivy.clock import Clock


from db_creds import *
from mail_sender import *

SM = None

from kivy.config import Config
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')

Window.size = (320, 600)

Builder.load_file('kvs/pages/chat_screen.kv')
Builder.load_file('kvs/widgets/avatar.kv')
Builder.load_file('kvs/widgets/chat_list_item.kv')
Builder.load_file('kvs/widgets/text_field.kv')
Builder.load_file('kvs/widgets/chatbubble.kv')

class WindowManager(ScreenManager):
    '''A window manager to manage switching between sceens.'''

class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm_password= ObjectProperty(None)
    courses_g1 = StringProperty(None)
    courses_g2 = StringProperty(None)
    courses_g3 = StringProperty(None)
    courses_b1 = StringProperty(None)
    courses_b2 = StringProperty(None)
    
    def __init__(self, username, email, password, confirm_password, courses_g1,  courses_g2, courses_g3, courses_b1, courses_b2): 
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.courses_g1 = courses_g1
        self.courses_g2 = courses_g2
        self.courses_g3 = courses_g3
        self.courses_b1 = courses_b1
        self.courses_b2 = courses_b2

    
    def register(self): 
        global SM
		# Define DB Stuff
        mydb = mysql.connect(
			host = "127.0.0.1", 
			user = "root",
			passwd = "Kirgizistan993",
			database = "dbforusers",
            )

		# Create A Cursor
        c = mydb.cursor()
        email_quary = f"select email from students"
        c.execute(email_quary)
        email_records =  c.fetchall() 
        mydb.commit()
        email_lst = list(x for i in email_records for x in i)
        print(email_lst)
        
        cc =mydb.cursor()
        school_quary = f"select s_email from school_mail"
        cc.execute(school_quary)
        school_strings = cc.fetchall()
        mydb.commit()
        school_lst = list(y for z in school_strings for y in z)
        print(school_lst)
        if self.username != "" and self.email != "" and self.password != "" and self.confirm_password != "" and self.courses_b1 != "" and self.courses_g1 != "": 
            
            if self.email.count("@") == 1 and self.email.count(".") > 0 and self.email not in email_lst and any( [str in self.email for str in school_lst] ):

                if self.password == self.confirm_password and len(self.password) >= 6 and re.search(r"\d", self.password)  and re.search(r"[A-Z]", self.password) and re.search(r"[a-z]", self.password) :
                        
                    verification_code = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(6))
                    info_quary = "insert into students (StudentName, Email, Password, VerifyCode, IsVerified) values (%s, %s, %s, %s, %s)"
                    c.execute(info_quary, (self.username, self.email, self.password, verification_code, 0)) 
                    course_quary = "insert into courses (Email, CanCourse_1, CanCourse_2, CanCourse_3, NeedCourse_1, NeedCourse_2 ) values (%s, %s, %s, %s, %s, %s)"
                    c.execute(course_quary, (self.email, self.courses_g1, self.courses_g2, self.courses_g3, self.courses_b1, self.courses_b2)) 
                    mydb.commit()
                    mydb.close()
                    print("\n\n" + str(self.email))
                    sendEmailVerification(verification_code, str(self.email))
                    toast("Everything is OK so far!")
                    SM.current = "verification"
                    toast("Verification Code has been sent to your email.")
                    return True
                        
                    
                else:
                    toast("Password doesnt match or password not security enough")
                    return False
            else:
                toast("Please check if your email is correct or valid")
                return False       
        else:
            toast("you need to fill in the information")
            return False
    


class MainApp(MDApp):

    def build(self):
        self.sm = WindowManager(transition=FadeTransition())
        self.sm.add_widget(Builder.load_file('login-page.kv'))
        self.sm.add_widget(Builder.load_file('sign_up2.kv'))
        self.sm.add_widget(Builder.load_file('navbar.kv'))
        self.sm.add_widget(Builder.load_file('verification.kv'))

        self.sm.add_widget(Builder.load_file('profile_page.kv'))
        #self.sm.add_widget(Builder.load_file('matching_page.kv'))
        self.sm.add_widget(Builder.load_file('main-2.kv'))
        self.sm.add_widget(Builder.load_file('search_profile.kv'))

        global SM
        SM = self.sm

        """
        self.connect_page = ConnectPage()
        screen = Screen(name='Connect')
        screen.add_widget(self.connect_page)
        self.sm.add_widget(screen)

        # Info page
        self.info_page = InfoPage()
        screen = Screen(name='Info')
        screen.add_widget(self.info_page)
        self.sm.add_widget(screen)
        """
        return self.sm
    
    # def on_start(self):
    #     self.search_menu = SearchPopupMenu()

    def created_account(self):
        name = self.sm.get_screen("create_an_account").ids.new_user.text
        email = self.sm.get_screen("create_an_account").ids.new_email.text
        
        password = self.sm.get_screen("create_an_account").ids.new_password.text
        confirm_password = self.sm.get_screen("create_an_account").ids.new_conf_password.text
        courses_g1 = self.sm.get_screen("create_an_account").ids.good_c1.text
        courses_g2 = self.sm.get_screen("create_an_account").ids.good_c2.text
        courses_g3 = self.sm.get_screen("create_an_account").ids.good_c3.text
        courses_b1 = self.sm.get_screen("create_an_account").ids.bad_b1.text
        courses_b2 = self.sm.get_screen("create_an_account").ids.bad_b2.text

        signup_validitet = CreateAccountWindow(name, email, password, confirm_password, courses_g1, courses_g2, courses_g3, courses_b1, courses_b2).register()
        if signup_validitet :
            self.sm.current = 'verification'
            toast('success')
        else:
            self.sm.current = 'create_an_account'
            popup = Popup(title= 'try again',
                          content= Label(text= 'enter valid info'),
                          size_hint=(None, None), size=(400,400),
                          width = 250, height = 300,
                          auto_dismiss=True )
            popup.open()

    def login_valid(self):
        email = self.sm.get_screen("login").ids.user_email.text
        psw = self.sm.get_screen("login").ids.user_password.text
        validation_status = LoginWindow().validate(email, psw)
        if validation_status:
            self.sm.current ='verification'
            toast("Success")
        else:
            self.sm.current = 'login'
            #App.get_running_app().root.access_denied = True 
            popup = Popup(title= 'try again',
                          content= Label(text= 'wrong email/password'),
                          size_hint=(None, None), size=(400,400),
                          width = 250, height = 300,
                          auto_dismiss=True )
            popup.open()
    
    def verify_code(self):
        email = str(self.sm.get_screen('create_an_account').ids.new_email.text).strip()
        if email == "":
            email = str(self.sm.get_screen('login').ids.user_email.text).strip()
        mydb = mysql.connect(
			host = "127.0.0.1", 
			user = "root",
			passwd = "Kirgizistan993",
			database = "dbforusers",
            )


        c = mydb.cursor(dictionary=True) 
        vc_query = f"select VerifyCode from students where email = '{email}'"
        c.execute(vc_query)
        vc_records =  c.fetchone() 
        print(vc_records)
        mydb.commit()
        inputted_verfication_code = self.sm.get_screen('verification').ids.user_verification_code.text
        if vc_records['VerifyCode'] == inputted_verfication_code:
            verified_query = f"update students set IsVerified = 1 where Email = '{email}'"
            print(verified_query)
            c = mydb.cursor()
            c.execute(verified_query)
            mydb.commit()
            toast("Verification Successful")
            self.sm.current = "home_page"

    
    """Profile page functions"""

    def update_profile(self):
        """Funktion som skickar den nya profil informationen till update_profile_info som sedan updaterar databasen"""
        student_email = self.sm.get_screen('login').ids.user_email.text
        name = self.sm.get_screen('update_profile_page').ids.edit_user.text
        passw = self.sm.get_screen('update_profile_page').ids.profile_password.text
        conf_passw = self.sm.get_screen('update_profile_page').ids.conf_password.text
        good_course1 = self.sm.get_screen('update_profile_page').ids.good_c1.text
        good_course2 = self.sm.get_screen('update_profile_page').ids.good_c2.text
        good_course3 = self.sm.get_screen('update_profile_page').ids.good_c3.text
        bad_course1 = self.sm.get_screen('update_profile_page').ids.bad_b1.text
        bad_course2 = self.sm.get_screen('update_profile_page').ids.bad_b2.text

        user_id = ProfilePage().get_student_id(student_email) 
        ProfilePage().update_profile_info(user_id, name, passw, conf_passw)
        ProfilePage().update_profile_courses(student_email, good_course1, good_course2, good_course3, bad_course1, bad_course2)
    
    def display_student_name(self): 
        student_email = self.sm.get_screen('login').ids.user_email.text
        student_name = ProfilePage().get_student_name(student_email)
        return student_name
    
    def get_can_courses(self): 
        student_email = self.sm.get_screen('login').ids.user_email.text
        can_course = ProfilePage().get_list_can_courses(student_email)
        #print(can_course)
        return can_course
    
    def get_my_name(self): 
        self.root.get_screen("home_page").ids.my_name.text = str(self.display_student_name())
        course_lst = self.get_can_courses()
        #print(course_lst) 
        self.root.get_screen("home_page").ids.can_c1.text = (course_lst[0])
        self.root.get_screen("home_page").ids.can_c2.text = (course_lst[1])
        self.root.get_screen("home_page").ids.can_c3.text = (course_lst[2])
        self.root.get_screen("home_page").ids.cant_c1.text = (course_lst[3])
        self.root.get_screen("home_page").ids.cant_c2.text = (course_lst[4])
    
    """Search"""
    def display_search_name(self): 
        search_student_name = self.sm.get_screen('home_page').ids.search_profile.text
        #print(search_student_name)
        display_name = SearchPopupMenu().search_student(search_student_name)
        return display_name
    
    def get_search_courses(self): 
        search_student_name = self.sm.get_screen('home_page').ids.search_profile.text
        can_course = SearchPopupMenu().get_search_student_courses(search_student_name)
        #print(can_course)
        return can_course
    
    def display_search_profile(self): 
        self.root.get_screen("search_profile").ids.search_name.text = str(self.display_search_name())
        course_lst = self.get_search_courses()
        #print(course_lst) 
        self.root.get_screen("search_profile").ids.search_can_courses_1.text = (course_lst[0])
        self.root.get_screen("search_profile").ids.search_can_courses_2.text = (course_lst[1])
        self.root.get_screen("search_profile").ids.search_can_courses_3.text = (course_lst[2])
        self.root.get_screen("search_profile").ids.search_cant_courses_1.text = (course_lst[3])
        self.root.get_screen("search_profile").ids.search_cant_courses_2.text = (course_lst[4])


    
    """Chat functions"""

    def change_screen(self, screen):
        '''Change screen using the window manager.'''
        self.sm.current = screen

    def show_theme_picker(self):
        '''Display a dialog window to change app's color and theme.'''
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def create_chat(self, profile):
        '''Get all messages and create a chat screen'''
        self.chat_screen = ChatScreen()
        self.msg_builder(profile, self.chat_screen)
        self.chat_screen.text = profile['name']
        self.chat_screen.image = profile['image']
        self.chat_screen.active = profile['active']
        self.sm.switch_to(self.chat_screen)



    def chatlist_builder(self):
        '''Create a Chat List Item for each user and
        adds it to the Message List'''
        for messages in profiles:
            for message in messages['msg']:
                self.chatitem = ChatListItem()
                self.chatitem.profile = messages
                self.chatitem.friend_name = messages['name']
                self.chatitem.friend_avatar = messages['image']

                lastmessage, time, isRead, sender = message.split(';')
                self.chatitem.mssg = lastmessage
                self.chatitem.timestamp = time
                self.chatitem.isRead = isRead
                self.chatitem.sender = sender
            self.sm.get_screen("msg-screen").ids.chatlist.add_widget(self.chatitem)

    def msg_builder(self, profile, screen):
        '''Create a message bubble for creating chat.'''
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

                print(self.chatmsg.isRead)
    
    """Socket chat
    # We cannot create chat screen with other screens, as it;s init method will start listening
    # for incoming connections, but at this stage connection is not being made yet, so we
    # call this method later
    def create_chat_page(self):
        self.chat_page = ChatPage()
        screen = Screen(name='Chat')
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)


    # Error callback function, used by sockets client
    # Updates info page with an error message, shows message and schedules exit in 10 seconds
    # time.sleep() won't work here - will block Kivy and page with error message won't show up
    def show_error(message):
        chat_app.info_page.update_info(message)
        chat_app.screen_manager.current = 'Info'
        Clock.schedule_once(sys.exit, 10)
    """

class logDataWindow(Screen):
    pass    

if __name__ == '__main__':
    chat_app = MainApp()
    chat_app.run()
