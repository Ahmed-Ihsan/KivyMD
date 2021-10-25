from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
MDBoxLayout:

    MDBoxLayout:
        md_bg_color: app.theme_cls.bg_light

    MDBoxLayout:
        md_bg_color: app.theme_cls.bg_normal

    MDBoxLayout:
        md_bg_color: app.theme_cls.bg_dark

    MDBoxLayout:
        md_bg_color: app.theme_cls.bg_darkest
'''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # "Light"
        # self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


MainApp().run()