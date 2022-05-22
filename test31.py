from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivymd.app import MDApp
from kivymd.uix.behaviors import (
    CircularRippleBehavior,
    CircularElevationBehavior,
)

KV = '''
#:import images_path kivymd.images_path


<CircularElevationButton>:
    size_hint: None, None
    size: "100dp", "100dp"
    source: f"{images_path}/kivymd_logo.png"


Screen:

    # With elevation effect
    CircularElevationButton:
        pos_hint: {"center_x": .5, "center_y": .6}
        elevation: 5

    # Without elevation effect
    CircularElevationButton:
        pos_hint: {"center_x": .5, "center_y": .4}
        elevation: 0
'''


class CircularElevationButton(
    CircularRippleBehavior,
    CircularElevationBehavior,
    ButtonBehavior,
    Image,
):
    md_bg_color = [0, 0, 1, 1]


class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)


Example().run()