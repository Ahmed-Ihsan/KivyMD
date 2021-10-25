import kivy.app
import kivy.uix.label
import kivy.uix.button
import kivy.uix.textinput
import kivy.uix.boxlayout
import arabic_reshaper
import bidi.algorithm
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, StringProperty

class Ar_text(TextInput):
    max_chars = NumericProperty(20)  # maximum character allowed
    str = StringProperty()

    def __init__(self, **kwargs):
        super(Ar_text, self).__init__(**kwargs)
        self.text = bidi.algorithm.get_display(arabic_reshaper.reshape("اطبع شيئاً"))

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return

        self.str = self.str+substring
        self.text = bidi.algorithm.get_display(arabic_reshaper.reshape(self.str))
        substring = ""
        super(Ar_text, self).insert_text(substring, from_undo)
        print("A")

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str)-1]
        self.text = bidi.algorithm.get_display(arabic_reshaper.reshape(self.str))
        print("B")

class TestApp(kivy.app.App):
    def build(self):
        reshaped_text = arabic_reshaper.reshape("بسم اللَّه")
        bidi_text = bidi.algorithm.get_display(reshaped_text)
        label = kivy.uix.label.Label(text=bidi_text, font_name="font/arial")
        textInput = Ar_text(text=bidi_text, font_name="font/arial")
        button = kivy.uix.button.Button(text=bidi_text, font_name="font/arial")

        boxLayout = kivy.uix.boxlayout.BoxLayout(orientation="vertical")
        boxLayout.add_widget(label)
        boxLayout.add_widget(textInput)
        boxLayout.add_widget(button)
        return boxLayout

testApp = TestApp()
testApp.run()