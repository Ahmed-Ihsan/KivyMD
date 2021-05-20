import kivy
import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from GBS.GBS import location
from AESA.AESA import enc, dec_
from key.RC4 import Rc4_key , decrypt
from HiddenText.image_hidden import hidden, save, reveal


def listToString(s): 
    string_ = ''
    for char in s:
        string_ = string_ + char  
    string_ = string_.replace('\'', '')
    string_ = string_.replace(',', '')
    string_ = string_.replace(']', '')
    string_ = string_.replace('[', '')
    string_ = string_.replace(' ', '')
    return string_

image = None
def send_ (text):
    global image
    le = location()
    print(le[1])

    en = enc(le[1])
    res = json.loads(en)
    print("AES: ",res)
    rc4 = Rc4_key(res['iv'], text, True)
    print('RC4: '+rc4)

    arr=[]
    for i in reversed(res['iv']):
        arr.append(i)

    res_ = listToString(arr)
    #print(res)

    string_ = str(rc4) + res_ +'=='+res['ciphertext']
    print(string_)

    image = hidden('HiddenText/NO2_adam.png',string_)
    
    return 0

def save_(a1 =1):
    global image
    print('save image')
    save('HiddenText/Test_gray1.png',image)
    return 0

def read(a1 =1):

    le = location()
    print(le[1])

    rc4 = reveal('HiddenText/Test_gray1.png')
    print("read from image: ", rc4)

    rc4=listToString(rc4)
    rc4 = rc4.split('==')
    print(rc4)
    
    arr=[]
    for i in reversed(rc4[1]):
        arr.append(i)
    res = listToString(arr)
    #print(res)

    dic_ = {'iv':res+'==', 'ciphertext':rc4[2]}
    print(dic_)
    x= dec_(dic_)

    text = decrypt(res+"==" , rc4[0] )
    print(text)

    return 0


class ConnectPage(GridLayout):
    
    def __init__(self, **kwargs):
        super(ConnectPage, self).__init__(**kwargs)
        self.add_widget(Label(text='text'))
        self.text = TextInput(multiline=False)  
        self.add_widget(self.text)

        self.cols = 1

        self.send = Button(text="send")
        self.send.bind(on_press=self.send_class)  
        self.add_widget(self.send)

        self.save = Button(text="save")
        self.save.bind(on_press=save_)  
        self.add_widget(self.save)

        self.read = Button(text="read")
        self.read.bind(on_press=read)  
        self.add_widget(self.read)

    def send_class(self,instaance):
        send_(self.text.text)

class MyApp(App):
    def build(self):
        return ConnectPage()

if __name__ == '__main__':
    MyApp().run()