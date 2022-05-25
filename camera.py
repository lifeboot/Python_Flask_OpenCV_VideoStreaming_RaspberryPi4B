import cv2
import numpy
from flask import Flask, render_template, Response, stream_with_context, request

video = cv2.VideoCapture(0)
app = Flask('__name__')

# defining face detector
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

def video_stream():
    while True:
        ret, frame = video.read()
        if not ret:
            break;
        else:
            frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)                    
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            face_rects=face_cascade.detectMultiScale(gray,1.3,5)
            for (x,y,w,h) in face_rects:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                break
            # encode OpenCV raw frame to jpg and displaying it
            ret, buffer = cv2.imencode('.jpeg', frame)
            #return buffer.tobytes()
            #ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port='5000', debug=False)
