from picamera2 import Picamera2
import cv2
import time
import requests
from config import api_url

# Set up the camera with Picam
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Give camera time to warm up
time.sleep(1)

frame_count = 1

last_sent_time = time.time()

while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    current_time = time.time()

    # Frames only get sent every 1 second
    if current_time - last_sent_time >= frame_count:
        
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        image_data = buffer.tobytes()

        
        # Send frames to the server
        try:
            response = requests.post(
                api_url, files={'image': (f'cat-{current_time}.jpg', image_data,'image/jpeg')},
                timeout=5
                )
            
            # Get the response from the server
            if response.status_code == 200:
                print("Image sent successfully")
            else:
                print("Failed to send image")

            last_sent_time = current_time

        except requests.exceptions.RequestException as e:
            print(f"Error sending image: {e}")



    

    



picam2.close()
cv2.destroyAllWindows()

