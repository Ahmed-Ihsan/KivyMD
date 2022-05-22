from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        self.theme_cls.primary_hue = "A700"  # "500"
        screen = MDScreen()
        screen.add_widget(
            
            MDRectangleFlatButton(
                text="Hello, World",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            ),

            MDRectangleFlatButton(
                text="ahmed",
                pos_hint={"center_x": 0.7, "center_y": 0.7},
            )
        )
        self.theme_cls.primary_palette = "Red"  # "Purple", "Red"
        self.theme_cls.primary_hue = "A700"  # "500"
        screen.add_widget(
            MDRectangleFlatButton(
                text="ahmed",
                pos_hint={"center_x": 0.7, "center_y": 0.7},
            )
        )
        return screen


MainApp().run()