from kivymd.app import MDApp
from kivy.lang import Builder
import kivy
import mysql.connector as mysql
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from  kivymd.uix.floatlayout import MDFloatLayout
from  kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.picker import MDThemePicker
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import OneLineAvatarIconListItem
from demo.demo import profiles
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import re
kivy.require('1.9.0')
from  kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
import re
import random, string

"""Database"""
MYSQL_USER =  'root' #USER-NAME
MYSQL_PASS =  'Kirgizistan993' #MYSQL_PASS
MYSQL_DATABASE = 'dbforusers'#DATABASE_NAME

mydb = mysql.connect(user=MYSQL_USER,passwd=MYSQL_PASS,database=MYSQL_DATABASE, host='127.0.0.1')

c = mydb.cursor(dictionary=True)

from db_creds import *
from mail_sender import *

SM = None
"""Main classes"""
class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validatee(self, email, password):
        mydb = mysql.connect(
			host = "127.0.0.1", 
			user = "root",
			passwd = "Kirgizistan993",
			database = "dbforusers",
            )

        c = mydb.cursor(dictionary=True) 
        psw_query = f"select Password, IsVerified from students where email = '{email}'"
        c.execute(psw_query)
        psw_records =  c.fetchone() 
        print(psw_records)
        mydb.commit()
        while password == psw_records['Password']:
            if psw_records['IsVerified'] == 1:
                SM.current = "home_page"
                SM.transition.direction = "up"
                toast("Login Successful!")
                
            else:
                toast("Please verify your email first!")
                SM.current = "verification"
                
        else:
            toast("Wrong email or password!")
            return False 
    

# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()
  
# class to build GUI for a popup window
class P(FloatLayout):
    pass
  
# function that displays the content
def popFun():
    show = P()
    window = Popup(title = "Fel", content = show, width = 2.5, height = 3,
                   size_hint = (None, None), size = (300, 300))
    window.open()

class login_page (BoxLayout):
    access_denied = BooleanProperty(True)


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self, email, password):
        mydb = mysql.connect(
			host = "127.0.0.1", 
			user = "root",
			passwd = "Kirgizistan993",
			database = "dbforusers",
            )

        c = mydb.cursor() 
        
        email_quary = f"select email from students"
        c.execute(email_quary)
        email_records =  c.fetchall() 
        mydb.commit()
        email_lst = list(x for i in email_records for x in i)
        
        
        psw_query = f"select Password, email from students"
        c.execute(psw_query)
        psw_records =  c.fetchall() 
        mydb.commit()
       
        psw_dct = dict((Email, Password) for Password, Email in psw_records)
        
        while email in email_lst:
            try:
                if psw_dct[email] == password:
                    return True
                else:
                    return False
            except KeyError:
                continue
            break

    

class VerificationPage(Screen):
    pass



class ProfileCard(MDFloatLayout, FakeRectangularElevationBehavior): 
    """For the design of the profile page """
    pass   
class ProfilePage(): 
    """This class connects with the database and gets student info"""
    def get_student_id(self, email):
        mydb = mysql.connect(
        host = "127.0.0.1", 
        user = "root",
        passwd = "Kirgizistan993",
        database = "dbforusers",
        )

		# Create A Cursor
        c = mydb.cursor()
        """Gets student id from the database"""
        studnet_id = f"select StudentId from students where Email = '{email}'"
        c.execute(studnet_id)
        result = c.fetchone()
        mydb.commit()
        result2 = result[0]

        return result2
    
    def get_student_name(self, email): 
        mydb = mysql.connect(
        host = "127.0.0.1", 
        user = "root",
        passwd = "Kirgizistan993",
        database = "dbforusers",
        )

		# Create A Cursor
        c = mydb.cursor()
        """Gets student name from the database"""
        studnet_name = f"select StudentName from students where Email = '{email}'"
        c.execute(studnet_name)
        result = c.fetchone()
        mydb.commit()
        student_name = result[0]

        return student_name
    
    def get_list_can_courses(self, email):
        """Gets a list of courses that studnet is good at from the database"""

        courses = f"select CanCourse_1, CanCourse_2, CanCourse_3  from courses where Email = '{email}'"
        c.execute(courses)
        result = c.fetchall()
        mydb.commit()
        can_course_lst = [item for t in result for item in t]
        print(can_course_lst)
        return can_course_lst
          



    def update_profile_info(self, id, new_name, passw, conf_passw):
        mydb = mysql.connect(
        host = "127.0.0.1", 
        user = "root",
        passwd = "Kirgizistan993",
        database = "dbforusers",
        )

		# Create A Cursor
        c = mydb.cursor()
        """Updates profile info. Checks the password"""
        if passw != "" and conf_passw != "" and passw == conf_passw and len(passw) >= 6 and re.search(r"\d", passw)  and re.search(r"[A-Z]", passw) and re.search(r"[a-z]", passw) :

            c.execute(f"SET SQL_SAFE_UPDATES = 0")
            update = f"UPDATE  Students SET StudentName = '{new_name}', Password ='{passw}' where StudentID = {id}"
            
            c.execute(update)
            mydb.commit()
            print(id, new_name, passw, conf_passw )
        else: 
            toast("Please check the password")

    def update_profile_courses(self, email, good_c1, good_c2, good_c3, bad_c1, bad_c2):
        mydb = mysql.connect(
        host = "127.0.0.1", 
        user = "root",
        passwd = "Kirgizistan993",
        database = "dbforusers",
        )

		# Create A Cursor
        c = mydb.cursor()

        """Updates courses"""
        c.execute(f"SET SQL_SAFE_UPDATES = 0")
    
        update_course = f"UPDATE  courses SET CanCourse_1 = '{good_c1}', CanCourse_2 = '{good_c2}', CanCourse_3 = '{good_c3}', NeedCourse_1 = '{bad_c1}', NeedCourse_2 = '{bad_c2}' where Email = '{email}'"
        c.execute(update_course)
        mydb.commit()
        print(good_c1, good_c2, good_c3, bad_c1, bad_c2 )

 
class NavBar(FakeRectangularElevationBehavior, MDFloatLayout): 
    """class for a bottom nav bar"""
    pass



class MessageScreen(Screen):
    '''A screen that display the story fleets and all message histories.'''


class ChatScreen(Screen):
    '''A screen that display messages with a user.'''

    text = StringProperty()
    image = ObjectProperty()
    active = BooleanProperty(defaultvalue=False)



class ChatListItem(MDCard):
    '''A clickable chat item for the chat timeline.'''

    isRead = OptionProperty(None, options=['delivered', 'read', 'new', 'waiting'])
    friend_name = StringProperty()
    mssg = StringProperty()
    timestamp = StringProperty()
    friend_avatar = StringProperty()
    profile = DictProperty()


class ChatBubble(MDBoxLayout):
    '''A chat bubble for the chat screen messages.'''

    profile = DictProperty()
    msg = StringProperty()
    time = StringProperty()
    sender = StringProperty()
    isRead = OptionProperty('waiting', options=['read', 'delivered', 'waiting'])


class Message(MDLabel):
    '''A adaptive text for the chat bubble.'''



