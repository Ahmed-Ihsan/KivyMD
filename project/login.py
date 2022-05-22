from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from Data_control import *
from kivy.uix.screenmanager import Screen ,ScreenManager
from kivymd.uix.label import MDLabel 
from kivymd.uix.button import MDFloatingActionButton
from kivymd.font_definitions import theme_font_styles

Window.size = (600, 300)

class First_screen(Screen):
    pass

class Seconde_screen(Screen):
    pass

class Three_screen(Screen):
    pass

class Fourth_screen(Screen):
    pass

class Show_screen(Screen):
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
    name: 'screen3'
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
            id:ID
            hint_text: "Input ID"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .98}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:Name
            hint_text: "Input Name"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .86}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:age
            hint_text: "Input age"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .74}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:number
            hint_text: "Input number phone"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .62}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:address
            hint_text: "Input address"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .5}
    BoxLayout:
        padding: dp(20)
        MDTextField:
            id:result
            hint_text: "Input result"
            mode: "rectangle"
            icon_left: 'key-variant'
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_x': .5, 'center_y': .38}
            
    MDRoundFlatIconButton:
        text: " Insert"
        pos_hint: {'center_x':0.15, 'center_y': .25}
        on_release: app.insert(ID.text,Name.text,age.text,number.text,address.text,result.text)
    MDRoundFlatIconButton:
        text: "Edite"
        pos_hint: {'center_x': .38, 'center_y': .25}
        on_release: app.edite_set(ID.text,Name.text,age.text,number.text,address.text,result.text)
    MDRoundFlatIconButton:
        text: "Search"
        pos_hint: {'center_x': .61, 'center_y': .25}
        on_release: app.move('screen4')
    MDRoundFlatIconButton:
        text: "Show"
        pos_hint: {'center_x': .84, 'center_y': .25}
        on_release: app.show()
    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:

<Fourth_screen>:
    name: 'screen4'
    BoxLayout: 
        padding: dp(20)
        MDTextField:
            id:search
            hint_text: "Input Text"
            mode: "rectangle"
            fill_color: 0, 0, 200, .4
            pos_hint: {'center_y': .95}

    MDRoundFlatIconButton:
        text: "Search"
        pos_hint: {'center_x': .6,'center_y': .8}
        on_release: on_release: app.search(box , search.text)
    MDRoundFlatIconButton:
        text: "Back"
        pos_hint: {'center_x': .3,'center_y': .8}
        on_release: on_release: app.move('screen3')

    ScrollView:
        pos_hint: {'center_x': .8, 'center_y': .25}
        MDList:
            id:box
            
<Show_screen>:
    name: 'screen5'
    MDRoundFlatIconButton:
        text: "Back"
        pos_hint: {'center_x': .3,'center_y': .9}
        on_release: on_release: app.move('screen3')
    ScrollView:
        pos_hint: {'center_x': .7, 'center_y': .25}
        MDList:
            id:box2
           
''')

class Main_app(MDApp):
    sm = ScreenManager()
    def build(self):
        self.sm.add_widget(First_screen(name='screen1'))
        self.sm.add_widget(Seconde_screen(name='screen2'))
        self.sm.add_widget(Three_screen(name='screen3'))
        self.sm.add_widget(Fourth_screen(name='screen4'))
        self.sm.add_widget(Show_screen(name='screen5'))
        return self.sm
    
    def user_login(self,*Data):
        if not "" in Data:
            check = login(Data[1],Data[0])
            print(check)
            if check :
                Window.size = (700, 500)
                self.sm.current = 'screen3'
            else:
                pass
        else:
            pass
    
    def user_sign(self,*Data):
        if not "" in Data:
            check = sign(Data[1], Data[0])
            print(check)
        else:
            pass

    def move(self,screen):
        self.sm.current = screen
        

    def insert(self,*Data):
        if not "" in Data:
           check = add(Data[0], Data[1], Data[2], Data[3], Data[4], Data[5])
           print(check)
        else:
            print('13A')
    
    def search(self,box,sch):
        sch = sch.split(":")
        if len(sch)> 1:
            res = search(sch[0],sch[1]).values
            print(res)
        else:
            res = search(None , sch).values
        for val in res:
            box.add_widget(
                MDLabel(
                    text=f'''ID  : {val[0]} || Name : {val[1]} || Age : {val[3]} || Number Phone : {val[1]} 
                Adress  : {val[1]} || result : {val[1]}
________________________________________________________
                    '''
                )
            )
    def show(self):
        self.sm.current = "screen5"
        box = self.sm.get_screen("screen5").ids.box2
        reslt = show_data().values
        reslt = reslt[::-1]
        for val in reslt:
            box.add_widget(
                MDLabel(
                    text=f'''ID  : {val[0]} || Name : {val[1]} || Age : {val[3]} || Number Phone : {val[1]} 
                Adress  : {val[1]} || result : {val[1]}
________________________________________________________
                    '''
                )
                
            )
           
    def remove_item(self,data):
        print(remove_data(data))
    
    def edite_set(self,*Data):
        if not "" in Data:
            check = edite(Data[0], Data[1], Data[2], Data[3], Data[4], Data[5])
            print(check)
        else:
            print('13M')

def Main():
    Main_app().run()

Main()
