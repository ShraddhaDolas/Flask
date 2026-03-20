from flask import Flask, render_template, Response
import cv2, time

app=Flask(__name__)
camera=cv2.VideoCapture(0)
time.sleep(1)

def generate_frames():
    while True:
        #read the camera frame
        success, frame = camera.read() #two parameters are given
        if not success:
            break
        else:
           '''The cv2.imencode() function in OpenCV encodes an image from its 
           raw format (a NumPy array) into a compressed image format (like JPEG or PNG) 
           and stores it in a memory buffer (as an array of bytes) instead of saving 
           it to a file on disk.'''

           ret, buffer = cv2.imencode('.jpeg', frame) 
           if not ret:
               print("failed to grab frame")
           frame = buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame' )

if __name__=="__main__":
    app.run(debug=True)