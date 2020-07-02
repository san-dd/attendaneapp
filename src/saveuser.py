
from pymongo import MongoClient, errors    
myclient = MongoClient('mongodb://localhost:27017/')
mydb = myclient.mydatabase
mycol = mydb.userdetails
#save user details to mongodb
def saveuser(data):
    print(data)
    try:
        x = mycol.insert_one(data)
        return {"success":False,"id":x.inserted_id}
    except:
        print("errorin mongo")
        return {"success":False}
#list all user
def listuser():
    try:
        userlist=mycol.find()
        userlist=[i for i in userlist]
        return {"success":True ,"userlist":userlist}
    except:
        print("errorin mongo")
        return {"success":False}
#list all searched user
def searchuserdetails(mobno):
    try:
        userlist=mycol.find({ "mobno": {"$in":mobno} })
        userlist=[i for i in userlist]
        print("searched user",userlist)
        return {"success":True ,"userlist":userlist}
    except:
        print("errorin mongo")
        return {"success":False}
    
def deleteuser(mobno):
    try:
        userlist=mycol.remove({ "mobno": mobno })
        return {"success":True}
    except:
        print("errorin mongo")
        return {"success":False}
#print(saveuser(mydict))
#print(searchuserdetails(["08087632981"]))