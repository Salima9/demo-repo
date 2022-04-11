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

"""Database"""
MYSQL_USER =  'root' #USER-NAME
MYSQL_PASS =  'Kirgizistan993' #MYSQL_PASS
MYSQL_DATABASE = 'dbforusers'#DATABASE_NAME

mydb = mysql.connect(user=MYSQL_USER,passwd=MYSQL_PASS,database=MYSQL_DATABASE, host='127.0.0.1')

c = mydb.cursor(dictionary=True)

"""Main classes"""

class LoginWindow(Screen):
    """User loggar in genom databasen """
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self, email, password):
        """Validate if password is same as in database"""
        psw_query = f"select Password from students where email = '{email}'"
        c.execute(psw_query)
        psw_records =  c.fetchone() 
        mydb.commit()
        if password == psw_records:
            return True

        else:
            return False 
    
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
        email_lst = list(email_records)
        print(email_lst)
         
        if self.email not in email_lst:   
            if self.username != "" and self.email != "" and self.email.count("@") == 1 and self.email.count(".") > 0:
                if self.password != "" and self.confirm_password != "" and self.password != self.confirm_password and len(self.password) >= 6 and re.search(r"\d", self.password)  and re.search(r"[A-Z]", self.password) and re.search(r"[a-z]", self.password) :
                    
                    info_quary = "insert into students (StudentName, Email, Password) values (%s, %s, %s)"
                    c.execute(info_quary, (self.username, self.email, self.password)) 
                    course_quary = "insert into courses (Email, CanCourse_1, CanCourse_2, CanCourse_3, NeedCourse_1, NeedCourse_2 ) values (%s, %s, %s, %s, %s, %s)"
                    c.execute(course_quary, (self.email, self.courses_g1, self.courses_g2, self.courses_g3, self.courses_b1, self.courses_b2)) 
                    mydb.commit()
                    mydb.close()
                else: 
                    if self.password != self.confirm_password: 
                        toast("Password doesnt match")
                    else: 
                        toast("Please check password")
        elif self.email in email_lst:
            toast("Invalid user")

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



