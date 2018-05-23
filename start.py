import time,datetime
import os
import cv2
import mysql.connector
import face_recognition
import shutil
from PIL import Image

unknown_DATA_DIR="./unknown_pic"
known_DATA_DIR="./D3A"
#video_capture = cv2.VideoCapture(0)

db = mysql.connector.connect(user="root", passwd="takming",host="localhost", db="student",charset="utf8")
cursor = db.cursor()
cursor.execute("SELECT student_id,student_image FROM student_data")
results = cursor.fetchall()

Student_id=[]
faces_to_compare =[]
for filename in os.listdir(known_DATA_DIR):
    file=os.path.splitext(filename)[-1]
    if file==".png"or file==".jpg"or file==".bmp":
        image=face_recognition.load_image_file("%s/%s"%(known_DATA_DIR,filename))
        face_encoding=face_recognition.face_encodings(image)[0]
        main_file_name=os.path.splitext(filename)[0]
        Student_id.append(main_file_name)
        faces_to_compare.append(face_encoding)


while True:
    time=datetime.datetime.now()
    if time.minute==35:
        os.system("python main.py")
    else:
        try:
            image_count=0
            for filename in os.listdir(unknown_DATA_DIR):
                file=os.path.splitext(filename)[-1]
                if file==".png"or file==".jpg"or file==".bmp":
                    image=face_recognition.load_image_file("./unknown_pic/%s"%filename)
                    face_locations = face_recognition.face_locations(image)
                    for face_location in face_locations:
                        top, right, bottom, left = face_location
                        face_image = image[top:bottom, left:right]
                        pil_image = Image.fromarray(face_image)
                        image_count=image_count+1
                        pil_image.save("./unknown_pic/after/image%s.png" % (image_count))
                    shutil.move("./unknown_pic/%s"%(filename),"./unknown_pic/recognition_end")



            for filename in os.listdir("./unknown_pic/after"):
                file=os.path.splitext(filename)[-1]
                if file==".png"or file==".jpg"or file==".bmp":
                    uknown_image=face_recognition.load_image_file("./unknown_pic/after/%s"%filename)
                    uknown_face_encoding = face_recognition.face_encodings(uknown_image)[0]
                    match = face_recognition.compare_faces(faces_to_compare,uknown_face_encoding, tolerance=0.43)
                    count=0
                    name = "Unknown"
                    for match_true in match:
                        if match_true==True:
                            name=Student_id[count]
                        count=count+1
                
                
                    time=datetime.datetime.now()
                    os.rename(os.path.join('./unknown_pic/after', filename), os.path.join('./unknown_pic/after', "%s_%s.png"%(time,name)))
                    shutil.move("./unknown_pic/after/%s_%s.png"%(time,name),"./known_people")




        except IndexError as n:
            print("錯誤原因：",n)
            os.rename(os.path.join('./unknown_pic/after', filename), os.path.join('./unknown_pic/after', "%s_%s"%(time,filename)))
            shutil.move("./unknown_pic/after/%s_%s"%(time,filename),"./unknown_pic/recognition_end")
























