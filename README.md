# 🐱 Cat Tracker – Raspberry Pi + YOLO-World

This project uses a **Raspberry Pi 4B (8GB)** with a **Pi Camera 2** to detect stray cats that visit my house at night to eat. The camera captures a live feed of the food bowl, and a **YOLO-World** zero-shot object detection model runs periodically to check for the presence of a cat based on a text prompt (e.g., `"cat"`).

When a cat is detected, an image is captured and uploaded to an **AWS S3 bucket**. This S3 upload automatically triggers an **AWS Lambda** function, which retrieves the most recently uploaded image and sends it to me via **Amazon SES email** as a real-time alert.


---

## 📦 Features

- Live camera feed using `picamera2`
- Scheduled object detection using YOLO-World (`ultralytics`)
- Text-prompted detection (e.g., `"cat"`, `"fluffy animal"`)
- Upload matching images to AWS S3
- Image sent to user via AWS SES 
- Runs in a Python virtual environment with minimal system dependencies

---