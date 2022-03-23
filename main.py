from kivymd.app import MDApp
from kivy.lang import Builder
import kivy
kivy.require('1.0.8')
from kivymd.uix.list import IconRightWidget, ThreeLineAvatarIconListItem
import mysql.connector as mysql
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from  kivy.uix.floatlayout import FloatLayout

class Notifications(): 
    def input_is_invalid(self):
        toast("Incorrect email or password", duration=6)

    def successfully_verified (self):
        toast("Your account is created ", duration=5)
    
    def successfully_loged_in(self): 
        toast("Successfully loged in", duration=5)

    
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
    name = ObjectProperty(None)
    first_n = ObjectProperty(None)
    last_n = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def __init__(self, name, first_n, last_n, email, password): 
        self.name = name
        self.first_n = first_n
        self.last_n = last_n
        self.email = email
        self.password = password
    
    
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
        if self.name != "" and self.email != "" and self.email.count("@") == 1 and self.email.count(".") > 0:
            if self.password != "":
                sql_query_1 = "insert into students (StudentName, FirstName, LastName, Email, Password) values (%s, %s, %s, %s, %s)"
                c.execute(sql_query_1, (self.name, self.first_n, self.last_n, self.email, self.password)) 
                mydb.commit()
                self.reset()
        else: 
            mydb.close()
            Notifications().already_exisiting()
        

    def reset(self):
        self.email = ""
        self.password = ""
        self.name = ""


class MainApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Builder.load_file('login-page.kv'))
        self.sm.add_widget(Builder.load_file('signup_page.kv'))

        return self.sm

    def created_account(self):
        name = self.sm.get_screen("create_account").ids.new_user.text
        first_n = self.sm.get_screen("create_account").ids.new_fisrt_n.text
        last_n = self.sm.get_screen("create_account").ids.new_last_n.text
        password = self.sm.get_screen("create_account").ids.new_password.text
        email = self.sm.get_screen("create_account").ids.new_email.text
        CreateAccountWindow(name, first_n, last_n, email, password).register()

    def login_valid(self):
        email = self.sm.get_screen("login").ids.user_email.text
        psw = self.sm.get_screen("login").ids.user_password.text
        validation_status = LoginWindow().validate(email, psw)
        if validation_status:
            Notifications().successfully_loged_in()
        else: 
            Notifications().input_is_invalid()

        
    
        


if __name__ == '__main__':
    MainApp().run()
