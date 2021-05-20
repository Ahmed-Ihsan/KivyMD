from stegano import lsb

def hidden(path,text):
    secret = lsb.hide(path,str(text))
    return secret

def save(path ,image):
    image.save(path)

def reveal(path):
    msg= lsb.reveal(path)
    return msg