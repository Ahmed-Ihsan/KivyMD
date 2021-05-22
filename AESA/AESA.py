import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64decode

def enc(data ,key):
    data = str(data)
    data = data.encode('utf-8')
    #key = get_random_bytes(16)
    key = key.replace('.', '')
    key = bytes(key+'ahmd','utf-8')
    cipher = AES.new(key, AES.MODE_CFB)
    ct_bytes = cipher.encrypt(data)
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv':iv, 'ciphertext':ct})
    return result

def dec_d(result,key):
    try:
        #b64 = json.loads(result)
        b64 = result
        print(b64)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        key = key.replace('.', '')
        key = bytes(key+'ahmd','utf-8')
        #key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        pt = cipher.decrypt(ct)
        return pt
    except ValueError:
        print("Incorrect decryption")