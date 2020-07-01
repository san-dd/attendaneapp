
from pymongo import MongoClient, errors    
myclient = MongoClient('mongodb://localhost:27017/')
mydb = myclient['mydatabase']
mycol = mydb["userdetails"]

#x = mycol.insert_one(mydict)

def saveuser(data):

    print(data)
    try:
        x = mycol.insert_one(data)
        return x.inserted_id
        print()
    except:
        print("errorin mongo")
        return("err")

def listuser():
    try:
        userlist=mycol.find()
        userlist=[i for i in userlist]
        return userlist
    except:
        print("errorin mongo")
        return("err")
#print(saveuser(mydict))