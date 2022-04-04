import email
from tkinter import Label
from kivymd.app import MDApp
from kivy.lang import Builder
import kivy
from matplotlib.pyplot import text
#kivy.require('1.0.8')
from kivymd.uix.list import IconRightWidget, ThreeLineAvatarIconListItem
import mysql.connector as mysql
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from  kivymd.uix.floatlayout import MDFloatLayout
from  kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.core.text import LabelBase
import re

import kivy
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')

from kivy.core.window import Window
Window.size = (310, 580)

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

        c = mydb.cursor(dictionary=True) 
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
    pass   
class ProfilePage(): 
    
    
    def get_student_id(self, email):
        mydb = mysql.connect(
			host = "127.0.0.1", 
			user = "root",
			passwd = "Kirgizistan993",
			database = "dbforusers",
            )

		# Create A Cursor
        c = mydb.cursor()
        """Hämtar användarens ID från databasen"""
        studnet_id = f"select StudentId from students where Email = '{email}'"
        c.execute(studnet_id)
        result = c.fetchone()
        mydb.commit()
        result2 = result[0]

        return result2

    def update_profile_info(self, id, new_name, passw, conf_passw):
        
        mydb = mysql.connect(
			host = "127.0.0.1", 
			user = "root",
			passwd = "Kirgizistan993",
			database = "dbforusers",
            )

		# Create A Cursor
        c = mydb.cursor()
        if passw != "" and conf_passw != "" and passw == conf_passw and len(passw) >= 6 and re.search(r"\d", passw)  and re.search(r"[A-Z]", passw) and re.search(r"[a-z]", passw) :

            """Uppdaterar användarens profil vid begäran"""
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
        """Uppdaterar användarens profil vid begäran"""
        c.execute(f"SET SQL_SAFE_UPDATES = 0")
    
        update_course = f"UPDATE  courses SET CanCourse_1 = '{good_c1}', CanCourse_2 = '{good_c2}', CanCourse_3 = '{good_c3}', NeedCourse_1 = '{bad_c1}', NeedCourse_2 = '{bad_c2}' where Email = '{email}'"
        c.execute(update_course)
        mydb.commit()
        print(good_c1, good_c2, good_c3, bad_c1, bad_c2 )

 




class MainApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Builder.load_file('login-page.kv'))
        self.sm.add_widget(Builder.load_file('sign_up2.kv'))
        #self.sm.add_widget(Builder.load_file('navbar.kv'))
        self.sm.add_widget(Builder.load_file('navbar2.kv'))
        self.sm.add_widget(Builder.load_file('profile_page.kv'))



        return self.sm

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

        CreateAccountWindow(name, email, password, confirm_password, courses_g1, courses_g2, courses_g3, courses_b1, courses_b2).register()

    def login_valid(self):
        email = self.sm.get_screen("login").ids.user_email.text
        psw = self.sm.get_screen("login").ids.user_password.text
        validation_status = LoginWindow().validate(email, psw)
        if validation_status:
            toast("success")
        else: 
            toast("invalid")
    

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

    

    
    
    
   
        
    
        


if __name__ == '__main__':
    #LabelBase.register(name = "MPoppins", fn_regular = "C:\Users\omurb\OneDrive\Dokument\python3\demo-repo\fonts\Poppins\Poppins""-Medium.ttf")
    #LabelBase.register(name = "BPoppins", fn_regular="C:\Users\omurb\OneDrive\Dokument\python3\demo-repo\fonts\Poppins\Poppins""-Bold.ttf")
    MainApp().run()
