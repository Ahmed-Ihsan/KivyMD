from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from Data_control import *
from kivy.uix.screenmanager import Screen ,ScreenManager

Window.size = (600, 300)

class First_screen(Screen):
    pass

class Seconde_screen(Screen):
    pass

class Three_screen(Screen):
    pass

class ContentNavigationDrawer(BoxLayout):
    pass


Builder.load_string('''
<First_screen>:
    name: 'screen1'
    BoxLayout:
        orientation: 'vertical'
        MDBottomAppBar:
            MDToolbar:
                title: "Login"
                icon: "keyboard-backspace"
                type: "bottom"
                mode: "end"
                
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:Name
            hint_text: "Input User Name"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .8}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:ID
            hint_text: "Input User ID"
            mode: "rectangle"
            icon_left: 'key-variant'
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .5}
    MDRoundFlatIconButton:
        text: "login"
        pos_hint: {'center_x':0.3, 'center_y': .3}
        on_release: app.user_login(ID.text,Name.text)
    MDRoundFlatIconButton:
        text: "sign up"
        pos_hint: {'center_x': .6, 'center_y': .3}
        on_release: app.move('screen2')
    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
<Seconde_screen>:
    name: 'screen2'
    BoxLayout:
        orientation: 'vertical'
        MDBottomAppBar:
            MDToolbar:
                title: "Sign UP"
                icon: "keyboard-backspace"
                type: "bottom"
                mode: "end"
                    
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:Name
            hint_text: "Input User Name"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .8}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:ID
            hint_text: "Input User ID"
            mode: "rectangle"
            icon_left: 'key-variant'
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .5}
    MDRoundFlatIconButton:
        text: "Sign up"
        pos_hint: {'center_x':0.3, 'center_y': .3}
        on_release: app.user_sign(ID.text,Name.text)
    MDRoundFlatIconButton:
        text: "login"
        pos_hint: {'center_x': .6, 'center_y': .3}
        on_release: app.move('screen1')
    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
<Three_screen>:
    name: 'screen2'
    BoxLayout:
        orientation: 'vertical'
        MDBottomAppBar:
            MDToolbar:
                title: "Home Page"
                icon: "keyboard-backspace"
                type: "bottom"
                mode: "end"
                    
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:Name
            hint_text: "Input User Name"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .98}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:Name
            hint_text: "Input User Name"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .86}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:Name
            hint_text: "Input User Name"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .74}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:Name
            hint_text: "Input User Name"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .62}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:Name
            hint_text: "Input User Name"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .5}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:ID
            hint_text: "Input User ID"
            mode: "rectangle"
            icon_left: 'key-variant'
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .38}
    MDRoundFlatIconButton:
        text: " Insert"
        pos_hint: {'center_x':0.15, 'center_y': .25}
        on_release: app.user_sign(ID.text,Name.text)
    MDRoundFlatIconButton:
        text: "Delete"
        pos_hint: {'center_x': .38, 'center_y': .25}
        on_release: app.move('screen1')
    MDRoundFlatIconButton:
        text: "Search"
        pos_hint: {'center_x': .61, 'center_y': .25}
        on_release: app.move('screen1')
    MDRoundFlatIconButton:
        text: "Show"
        pos_hint: {'center_x': .84, 'center_y': .25}
        on_release: app.move('screen1')
    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
''')

class Main_app(MDApp):
    sm = ScreenManager()
    def build(self):
        self.sm.add_widget(First_screen(name='screen1'))
        self.sm.add_widget(Seconde_screen(name='screen2'))
        self.sm.add_widget(Three_screen(name='screen3'))
        return self.sm
    
    def user_login(self,*Data):
        if not "" in Data:
            chak = login(Data[1],Data[0])
            if chak :
                Window.size = (700, 500)
                self.sm.current = 'screen3'
            else:
                pass
        else:
            pass
    
    def user_sign(self,*Data):
        if not "" in Data:
            chak = sign(Data[1], Data[0])
            print(chak)
        else:
            pass

    def move(self,screen):
        self.sm.current = screen
        
def Main():
    Main_app().run()

Main()