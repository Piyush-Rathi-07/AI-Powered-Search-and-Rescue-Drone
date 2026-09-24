# AI-Powered Search & Rescue Drone

## 🚁 Project Overview

An AI-powered drone-based Search & Rescue system designed to assist rescue teams in locating possible victims and identifying hazards in disaster-affected areas.

The system combines an FPV drone, RGB camera, AI-based object detection, GPS geo-tagging and a rescue dashboard.

## 🎯 Objectives

- Detect possible victims using an onboard RGB camera.
- Detect hazards such as fire, smoke and debris.
- Obtain the drone's GPS location.
- Geo-tag detected objects.
- Provide useful information to rescue teams.
- Support faster and safer search operations.

## 🧠 AI Detection

The project includes two AI approaches:

### 1. Normal YOLO

Uses predefined object classes for real-time detection.

Example:
- Person
- Vehicle
- Other supported classes

### 2. Open-Vocabulary YOLO

Allows detection using user-defined text prompts.

Example:
- Person
- Fire
- Smoke
- Debris
- Collapsed building
- Vehicle

## 📡 System Workflow

RGB Camera
↓
AI Detection
↓
Possible Victim / Hazard
↓
GPS Geo-tagging
↓
Communication
↓
Rescue Dashboard

## 🛠️ Hardware

- FPV Drone
- Flight Controller
- RGB Camera
- GPS Module
- Companion Computer
- Communication Module

## 💻 Software

- Python
- OpenCV
- Ultralytics YOLO
- PySerial
- Tkinter
- Linux / Raspberry Pi OS (depending on hardware)

## 📂 Repository Structure

```text
Search-Rescue-Drone/
│
├── AI/
│   ├── normal_yolo/
│   │   └── detect.py
│   │
│   └── open_vocabulary_yolo/
│       └── detect_open_vocab.py
│
├── GPS/
│   └── gps_reader.py
│
├── Dashboard/
│   └── dashboard.py
│
├── Communication/
│   └── communication_demo.py
│
├── requirements.txt
└── README.md

##⚙️ Installation

Install the required Python libraries:

pip install -r requirements.txt

##▶️ Running AI Detection

For normal YOLO:

python AI/normal_yolo/detect.py

For Open-Vocabulary YOLO:

python AI/open_vocabulary_yolo/detect_open_vocab.py

##📍 GPS

The GPS module reads positioning information from the connected GPS receiver and can be used to associate detected objects with approximate coordinates.

📊 Dashboard

The dashboard displays information such as:

1)Possible victim detections
2)Hazard detections
3)Confidence values
4)GPS information
5)Drone status

##🚧 Current Scope

The current software prototype focuses on RGB-camera-based detection, GPS information and rescue-data visualization.

##Future Scope

Potential future enhancements include:

1)UWB-based through-rubble sensing
2)RF/cellular-based victim signal detection
3)Multi-UAV coordination
4)Mesh communication
5)Thermal imaging
6)GPS-denied navigation
7)Advanced victim prioritization

##⚠️ Disclaimer

AI detection indicates a detected object or possible victim candidate; it does not by itself confirm that a person is a victim. Hardware performance depends on the camera, drone, computing platform, environment and communication system.





