import threading
import face_recognition
import cv2
import os
import datetime,time



video_capture=cv2.VideoCapture(0)



def main():
    known_DATA_DIR="./D3A"
    Student_id=[]
    faces_to_compare =[]
    rollcall=[]
    rollcall.append([])
    rollcall.append([])
    
    
    
    for filename in os.listdir(known_DATA_DIR):
        file=os.path.splitext(filename)[-1]
        if file==".png"or file==".jpg":
            image=face_recognition.load_image_file("%s/%s"%(known_DATA_DIR,filename))
            face_encoding=face_recognition.face_encodings(image)[0]
            main_file_name=os.path.splitext(filename)[0]
            Student_id.append(main_file_name)
            faces_to_compare.append(face_encoding)
            rollcall[0].append(main_file_name)
            rollcall[1].append(0)


    T=True
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    rollcall[0].sort()
    

    while T==True:
        a,frame=video_capture.read()
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        if process_this_frame:
            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)

            face_names = []
            
            for face_encoding in face_encodings:
                match = face_recognition.compare_faces(faces_to_compare, face_encoding, tolerance=0.43)
                count=0
                name = "Unknown"
                for match_true in match:
                    if match_true==True:
                        name =Student_id[count]
                        face_names.append(name)
                        rollcall_record_num=0
                        for rollcall_record in rollcall[0]:
                            if name==rollcall_record:
                                rollcall[1][rollcall_record_num]=1
                            rollcall_record_num+=1
                    count+=1



        process_this_frame = not process_this_frame
    
    
   
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        time=datetime.datetime.now()
        if time.second==30 or time.second==0:
            cv2.imwrite("./unknown_pic/%s.png"%time, frame)

   
        if time.minute==38:
            T=False
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()




main()























