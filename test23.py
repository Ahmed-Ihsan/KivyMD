# code to show how to use StackLayout using .kv file

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# creates the button in kivy
# if not imported shows the error
from kivy.uix.button import Button

# The StackLayout arranges children vertically
# or horizontally, as many as the layout can fit.
from kivy.uix.stacklayout import StackLayout

# creating the root widget used in .kv file
class StackLayout(StackLayout):
	pass

# class in which name .kv file must be named Slider.kv.
# or creating the App class
class StackApp(App):
	def build(self):
		# returning the instance of StackLayout class
		return StackLayout()

# run the app
if __name__=='__main__':
	StackApp().run()
