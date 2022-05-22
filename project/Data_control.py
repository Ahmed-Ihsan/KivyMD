import pandas as pd

try:
    Data = pd.read_csv('Data.csv')
except:
    Data = pd.DataFrame({'ID':[],'Nmae':[],'Age':[],'Number Phone':[],'Adress':[],'result':[]})
    Data.to_csv('Data.csv')

try:
   User = pd.read_csv('User.csv')
except:
    User = pd.DataFrame({'Name':[],'ID':[]})
    User.to_csv('User.csv')

def sign(user= None , id = None ):
    global User
    user_sin = User[User['Name']==user]
    try:
        user_sin =user_sin.values[0]
    except:
        input = pd.DataFrame({'Name':[user],'ID':[id]})
        User = User.append(input)
        input.to_csv('User.csv',mode='a',header=False,index=True)        
        return 1
    if not user in user_sin :
        input = pd.DataFrame({'Name':[user],'ID':[id]})
        User = User.append(input)
        input.to_csv('User.csv',mode='a',header=False,index=True)
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
        res = Data[Data['ID']==ID]
        if len(res) == 0:
            input = pd.DataFrame({'ID':[str(ID)],'Nmae':[name],'Age':[Age],'Number Phone':[Number_Phone],'Adress':[Adress],'result':[result]})
            print(input)
            print(Data)
            Data = pd.concat([input, Data],ignore_index=True)
            Data.to_csv('Data.csv')
            return 1
        return 0
    except:
        print('12D')
        return 0

def edite(ID = None,name = None, Age = None, Number_Phone = None, Adress = None,result = None):
    global Data
    res = Data[Data['ID'] == str(ID)].index
    for i in [(ID,'ID'),(name,'Nmae'), (Age,'Age'), (Number_Phone,'Number Phone'), (Adress,'Adress'),(result,'result')]:
        Data.loc[res, i[1]] = i[0]
    Data.to_csv('Data.csv')
    
def search(key=None, word=None ):
    s = word[0]
    if key is None:
        if type(s) is str:
            pass
        else:
            print('12W')
            if word is None:
                print('12L')
                return 0
            word = str(s)
        for i in ['ID','Nmae','Age','Number Phone','Adress','result']:
            reslt = Data[Data[i] == s]
            if  len(reslt) >= 1 :
                return reslt
        return 0
    else:
        reslt = Data[Data[key]== s]
        if not reslt is None :
            return reslt
        return 0

def show_data():
    return Data

def remove_data(data):
    if type(data) is str:  
        Data.drop(Data[Data['ID'] == data].index,inplace = True)
        header_libel = pd.DataFrame({'ID':[],'Nmae':[],'Age':[],'Number Phone':[],'Adress':[],'result':[]})
        header_libel.to_csv('Data.csv',index=True)
        Data.to_csv('Data.csv',mode='a',header=False,index=True)
        return 1
    return 'Error , the value is not string'
