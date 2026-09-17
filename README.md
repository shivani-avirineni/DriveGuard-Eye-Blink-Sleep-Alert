```text
# 🚗 DriveGuard – Eye Blink Based Sleep Alert

DriveGuard is a real-time driver drowsiness detection system designed to monitor a driver's eyes using computer vision. The system detects prolonged eye closure and provides an audio alert when signs of drowsiness are detected, helping improve driver awareness and road safety.

## Features

- Real-time driver drowsiness detection
- Eye-blink and eye-closure monitoring
- Face detection using OpenCV
- Detection of prolonged eye closure
- Automatic audio alert when drowsiness is detected
- User registration and login
- Dashboard for accessing the detection system
- Webcam-based real-time monitoring
- Simple and user-friendly web interface

## Technologies Used

- Python
- Flask
- OpenCV
- NumPy
- Pygame
- HTML
- CSS
- JavaScript
- Haar Cascade Classifiers
- Git and GitHub

## How It Works

The system uses the computer's webcam to continuously monitor the driver's face and eyes.

1. The webcam captures the driver's face in real time.
2. OpenCV detects the face using a Haar Cascade classifier.
3. The eye region is detected from the driver's face.
4. The system monitors eye activity and blink/closure patterns.
5. If the eyes remain closed for a predefined period, the system considers it a possible drowsiness event.
6. An audio alert is played using the configured sound file.
7. The driver is alerted so that they can become aware of their drowsy state and take appropriate action.

## System Workflow

Webcam
   ↓
Face Detection
   ↓
Eye Detection
   ↓
Eye Blink Monitoring
   ↓
Prolonged Eye Closure
   ↓
Drowsiness Detected
   ↓
Audio Alert

## Project Structure

DriveGuard-Eye-Blink-Sleep-Alert/
│
├── static/
│   ├── css/
│   ├── img/
│   └── js/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   └── register.html
│
├── App.bat
├── app.py
├── SleepDetection.py
├── buzz.mp3
├── haarcascade_eye_tree_eyeglasses.xml
├── haarcascade_frontalface_default.xml
├── requirements.txt
└── .gitignore

## Installation

### 1. Clone the Repository

git clone https://github.com/shivani-avirneni/DriveGuard-Eye-Blink-Sleep-Alert.git

### 2. Open the Project Directory

cd DriveGuard-Eye-Blink-Sleep-Alert

### 3. Create a Virtual Environment

python -m venv venv

### 4. Activate the Virtual Environment

For Windows:

venv\Scripts\activate

### 5. Install the Required Packages

pip install -r requirements.txt

## Running the Application

Run the Flask application using:

python app.py

After starting the application, open a web browser and visit:

http://127.0.0.1:5000/

Register a new user or log in with an existing account and access the dashboard.

## Using the Drowsiness Detection System

1. Start the application.
2. Log in to the DriveGuard system.
3. Open the dashboard.
4. Start the drowsiness detection system.
5. Allow webcam access if requested.
6. Position your face clearly in front of the camera.
7. The system continuously monitors your eyes.
8. If prolonged eye closure is detected, the alert sound is activated.

## User Authentication

The application includes a basic user authentication interface consisting of:

- User Registration
- User Login
- Dashboard
- Logout

The web pages are implemented using Flask templates and HTML/CSS/JavaScript.

## Computer Vision

OpenCV is used for real-time face and eye detection. Haar Cascade XML classifiers are included in the project to identify facial and eye regions from webcam frames.

The system uses:

- haarcascade_frontalface_default.xml
- haarcascade_eye_tree_eyeglasses.xml

These classifiers help locate the driver's face and eyes during monitoring.

## Alert System

When the system detects prolonged eye closure, an audio alert is generated using the project's `buzz.mp3` sound file.

The purpose of the alert is to notify the driver of a possible drowsiness condition.

## Applications

DriveGuard can be used as a prototype for:

- Driver safety systems
- Long-distance driving
- Night-time driving
- Commercial transportation
- Truck and bus driver monitoring
- Automotive safety applications
- Computer vision-based driver assistance systems

## Future Enhancements

The project can be further enhanced with:

- Facial landmark-based Eye Aspect Ratio (EAR)
- Machine learning-based drowsiness classification
- Improved detection accuracy
- Head-pose estimation
- Yawning detection
- Mobile application integration
- SMS or emergency notifications
- Cloud-based driver monitoring
- Driver fatigue analytics
- Improved performance under different lighting conditions

## Limitations

The current system is a computer-vision prototype and its performance may be affected by:

- Poor lighting conditions
- Camera quality
- Face position
- Occlusion of the eyes
- Glasses and other visual obstructions
- Webcam availability

Therefore, the system should be considered an assistance/prototype system rather than a replacement for safe driving practices.

## Author

Shivani Avirneni

GitHub:
https://github.com/shivani-avirneni

## License

This project is developed for educational and academic purposes.

⭐ If you find this project useful, consider giving the repository a star.
```
