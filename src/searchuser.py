import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# from PIL import ImageGrab
 
path = 'C:/Users/santo/attendaneapp/static/uploads'
temppath='C:/Users/santo/AppData/Local/Temp'


images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
 
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
 
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
'''cap = cv2.VideoCapture(0)
 
while True:
    success, img = cap.read()
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
 
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
 
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)'''
def searchImages(file):
    try:
        print("filename",file)
        imgTest = face_recognition.load_image_file(f'{temppath}/{file}')
        imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
        print(f'{temppath}/{file}')
        faceLocTest = face_recognition.face_locations(imgTest)[0]
        encodeTest = face_recognition.face_encodings(imgTest)[0]

        results = face_recognition.compare_faces(encodeListKnown,encodeTest)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeTest)
        findfaces=[myList[i] for i in range(len(myList)) if results[i]==True]
        userclass=[i.split("_")[0] for i in findfaces]
        print(results,faceDis)
        print("find class",userclass)
        return {"success":True, "userclass":set(userclass)}
    except:
        return {"success":False}
#delete incoding from 
def deleteEncoding(imagelist):
    for image in imagelist:
        indexofimage=myList.index(image)
        del(myList[indexofimage])
        del(classNames[indexofimage])
        del(encodeListKnown[indexofimage])
        
#inser encoding to current model to avoid refresh model
def InsertEncoding(imagelist):
    try:
        newimages=[]
        for cl in imagelist:
            curImg = cv2.imread(f'{path}/{cl}')
            newimages.append(curImg)
            myList.append(cl)
            classNames.append(os.path.splitext(cl)[0])
            
        for img in newimages:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeListKnown.append(encode)
        return {"success":True}
    except:
        return {"success":False}
        

#conver image to base 64
# import base64
# from PIL import Image
# from io import BytesIO

# with open("encoded-20200707194720.txt", "rb") as image_file:
#     data = image_file.read()#base64.b64encode(image_file.read())

# im = Image.open(BytesIO(base64.b64decode(data)))
# im.save('image1.png', 'PNG')
