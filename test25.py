from kivy.factory import Factory
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import HoverBehavior

Builder.load_string('''
#:import MDDropdownMenu kivymd.uix.menu.MDDropdownMenu


<HoverBehaviorExample@Screen>

    MDRaisedButton:
        text: "Open menu"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: MDDropdownMenu(items=app.menu_items, width_mult=4).open(self)
''')


class MenuItem(MDLabel, HoverBehavior):
    '''Custom menu item implementing hover behavior.'''

    def on_enter(self, *args):
        '''The method will be called when the mouse cursor
        is within the borders of the current widget.'''

        self.text_color = [1, 1, 1, 1]

    def on_leave(self, *args):
        '''The method will be called when the mouse cursor goes beyond
        the borders of the current widget.'''

        self.text_color = [0, 0, 0, 1]


class Test(MDApp):
    menu_items = []

    def build(self):
        self.menu_items = [
            {
                "viewclass": "MenuItem",
                "text": "Example item %d" % i,
                "theme_text_color": "Custom",
                "text_color": [0, 0, 0, 1],
                "halign": "center",
            }
            for i in range(5)
        ]
        return Factory.HoverBehaviorExample()


Test().run()