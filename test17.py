from kivy.lang import Builder

from kivymd.app import MDApp


KV = '''
AnchorLayout:
    canvas:
        Color:
            rgba: app.theme_cls.primary_color
        Rectangle:
            pos: self.pos
            size: self.size
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


MainApp().run()