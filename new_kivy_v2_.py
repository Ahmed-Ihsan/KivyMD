from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen ,ScreenManager
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.core.window import Window
import json
import codecs
import string
from plyer import storagepath , gps
import time
import geocoder
from base64 import b64encode
from Crypto.Cipher import AES
from base64 import b64decode
from stegano import tools
from typing import IO, Union

Window.size = (350,600)

def hide(
    input_image: Union[str, IO[bytes]],
    message: str,
    encoding: str = "UTF-8",
    shift: int = 0,
    auto_convert_rgb: bool = False,
    Gps_ : int = 0,
):
    """Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    message_length = len(message)
    assert message_length != 0, "message length is zero"

    img = tools.open_image(input_image)
    
    if img.mode not in ["RGB", "RGBA"]:
        if not auto_convert_rgb:
            print("The mode of the image is not RGB. Mode is {}".format(img.mode))
            answer = input("Convert the image to RGB ? [Y / n]\n") or "Y"
            if answer.lower() == "n":
                raise Exception("Not a RGB image.")
        img = img.convert("RGB")
    encoded = img.copy()

    width, height = img.size
    index = 0

    message = str(message_length) + ":" + str(message)
    message_bits = "".join(tools.a2bits_list(message, encoding))
    message_bits += "0" * ((3 - (len(message_bits) % 3)) % 3)

    npixels = width * height
    len_message_bits = len(message_bits)
    if len_message_bits > npixels * 3:
        raise Exception(
            "The message you want to hide is too long: {}".format(message_length)
        )
    for row in range(height):
        for col in range(width):
            if shift != 0:
                shift -= 1
                continue
            if index + 3 <= len_message_bits:

                # Get the colour component.
                pixel = img.getpixel((col , row ))

                r = pixel[0]+Gps_%2
                g = pixel[1]+Gps_%3
                b = pixel[2]+1

                # Change the Least Significant Bit of each colour component.
                r = tools.setlsb(r, message_bits[index])
                g = tools.setlsb(g, message_bits[index + 1])
                b = tools.setlsb(b, message_bits[index + 2])

                # Save the new pixel
                if img.mode == "RGBA":
                    encoded.putpixel((col, row), (r, g, b, pixel[3]))
                else:
                    encoded.putpixel((col, row), (r, g, b))

                index += 3
            else:
                img.close()
                return encoded

def reveal(input_image: Union[str, IO[bytes]], encoding: str = "UTF-8", shift: int = 0,Gps_: int = 0):
    """Find a message in an image (with the LSB technique).
    """
    img = tools.open_image(input_image)

    width, height = img.size
    buff, count = 0, 0
    bitab = []
    limit = None
    for row in range(height):
        for col in range(width):
            if shift != 0:
                shift -= 1
                continue
            # pixel = [r, g, b] or [r,g,b,a]

            try:
                pixel = img.getpixel((col + Gps_, row + Gps_))
            except:
                pixel = img.getpixel((col , row ))

            if img.mode == "RGBA":
                pixel = pixel[:3]  # ignore the alpha
            for color in pixel:
                buff += (color & 1) << (tools.ENCODINGS[encoding] - 1 - count)
                count += 1
                if count == tools.ENCODINGS[encoding]:
                    bitab.append(chr(buff))
                    buff, count = 0, 0
                    if bitab[-1] == ":" and limit is None:
                        try:
                            limit = int("".join(bitab[:-1]))
                        except Exception:
                            pass

            if len(bitab) - len(str(limit)) - 1 == limit:
                img.close()
                return "".join(bitab)[len(str(limit)) + 1:]

def hidden(path,text,num):
    secret = hide(path,str(text),shift=2 ,Gps_= num)
    return secret

def save(path ,image):
    image.save(path)

def reveal_(path ):
    msg= reveal(path,shift=2)
    return msg

def enc(data):
    x = data.replace(".", "1")
    x = str(len(x + x)*len(x)) + x
    x = data.replace("1", str(len(x)))
    x = data.replace(".", str(len(x)))
    x = int(x)*int(x)
    data = data.encode('utf-8')
    key = b'\xea`{-\xe8*\x9e\xe3\xfe\xe7\xf1}\x17}\x9cL'
    cipher = AES.new(key, AES.MODE_CFB)
    ct_bytes = cipher.encrypt(data)
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv':iv, 'ciphertext':ct})
    return result

def dec_d(result):
    try:
        #b64 = json.loads(result)
        b64 = result
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        key = b'\xea`{-\xe8*\x9e\xe3\xfe\xe7\xf1}\x17}\x9cL'
        #key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        pt = cipher.decrypt(ct)
        return pt
    except ValueError:
        print("Incorrect decryption")

def location():
    g = geocoder.ip('me')
    return g, g.latlng

MOD = 256

def KSA(key):
    ''' Key Scheduling Algorithm (from wikipedia):
        for i from 0 to 255
            S[i] := i
        endfor
        j := 0
        for i from 0 to 255
            j := (j + S[i] + key[i mod keylength]) mod 256
            swap values of S[i] and S[j]
        endfor
    '''
    key_length = len(key)
    # create the array "S"
    S = list(range(MOD))  # [0,1,2, ... , 255]
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values

    return S


def PRGA(S):
    ''' Psudo Random Generation Algorithm (from wikipedia):
        i := 0
        j := 0
        while GeneratingOutput:
            i := (i + 1) mod 256
            j := (j + S[i]) mod 256
            swap values of S[i] and S[j]
            K := S[(S[i] + S[j]) mod 256]
            output K
        endwhile
    '''
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % MOD]
        yield K


def get_keystream(key):
    ''' Takes the encryption key to get the keystream using PRGA
        return object is a generator
    '''
    S = KSA(key)
    return PRGA(S)


def encrypt_logic(key, text):
    ''' :key -> encryption key used for encrypting, as hex string
        :text -> array of unicode values/ byte string to encrpyt/decrypt
    '''
    # For plaintext key, use this
    key = [ord(c) for c in key]
    # If key is in hex:
    # key = codecs.decode(key, 'hex_codec')
    # key = [c for c in key]
    keystream = get_keystream(key)

    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
        res.append(val)
    return ''.join(res)


def encrypt(key, plaintext):
    ''' :key -> encryption key used for encrypting, as hex string
        :plaintext -> plaintext string to encrpyt
    '''
    plaintext = [ord(c) for c in plaintext]
    return encrypt_logic(key, plaintext)


def decrypt(key, ciphertext):
    ''' :key -> encryption key used for encrypting, as hex string
        :ciphertext -> hex encoded ciphered text using RC4
    '''
    ciphertext = codecs.decode(ciphertext, 'hex_codec')
    res = encrypt_logic(key, ciphertext)
    return codecs.decode(res, 'hex_codec').decode('utf-8')


def Rc4_key(key, text, cipher = 0):
    alphabet = string.ascii_letters + string.digits

    #print(key)
    #key = 'not-so-random-key'  # plaintext
    plaintext = text  # plaintext
    # encrypt the plaintext, using key and RC4 algorithm
    ciphertext = encrypt(key, plaintext)
    '''print('plaintext:', plaintext)
    print('ciphertext :', ciphertext)'''
    # ..
    # Let's check the implementation
    # ..
    #ciphertext = '2D7FEE79FFCE80B7DDB7BDA5A7F878CE298615476F86F3B890FD4746BE2D8F741395F884B4A35CE979'

    # change ciphertext to string again
    decrypted =" "
    try:
        decrypted = decrypt(key, text)
    except:
        pass
    #print('decrypted:', decrypted)

    if cipher:
        #print('\nCongrats ! You made it.')
        return ciphertext
    elif not cipher :
        return decrypted
    else:
        pass

class First_screen(Screen):
    pass

class Seconde_screen(Screen):
    pass

class WindowsManager(ScreenManager):
    pass

class ContentNavigationDrawer(BoxLayout):
    pass

class Camare_screen(Screen):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png(storagepath.get_home_dir()+"/IMG_{}.png".format(timestr))
        print("Captured")

kv = '''
WindowsManager:
    First_screen:
    Seconde_screen:
    Camare_screen:

<First_screen>:
    name:'first_logo'
    Image:
        source: "logo2-01.jpg"
        size: self.texture_size
        pos_hint: { 'center_y': .75}
    MDRoundFlatIconButton:
        text: "New massage"
        icon: "email-newsletter"
        pos_hint: {'center_x': .5, 'center_y': .4}
        on_release: app.root.current = 'AES_rc4'
    MDRoundFlatIconButton:
        text: "Camera"
        icon: "camera"
        pos_hint: {'center_x': .5, 'center_y': .3}
        on_release: app.root.current = 'seconde'
    MDBottomAppBar:
        MDToolbar:
            title: "Title"
            icon: "git"
            type: "bottom"
            left_action_items: [["menu", lambda x: x]]
            mode: "end"

<Seconde_screen>:
    name:'AES_rc4'
    Screen:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDBottomAppBar:
                        MDToolbar:
                            title: "Title"
                            icon: "git"
                            type: "bottom"
                            mode: "end"
                            left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
                            elevation: 10

                    FloatLayout:
                        BoxLayout:
                            MDIconButton:
                                icon: 'textbox'
                                pos_hint: {'center_y': .9}
                                on_release: app.root.current = 'seconde'   
                            MDTextField:
                                id: inptext
                                font_name:'arial.ttf'
                                icon_left : 'magnify'
                                hint_text: "Enter Text"
                                helper_text: "one line only"
                                helper_text_mode: "on_focus"
                                on_text: app.text_arabic(self)
                                pos_hint: {'center_x': .5, 'center_y': .9}
                        MDRoundFlatIconButton:
                            text: "Open manager"
                            icon: "folder"
                            pos_hint: {'center_x': .5, 'center_y': .75}
                            on_release: app.file_manager_open()
                        MDRoundFlatIconButton:
                            text: "Run AES & RC4"
                            icon: "worker"
                            pos_hint: {'center_x': .5, 'center_y': .65}
                            on_release: app.button_(inptext.text)
                        MDRoundFlatIconButton:
                            text: "Save Image"
                            icon: "content-save-outline"
                            pos_hint: {'center_x': .5, 'center_y': .55}
                            on_release: app.save_images()
                        MDRoundFlatIconButton:
                            text: "Read Image"
                            icon: "read"
                            pos_hint: {'center_x': .5, 'center_y': .45}
                            on_release: app.read_text()  
                        MDRoundFlatIconButton:
                            text: "Send Image"
                            icon: "send"
                            pos_hint: {'center_x': .5, 'center_y': .35}
                            on_release: app.file_manager_open()    
                        MDRoundFlatIconButton:
                            text: "Back"
                            icon: "keyboard-backspace"
                            pos_hint: {'center_x': .5, 'center_y': .25}
                            on_release: app.root.current = 'first_logo'             

                MDNavigationDrawer:
                    id: nav_drawer

                    ContentNavigationDrawer:


<Camare_screen>:
    name:'seconde'
    orientation: 'vertical'
    Camera:
        id: camera
        play: True
        pos_hint: {'center_x': .5, 'center_y': .7}
    MDRoundFlatIconButton:
        text: "Capture"
        icon: "content-save-outline"
        pos_hint: {'center_x': .5, 'center_y': .40}
        on_release: root.capture()
    MDRoundFlatIconButton:
        text: "Read Image"
        icon: "read"
        pos_hint: {'center_x': .5, 'center_y': .30}
        on_release: app.root.current = 'AES_rc4'
    MDRoundFlatIconButton:
        text: "Back"
        icon: "keyboard-backspace"
        pos_hint: {'center_x': .5, 'center_y': .20}
        on_release: app.root.current = 'first_logo'
    MDBottomAppBar:
        MDToolbar:
            title: "Title"
            icon: "git"
            type: "bottom"
            left_action_items: [["menu", lambda x: x]]
            mode: "end"
         
'''

image = None
path_ = ''
ara = True
tex_sav = ''
new=''
new_len = 0
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

def str_path(path):
    path = path.replace('\\', "\\\\")
    return path

def send_ (text):
    global image, path_
    le = location()
    print(le[1])
    toast(str(le[1]))
    en = enc(str(le[1][0]) + str(le[1][1]))
    res = json.loads(en)
    print("AES: ",res)

    rc4 = Rc4_key(res['iv']+str(le[1][0]) + str(le[1][1])+'mynameisahmed', text, True)
    print('RC4: '+rc4)

    arr=[]
    for i in reversed(res['iv']):
        arr.append(i)

    res_ = listToString(arr)
    #print(res)

    string_ = str(rc4) + res_ +'=='+res['ciphertext']
    print(string_)
    print(path_)
    #path = json.loads(str_path(path))

    ''' Gps_ = str(le[1][0]) + str(le[1][1])
    Gps_ = Gps_.replace('.', '')
    Gps_i = int(Gps_)

    print(type(Gps_i))
    print(type(Gps_))
    print(Gps_)

    while True :
        Gps_i = (Gps_i % 2 ) + int(Gps_[int(len(Gps_)/2)])
        if Gps_i < 10:
            break
    '''

    image = hidden(path_,string_,4)
    return 0

def save_():
    global image , path_
    #print('save image')
    toast('save image')
    save(path_,image)
    return 0

def read():
    global path_
    toast('Read image')
    le = location()
    print(le[1])

    '''Gps_ = str(le[1][0]) + str(le[1][1])
    Gps_ = Gps_.replace('.', '')
    Gps_i = int(Gps_)
    print(type(Gps_i))
    print(type(Gps_))
    while True :
        Gps_i = (Gps_i % 2 ) + int(Gps_[int(len(Gps_)/2)])
        if Gps_i < 10:
            break'''

    rc4 = reveal_(path_)
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
    x= dec_d(dic_ )
    print(x)
    
    text = decrypt(res+"=="+str(le[1][0]) + str(le[1][1])+'mynameisahmed', rc4[0] )
    print(text)

    return 0


class app_name(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            previous=True,
        )

    def build(self): 
        return Builder.load_string(kv)

    def callback_for_menu_items(self, *args):
        toast(args[0])

    
    def file_manager_open(self):
        self.file_manager.show(storagepath.get_home_dir())  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)
        global path_ 
        path_ = path
        print(path_)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()
    
    def button_(self,te):
        send_ (te)

    def save_images(self):
        save_()

    def read_text(self):
        read()

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def text_arabic(self,text):
        global ara ,tex_sav,new,new_len
        '''try:
            if ara :
                old_len = new_len
                new_len = len(text.text)
                print(old_len,"  ",new_len)
                if len(text.text) >= old_len:
                    tex_sav += text.text[-1]
                    new = tex_sav
                    reshaped_text = arabic_reshaper.reshape(new)
                    text_ = get_display(u''+reshaped_text, upper_is_rtl=True)
                    print( text_ )
                    ara = False
                    text.text = text_
                else:
                    old_len = new_len
                    new_len = len(text.text)
                    tex_sav = tex_sav[1:]
                    new = tex_sav
                    ara = False
                    new = arabic_reshaper.reshape(new)
                    new = get_display(u''+new, upper_is_rtl=True)
                    text.text = new
                    pass
            else:
                ara = True
        except Exception as e:
            print(e)'''
        


    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


if __name__ == '__main__':
    app_name().run()
