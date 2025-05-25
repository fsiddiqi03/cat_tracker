from picamera2 import Picamera2
import cv2
import time
from ultralytics import YOLO
from api import API
from config import api_url
from gpiozero import MotionSensor


# Set up the camera with Picam
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Api Setup 
sender = API(api_url)
pir = MotionSensor(4)

try:
    while True:

        
        
        if pir.motion_detected:
            print("Motion detected!")
           
            # capture frame from camera
            frame = picam2.capture_array()
            _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])

            timestame = time.time()
            file_name = f"cat_{timestame}.jpg"

            # call api 
            response = sender.send_request(jpeg.tobytes(), file_name)
            print(response)
            # check if the response is valid
            if response.status_code == 200:
                print("Image sent successfully")
            else:
                print("Failed to send image")



except KeyboardInterrupt:
    print("Exiting...")
finally:
    picam2.stop()
    picam2.close()
    print("Camera stopped and closed.")


