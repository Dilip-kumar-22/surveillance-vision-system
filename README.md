# Argus: Computer Vision Surveillance 👁️

A real-time motion detection system built with OpenCV. It transforms a standard webcam into a security sentinel that monitors an environment, highlights moving targets with bounding boxes, and logs entry/exit timestamps to a CSV file.

## ⚡ Features
* **Gaussian Blur Filtering:** Reduces visual noise to prevent false positives.
* **Delta Frame Calculation:** Compares current video frames against a static baseline to identify pixel shifts.
* **Automated Logging:** records exact timestamps of all detected motion events into a structured dataset (`Times.csv`) for later analysis.
* **Live HUD:** Draws dynamic bounding boxes around targets in real-time.

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Computer Vision:** OpenCV (`cv2`)
* **Data Handling:** Pandas (Time-series logging)

## 🚀 Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
