from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import json
from GBS.GBS import location
from AESA.AESA import enc, dec_d
from key.RC4 import Rc4_key , decrypt
from HiddenText.image_hidden import hidden, save, reveal

image = None
path_ = ''
def listToString(s): 
    string_ = ''
    for char in s:
        string_ = string_ + char  
    string_ = string_.replace('\'', '')
    string_ = string_.replace(',', '')
    string_ = string_.replace(']', '')
    string_ = string_.replace('[', '')
    string_ = string_.replace(' ', '')
    return string_

def str_path(path):
    path = path.replace('\\', "\\\\")
    return path

def send_ (text):
    global image, path_
    le = location()
    print(le[1])
    en = enc(text,str(le[1][0]) + str(le[1][1]))
    res = json.loads(en)
    print("AES: ",res)

    rc4 = Rc4_key(res['iv'], text, True)
    print('RC4: '+rc4)

    arr=[]
    for i in reversed(res['iv']):
        arr.append(i)

    res_ = listToString(arr)
    #print(res)

    string_ = str(rc4) + res_ +'=='+res['ciphertext']
    print(string_)
    print(path_)
    #path = json.loads(str_path(path))
    image = hidden(path_,string_)
    
    return 0

def save_():
    global image , path_
    print('save image')
    save(path_,image)
    return 0

def read():
    global path_
    le = location()
    print(le[1])

    rc4 = reveal(path_)
    print("read from image: ", rc4)

    rc4=listToString(rc4)
    rc4 = rc4.split('==')
    print(rc4)
    
    arr=[]
    for i in reversed(rc4[1]):
        arr.append(i)
    res = listToString(arr)
    #print(res)

    dic_ = {'iv':res+'==', 'ciphertext':rc4[2]}
    print(dic_)
    x= dec_d(dic_ , rc4[2])
    print(x)
    text = decrypt(res+"==" , rc4[0] )
    print(text)

    return 0

KV = '''
Screen:
    ScreenManager:
        Screen:
            BoxLayout:
                orientation: 'vertical'
                MDBottomAppBar:
                    MDToolbar:
                        title: "Title"
                        icon: "keyboard-backspace"
                        type: "bottom"
                        mode: "end"
                        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
                        elevation: 10

                FloatLayout:
                    BoxLayout:
                        spacing: dp(10)
                        padding: dp(20)
                        MDIconButton:
                            icon: 'textbox'
                            pos_hint: {'center_y': .9}
                        MDTextField:
                            id: inptext
                            icon_left : 'magnify'
                            hint_text: "Enter Text"
                            helper_text: "one line only"
                            helper_text_mode: "on_focus"
                            pos_hint: {'center_x': .5, 'center_y': .9}
                    MDRoundFlatIconButton:
                        text: "Open manager"
                        icon: "folder"
                        pos_hint: {'center_x': .5, 'center_y': .75}
                        on_release: app.file_manager_open()
                    MDRoundFlatIconButton:
                        text: "Run AES & RC4"
                        icon: "worker"
                        pos_hint: {'center_x': .5, 'center_y': .65}
                        on_release: app.button_(inptext.text)
                    MDRoundFlatIconButton:
                        text: "Save Image"
                        icon: "content-save-outline"
                        pos_hint: {'center_x': .5, 'center_y': .55}
                        on_release: app.save_images()
                    MDRoundFlatIconButton:
                        text: "Read Image"
                        icon: "read"
                        pos_hint: {'center_x': .5, 'center_y': .45}
                        on_release: app.read_text()  
                    MDRoundFlatIconButton:
                        text: "Send Image"
                        icon: "send"
                        pos_hint: {'center_x': .5, 'center_y': .35}
                        on_release: app.file_manager_open()             

            MDNavigationDrawer:
                id: nav_drawer

                ContentNavigationDrawer:
'''

class ContentNavigationDrawer(BoxLayout):
    pass

class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            previous=True,
        )

    def build(self):
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show('.\\')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)
        global path_
        path_ = path
        print(path_)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()
    
    def button_(self,te):
        send_ (te)

    def save_images(self):
        save_()

    def read_text(self):
        read()

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


Example().run()