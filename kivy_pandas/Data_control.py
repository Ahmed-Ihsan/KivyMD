from tkinter.constants import NONE
import pandas as pd

try:
    Data = pd.read_csv('Data.csv')
except:
    Data = pd.DataFrame({'Expiration':[],'Nmae':[],'Price':[],'Producing Country':[],'Type':[]})
    Data.to_csv('Data.csv',index=False)

try:
   User = pd.read_csv('User.csv')
except:
    User = pd.DataFrame({'Name':[],'ID':[]})
    User.to_csv('User.csv',index=False)

def sign(user= None , id = None ):
    global User
    user_sin = User[User['Name']==user]
    try:
        user_sin =user_sin.values[0]
    except:
        input = pd.DataFrame({'Name':[user],'ID':[id]})
        User = User.append(input)
        input.to_csv('User.csv',mode='a',header=False,index=False)        
        print(User)
        return 1
    if not user in user_sin :
        input = pd.DataFrame({'Name':[user],'ID':[id]})
        User = User.append(input)
        input.to_csv('User.csv',mode='a',header=False,index=False)
        return 1
    else:
        return 0

def login(user= None , id = None):
    global User
    user_login = User[User['Name']==user]
    try:
        user_login = user_login.values[0]
        print(user_login)
        if id in user_login:
            return 1
        else:
            return 0
    except:
        user_login = user_login
        if len(user_login) != 0:
            if user_login[1] == int(id):
                return 1
            else:
                return 0
        return 0