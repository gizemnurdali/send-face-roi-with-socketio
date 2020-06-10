import eventlet
import socketio
import pickle 
from PIL import Image 
import PIL 
import cv2

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect', sid)

@sio.event
def my_image(sid,bytes): 
    
    frame=pickle.loads(bytes)
    img=PIL.Image.fromarray(frame)
    img.save('testrgb.png')
    img_ = cv2.imread('testrgb.png') 
    cv2.imshow('frame',img_)
    cv2.waitKey(1)
    print("frame is saved")

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__== '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

