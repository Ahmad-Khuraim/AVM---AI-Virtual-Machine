# worker.py
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time
import speech_recognition as sr
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage

# Audio Libs Setup
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
except:
    pass


class VoiceWorker(QThread):
    status_update = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.running = False
        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()

    def run(self):
        self.running = True
        with self.mic as source:
            try:
                self.rec.adjust_for_ambient_noise(source)
            except:
                pass
            while self.running:
                try:
                    # Listen
                    audio = self.rec.listen(source, timeout=3, phrase_time_limit=4)
                    try:
                        text = self.rec.recognize_google(audio).lower()

                        if "chrome" in text:
                            self.status_update.emit("Opening Chrome...", "#00ff00")
                            pyautogui.hotkey('win', 'r')
                            time.sleep(0.5)
                            pyautogui.write('chrome')
                            pyautogui.press('enter')
                        elif "close" in text:
                            self.status_update.emit("Closing Window...", "#ff0000")
                            pyautogui.hotkey('alt', 'f4')
                        elif "show" in text:
                            self.status_update.emit("TOGGLE_UI", "")
                    except sr.UnknownValueError:
                        pass
                except:
                    pass

    def stop(self):
        self.running = False
        self.terminate()


class VideoWorker(QThread):
    frame_ready = Signal(QImage)
    status_update = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.smoothening = 5
        self.sensitivity = 1.5

        self.plocX, self.plocY = 0, 0
        self.screen_w, self.screen_h = pyautogui.size()
        self.frame_r = 100

        # Audio
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.vol_range = self.volume.GetVolumeRange()
            self.min_vol = self.vol_range[0]
            self.max_vol = self.vol_range[1]
        except:
            self.volume = None

        self.voice_worker = VoiceWorker()
        self.voice_worker.status_update.connect(self.pass_signal)

        # State Variables
        self.drag_active = False
        self.active_hand_label = "Right"

        # Timers
        self.pinch_start_time = 0
        self.pinch_active = False
        self.last_click_time = 0
        self.last_back_time = 0
        self.wakanda_timer = 0

        # Feature Flags
        self.gestures = {
            "move": True,
            "drag": True,
            "right_click": True,
            "left_click": True,
            "back": True,
            "four_finger": True
        }

    def pass_signal(self, msg, col):
        self.status_update.emit(msg, col)

    def toggle_voice(self, state):
        if state == Qt.Checked:
            self.voice_worker.start()
            self.status_update.emit("Voice Listening...", "#00d4ff")
        else:
            self.voice_worker.stop()
            self.status_update.emit("Voice OFF", "#888888")

    def toggle_hand(self):
        if self.active_hand_label == "Right":
            self.active_hand_label = "Left"
        else:
            self.active_hand_label = "Right"
        self.status_update.emit(f"Switched to {self.active_hand_label} Hand", "#ffffff")

    def toggle_gesture(self, gesture_name):
        if gesture_name in self.gestures:
            self.gestures[gesture_name] = not self.gestures[gesture_name]
            state = "ON" if self.gestures[gesture_name] else "OFF"
            self.status_update.emit(f"{gesture_name.replace('_', ' ').title()} {state}", "#aaaaaa")

    def get_dist(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def run(self):
        cap = cv2.VideoCapture(0)
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        draw_utils = mp.solutions.drawing_utils

        while self.running:
            ret, frame = cap.read()
            if not ret: continue

            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            mode_text = "Idle"
            mode_color = "#888888"

            if results.multi_hand_landmarks:
                hand_data = []
                for landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    label = handedness.classification[0].label
                    lm_list = []
                    for id, lm in enumerate(landmarks.landmark):
                        lm_list.append([int(lm.x * w), int(lm.y * h)])
                    hand_data.append((label, lm_list))
                    draw_utils.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                # --- 1. SLEEP / WAKE ---
                if len(hand_data) == 2:
                    h1, h2 = hand_data[0][1], hand_data[1][1]
                    wrist_dist = self.get_dist(h1[0], h2[0])

                    if wrist_dist < 60:
                        self.wakanda_timer += 1
                        if self.wakanda_timer > 3:  # Fast trigger (0.1s)
                            self.status_update.emit("TOGGLE_SLEEP", "#ff0000")
                            self.wakanda_timer = 0
                            time.sleep(1)
                    else:
                        self.wakanda_timer = 0

                    # --- 2. VOLUME ---
                    i1, i2 = h1[8], h2[8]
                    dist = self.get_dist(i1, i2)
                    cv2.line(frame, tuple(i1), tuple(i2), (255, 0, 255), 2)

                    if self.volume:
                        vol_level = np.interp(dist, [50, 300], [self.min_vol, self.max_vol])
                        self.volume.SetMasterVolumeLevel(vol_level, None)
                        vol_percent = int(np.interp(dist, [50, 300], [0, 100]))
                        mode_text = f"VOL: {vol_percent}%"
                        mode_color = "#00ffcc"

                        # --- 3. ONE HAND CONTROL ---
                target_lm = None
                for label, lm in hand_data:
                    if label == self.active_hand_label:
                        target_lm = lm
                        break
                if target_lm is None and len(hand_data) > 0:
                    target_lm = hand_data[0][1]

                if target_lm:
                    lm = target_lm
                    x1, y1 = lm[8]
                    x2, y2 = lm[12]
                    thumb = lm[4]

                    fingers = []
                    # Simple finger up check
                    if lm[4][1] < lm[3][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    for id in [8, 12, 16, 20]:
                        if lm[id][1] < lm[id - 2][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    # A. 4 FINGERS (Toggle UI)
                    if fingers[1:] == [1, 1, 1, 1] and self.gestures['four_finger']:
                        mode_text = "Toggle UI"
                        self.status_update.emit("TOGGLE_UI", "#ffffff")
                        time.sleep(0.5)

                    # B. DRAG (Fist)
                    elif fingers == [0, 0, 0, 0, 0] and self.gestures['drag']:
                        mode_text = "DRAGGING"
                        mode_color = "#ffaa00"
                        drag_pt = lm[9]  # Knuckle

                        if not self.drag_active:
                            pyautogui.mouseDown()
                            self.drag_active = True

                        x3 = np.interp(drag_pt[0], (self.frame_r, w - self.frame_r), (0, self.screen_w))
                        y3 = np.interp(drag_pt[1], (self.frame_r, h - self.frame_r), (0, self.screen_h))
                        self.plocX += (x3 - self.plocX) / self.smoothening
                        self.plocY += (y3 - self.plocY) / self.smoothening
                        pyautogui.moveTo(self.plocX, self.plocY)

                    elif self.drag_active and fingers != [0, 0, 0, 0, 0]:
                        pyautogui.mouseUp()
                        self.drag_active = False
                        mode_text = "Dropped"

                    # C. BACK (3 Fingers)
                    elif fingers[1:4] == [1, 1, 1] and fingers[4] == 0 and self.gestures['back']:
                        mode_text = "BACK"
                        mode_color = "#ff00ff"
                        if time.time() - self.last_back_time > 1.0:
                            pyautogui.hotkey('alt', 'left')
                            self.last_back_time = time.time()

                    # D. RIGHT CLICK (Index+Middle)
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and self.gestures['right_click']:
                        dist = self.get_dist((x1, y1), (x2, y2))
                        if dist < 40:
                            mode_text = "RIGHT CLICK"
                            mode_color = "#ffff00"
                            if time.time() - self.last_click_time > 0.5:
                                pyautogui.rightClick()
                                self.last_click_time = time.time()

                    # E. LEFT CLICK LOGIC (Index+Thumb) - NO DRAG
                    elif fingers[1] == 1 and fingers[2] == 0:
                        pinch_dist = self.get_dist((x1, y1), thumb)

                        if pinch_dist < 30:
                            # Pinching: Block movement, Prepare Click
                            if not self.pinch_active:
                                self.pinch_active = True
                                self.pinch_start_time = time.time()

                            # Visual Feedback only - NO MOUSE MOVE
                            mode_text = "Click Ready..."
                            mode_color = "#ffff00"
                        else:
                            if self.pinch_active:
                                # Released
                                self.pinch_active = False
                                duration = time.time() - self.pinch_start_time

                                if duration < 0.2 and self.gestures['left_click']:
                                    pyautogui.doubleClick()
                                    mode_text = "DBL CLICK"
                                    mode_color = "#00ff00"
                                elif self.gestures['left_click']:
                                    pyautogui.click()
                                    mode_text = "CLICK"
                                    mode_color = "#00ff00"

                            # Move Cursor (Only if NOT pinching)
                            if self.gestures['move']:
                                mode_text = f"Moving ({self.active_hand_label})"
                                mode_color = "#00d4ff"
                                x3 = np.interp(x1, (self.frame_r, w - self.frame_r), (0, self.screen_w))
                                y3 = np.interp(y1, (self.frame_r, h - self.frame_r), (0, self.screen_h))
                                self.plocX += (x3 - self.plocX) / self.smoothening
                                self.plocY += (y3 - self.plocY) / self.smoothening
                                pyautogui.moveTo(self.plocX, self.plocY)

            self.status_update.emit(mode_text, mode_color)
            qimg = QImage(rgb_frame.data, w, h, w * 3, QImage.Format_RGB888)
            self.frame_ready.emit(qimg)

        cap.release()

    def stop(self):
        self.running = False
        self.voice_worker.stop()
        self.terminate()