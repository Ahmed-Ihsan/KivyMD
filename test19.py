from kivy.lang import Builder
from kivymd.app import MDApp


KV = '''
MDBoxLayout:
    adaptive_height: True
    md_bg_color: app.theme_cls.primary_color
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


MainApp().run()