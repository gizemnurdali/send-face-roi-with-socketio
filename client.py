import socketio
import cv2
import pickle
import numpy as np

sio = socketio.Client()
    
@sio.event
def connect_handler():
    print('connection established')
    send_image()
sio.on('connect',connect_handler)

@sio.event
def send_image(): 

    cam=cv2.VideoCapture(0)
    face_casc=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    i=0
    while True:
        ret,frame=cam.read()
        gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_casc.detectMultiScale(gray_frame,1.1,3)
        
        for x,y,w,h in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3) 
            
            face_roi=frame[y:y+h,x:x+w]
            face_roi_bytes=pickle.dumps(face_roi)
            i+=1
            if i==15:
                sio.emit('my_image',face_roi_bytes)
                i=0
        cv2.imshow("frame",frame)
        if cv2.waitKey(25) & 0xFF=='q':
            break
    cam.release()
    cv2.destrorAllWindows()
@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()

