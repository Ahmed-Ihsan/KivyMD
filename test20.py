from kivy.lang import Builder

from kivymd.app import MDApp


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_string(
            '''
MDBoxLayout:
    MDBottomNavigation:
        
        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Python'
            icon: 'language-python'
            on_tab_touch_down: print("on_tab_touch_down")
            on_tab_touch_move: print("on_tab_touch_move")
            on_tab_touch_up: print("on_tab_touch_up")
            on_tab_press: print("on_tab_press")
            on_tab_release: print("on_tab_release")

            MDLabel:
                text: 'Python'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'C++'
            icon: 'language-cpp'

            MDLabel:
                text: 'I programming of C++'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'JS'
            icon: 'language-javascript'

            MDLabel:
                text: 'JS'
                halign: 'center'
'''
        )


Test().run()
