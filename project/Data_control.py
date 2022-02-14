import pandas as pd

try:
    Data = pd.read_csv('Data.csv')
except:
    Data = pd.DataFrame({'ID':[],'Nmae':[],'Age':[],'Number Phone':[],'Adress':[],'result':[]})
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
        return 1
    if not user in user_sin :
        input = pd.DataFrame({'Name':[user],'ID':[id]})
        User = User.append(input)
        input.to_csv('User.csv',mode='a',header=False,index=False)
        return 1
    else:
        print('12E')
        return 0

def login(user= None , id = None):
    global User
    user_login = User[User['Name']== user]
    try:
        user_login = user_login.values[0]
        if str(id) in str(user_login):
            return 1
        else:
            print('12A')
            return 0
    except:
        if len(user_login) != 0:
            if user_login[1] == int(id):
                return 1
            else:
                print('12B')
                return 0
        print('12C')
        return 0

def add(ID = None,name = None, Age = None, Number_Phone = None, Adress = None,result = None):
    global Data
    try:
        input = pd.DataFrame({'ID':[ID],'Nmae':[name],'Age':[Age],'Number Phone':[Number_Phone],'Adress':[Adress],'result':[result]})
        Data = Data.append(input)
        input.to_csv('Data.csv',mode='a',header=False,index=False)
        return 1
    except:
        print('12D')
        return 0

def delete():
    pass
def edite():
    pass
def search():
    pass