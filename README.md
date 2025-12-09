# 🧠 AVM - AI Virtual Mouse

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?style=for-the-badge)
![PySide6](https://img.shields.io/badge/PySide6-Modern%20UI-Qt?style=for-the-badge&logo=qt&logoColor=white)

> **A futuristic, touch-free computer interface controlled entirely by Hand Gestures and Voice Commands.**

---

## 🌟 Overview
**Neural Interface** converts your webcam into a powerful input device. Forget physical mice and keyboards—control your cursor, click, drag files, and manage system volume just by waving your hands. It features a sleek **Dark Mode Dashboard** built with PySide6 for real-time feedback.

---

## 🎮 Gesture Controls (How to Use)

| Gesture | Action | Description |
| :--- | :--- | :--- |
| **Index Finger Up** ☝️ | **Move Cursor** | Moves the mouse pointer smoothly across the screen. |
| **Index + Thumb Pinch** 👌 | **Left Click** | Quick pinch (< 0.2s) for Click/Double Click. |
| **Fist (Mutthi)** ✊ | **Drag & Drop** | Clench your fist to grab and drag files/windows. |
| **Index + Middle Up** ✌️ | **Right Click** | Raises context menu. |
| **Two Hands Index Up** ☝️☝️ | **Volume Control** | Move hands apart to **Increase**, close to **Decrease**. |
| **4 Fingers Up** 🖐️ | **Toggle UI** | Hides/Shows the Dashboard panel. |
| **Cross Wrists (Wakanda)** 🙅‍♂️ | **Sleep/Wake** | Locks or Unlocks the system tracking. |

---

## 🗣️ Voice Commands (Super Mode)
Just say the command to trigger actions via Windows Search:

* 🎙️ **"Open Chrome"** → Launches Google Chrome.
* 🎙️ **"Open Spotify"** → Plays your music.
* 🎙️ **"Screenshot"** → Saves a screenshot instantly.
* 🎙️ **"Close Window"** → Closes the current active app.

---

## 🛠️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/AI-Virtual-Mouse.git](https://github.com/YOUR_USERNAME/AI-Virtual-Mouse.git)
    cd AI-Virtual-Mouse
    ```

2.  **Install Dependencies**
    (Make sure you have Python installed)
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    python main.py
    ```

---

## 📂 Project Structure
* `main.py` - The entry point of the application.
* `worker.py` - Contains the Logic Engine (OpenCV, MediaPipe, Audio control).
* `ui.py` - Handles the Modern Dashboard UI (PySide6).
* `Assets/` - Stores icon images for the UI.

---

## 📸 Screenshots
*(Upload a screenshot of your running project here later)*

---

### ❤️ Show some love
If you like this project, give it a **Star ⭐** on GitHub!