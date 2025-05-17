from picamera2 import Picamera2
import cv2
import time


# Set up the camera with Picam
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Give camera time to warm up
time.sleep(1)

while True:
    # Capture an image
    image = picam2.capture_array()

    # Display the image in a window
    cv2.imshow("Live Image", image)

    # Wait for a key press and check if it's 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the camera and close all OpenCV windows
picam2.close()
cv2.destroyAllWindows()

