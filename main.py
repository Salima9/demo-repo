from kivymd.app import MDApp
from kivy.lang import Builder
from unicodedata import name
import kivy
kivy.require('1.0.8')
from kivymd.uix.list import IconRightWidget, ThreeLineAvatarIconListItem
import mysql.connector as mysql
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from  kivy.uix.floatlayout import FloatLayout

class Notifications(ScreenManager): 
    def invalid_input(self):
        toast("Incorrect password or username", duration=2)

    def account_created(self):
        toast("You are now a member of Student Market", duration=2)

    def already_exisiting(self):
        toast("A user with this username exists already", duration=3)
 
class LoginWindow():
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self, email, password):
        mydb = mysql.connect(
			host = "127.0.0.1", 
			user = "root",
			passwd = "Kirgizistan993",
			database = "dbforusers",
            )

		# Create A Cursor
        c = mydb.cursor() 
        try: 
            password_variable = f"SELECT Password FROM Studenrs WHERE Email = '{email}'"
            c.execute(password_variable)
            password_query = c.fetchone()
            mydb.commit()
            if password == password_query.get('Password'):
                self.reset()
                return True


            else:
                mydb.close()
                Notifications().invalid_input()
                return False
        except:
            pass
    

    def reset(self):
        self.email = ""
        self.password = ""

class CreateAccountWindow(): 
    first_n = StringProperty(None)
    last_n = StringProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def __init__(self, name, first_n, last_n, email, password): 
        self.name = name
        self.first_n = first_n
        self.last_n = last_n
        self.email = email
        self.password = password
        
       
    
    def register(self): 
        # Create Database Or Connect To One
		#conn = sqlite3.connect('users.db')
		
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
                #split_name = self.name.split()
                #first_n = split_name[0]
                #last_n = split_name[1]
                sql_query_1 = "insert into students (StudentName, FirstName, LastName, Email, Password) values (%s, %s, %s, %s, %s)"
                c.execute(sql_query_1, (self.name, self.first_n, self.last_n, self.email, self.password)) 
                mydb.commit()
                Notifications().account_created()
                self.reset()
                #sm.current = "login"
        else: 
            mydb.close()
            Notifications().already_exisiting()
        
    def login(self):
        self.reset()
        #sm.current = "login"

    def reset(self):
        self.email = ""
        self.password = ""
        self.name = ""



class MainApp(MDApp):
    """Klass för själva appen."""

    def build(self):
        """Build funktion som initierar samtliga filer"""
        self.sm = ScreenManager()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        #self.sm.add_widget(Builder.load_file('first_page.kv'))
        self.sm.add_widget(Builder.load_file('login-page.kv'))
        self.sm.add_widget(Builder.load_file('myy.kv'))
        self.sm.add_widget(Builder.load_file('home_page.kv'))
       

        return self.sm

    def account_labels(self):
        """Skapar ett objekt av klassen User med samtliga inparametrar"""
        name = self.sm.get_screen("create_account").ids.created_user.text

        first_n = self.sm.get_screen("create_account").ids.created_fisrt_n.text
        last_n = self.sm.get_screen("create_account").ids.created_last_n.text

        password = self.sm.get_screen("create_account").ids.created_password.text
        email = self.sm.get_screen("create_account").ids.Email.text
        CreateAccountWindow(name, first_n, last_n, email, password).register()


    def get_name(self):
        return self.sm.get_screen("login").ids.user_name.text

    def get_email(self):
        return self.sm.get_screen("login").ids.user_email.text

    def get_password(self):
        return self.sm.get_screen("login").ids.user_password.text
    
    def login_input(self):
        """Funktion som hanterar login. Samt sätter användarens information på Profil skärmen"""
        old_name = self.get_name()
        valid = LoginWindow().validate(self.get_email(), self.get_password())
        if valid:
            self.root.current = 'home_page'
            self.sm.get_screen('home_page').ids.profile_name.text = old_name
            self.sm.get_screen('home_page').ids.edit_user.text = old_name
            self.sm.get_screen('home_page').ids.profile_password.text = self.get_password()


        else:
            self.reset()
            Notifications().invalid_input()


if __name__ == '__main__':
    MainApp().run()
