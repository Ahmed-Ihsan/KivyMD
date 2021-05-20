import kivy
import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import codecs
import string
from stegano import lsb
import secrets
import json
import geocoder
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64decode


def enc(data):
    data = str(data)
    data = data.encode('utf-8')
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB)
    ct_bytes = cipher.encrypt(data)
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv':iv, 'ciphertext':ct})
    return result

def dec_(result):
    try:
        #b64 = json.loads(result)
        b64 = result
        print(b64)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        pt = cipher.decrypt(ct)
        print(pt)
        return pt
    except ValueError:
        print("Incorrect decryption")

def location():
    g = geocoder.ip('me')
    return g, g.latlng

def hidden(path,text):
    secret = lsb.hide(path,str(text))
    secret.save('HiddenText/Test_gray.png')
    return secret
    
def save(path ,image):
    image.save(path)

def reveal(path):
    msg= lsb.reveal(path)
    return msg

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
        print(11111111111)
    except:
        pass
    #print('decrypted:', decrypted)

    if cipher:
        #print('\nCongrats ! You made it.')
        return ciphertext
    elif not cipher :
        return decrypted
    else:
        #print('Shit! You pooped your pants ! .-.')
        pass

    # until next time folks !



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

    image = hidden('NO2_adam.png',string_)
    
    return 0

def save_(a1 =1):
    global image
    print('save image')
    save('Test_gray1.png',image)
    return 0

def read(a1 =1):

    le = location()
    print(le[1])

    rc4 = reveal('Test_gray1.png')
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