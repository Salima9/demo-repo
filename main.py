import kivy
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

#from kivy.lang import Builder
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')

from kivy.core.window import Window
Window.size = (320, 600)

class WindowManager(ScreenManager):
    '''A window manager to manage switching between screens'''
    
    

class MessageScreen(Screen):
    '''A screen that display the stories and all message histories.'''
    


class MainApp(MDApp):
    def build(self):
        '''Initialize the application and return the root widget'''

        #setting theme properties
        self.theme_cls.theme_style = 'Dark' #Dark theme
        self.theme_cls.primary_palette = 'Teal' #Main color palette
        self.theme_cls.accent_palette = 'Teal' #Second coloe palette with 400 hue value
        self.theme_cls_accent_hue = '400'
        self.title = 'CSC chat'

        #Storing the screens in a list.
        screens = [MessageScreen(name='message')]
        #Adding all screen in screens to the window manager
        
        self.wm = WindowManager(transition=FadeTransition()) #Creating and instance of Window manager and setting the animation when switching 

        for screen in screens:
            self.wm.add_widget(screen)

        #Return the window manager.
        return self.wm 

if __name__=="__main__":
    MainApp().run()



