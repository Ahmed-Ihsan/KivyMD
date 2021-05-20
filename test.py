from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import json
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from GBS.GBS import location
from AESA.AESA import enc, dec_
from key.RC4 import Rc4_key , decrypt
from HiddenText.image_hidden import hidden, save, reveal

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
                            icon: 'magnify'
                            pos_hint: {'center_y': .9}
                        MDTextField:
                            icon_left : 'magnify'
                            hint_text: "Enter Text"
                            helper_text: "one line only"
                            helper_text_mode: "on_focus"
                            on_text: root.set_list_md_icons(self.text, True)
                            pos_hint: {'center_x': .5, 'center_y': .9}

                    MDRoundFlatIconButton:
                        text: "Open manager"
                        icon: "folder"
                        pos_hint: {'center_x': .5, 'center_y': .75}
                        on_release: app.file_manager_open()
                    MDRoundFlatIconButton:
                        text: "Run AES & RC4"
                        icon: "worker"
                        pos_hint: {'center_x': .5, 'center_y': .55}
                        on_release: app.file_manager_open()
                    MDRoundFlatIconButton:
                        text: "Save Image"
                        icon: "content-save-outline"
                        pos_hint: {'center_x': .5, 'center_y': .65}
                        on_release: app.file_manager_open()
                    MDRoundFlatIconButton:
                        text: "Send Image"
                        icon: "send"
                        pos_hint: {'center_x': .5, 'center_y': .45}
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
        print(path)

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