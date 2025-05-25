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

# Time management variables
ACTIVE_DURATION = 120  # Send frames for 60 seconds after motion
FRAME_INTERVAL = 1.0  # Send frame every 1 second during active period
MOTION_DEBOUNCE = 5   # Minimum seconds between motion events to restart timer

motion_start_time = 0
last_frame_sent = 0
last_motion_time = 0
active_mode = False

try:
    while True:

        current_time = time.time()
        # Check if the motion sensor is triggered

        # Check for motion
        if pir.motion_detected:
            if current_time - last_motion_time >= MOTION_DEBOUNCE:
                print("Motion detected!")
                motion_start_time = current_time
                last_motion_time = current_time
                active_mode = True
        
            elif active_mode:
                print("Motion detected again, resetting timer.")
                motion_start_time = current_time



        # Exit active mode if active for longer than 2 minutes 
        if active_mode and (current_time - motion_start_time >= ACTIVE_DURATION):
            print("Active mode ended.")
            active_mode = False
           


        if active_mode and (current_time - last_frame_sent >= FRAME_INTERVAL):
            print("Motion detected!")
           
            # capture frame from camera
            frame = picam2.capture_array()
            _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])

            timestamp = time.time()
            file_name = f"cat_{timestamp}.jpg"

            try:
                response = sender.send_request(jpeg.tobytes(), file_name)
                print(response)
                # check if the response is valid
                if response.status_code == 200:
                    print("Image sent successfully")
                    last_frame_sent = current_time
                else:
                    print("Failed to send image")
            except Exception as e:
                print(f"Error sending image: {e}")



except KeyboardInterrupt:
    print("Exiting...")
finally:
    picam2.stop()
    picam2.close()
    print("Camera stopped and closed.")


