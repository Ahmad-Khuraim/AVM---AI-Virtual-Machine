# ui.py
import os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QPropertyAnimation, QEasingCurve, QRect, QSize
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QToolButton, QFrame, QSlider, QPushButton, QCheckBox, QGraphicsDropShadowEffect, QSizePolicy
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AVM | Neural Interface")
        self.resize(1100, 700)
        self.setStyleSheet(self.qss())

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QHBoxLayout(self.central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- 1. CAMERA AREA ---
        self.camera_frame = QFrame()
        self.camera_frame.setObjectName("CameraFrame")
        self.camera_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cam_layout = QVBoxLayout(self.camera_frame)
        self.cam_layout.setContentsMargins(0, 0, 0, 0)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setScaledContents(True)
        self.cam_layout.addWidget(self.video_label)
        self.main_layout.addWidget(self.camera_frame)

        # --- 2. SIDEBAR ---
        self.sidebar = QFrame(self.central)
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setGeometry(0, 0, 280, 700)

        self.side_layout = QVBoxLayout(self.sidebar)
        self.side_layout.setContentsMargins(20, 25, 20, 25)
        self.side_layout.setSpacing(15)
        self.side_layout.setAlignment(Qt.AlignTop)

        # Header
        header_layout = QHBoxLayout()
        self.menu_btn = QPushButton("☰")
        self.menu_btn.setObjectName("menuBtn")
        self.menu_btn.setFixedSize(40, 40)
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        self.menu_btn.clicked.connect(self.toggle_sidebar)

        self.menu_label = QLabel("AVM Control")
        self.menu_label.setObjectName("headerTitle")

        header_layout.addWidget(self.menu_btn)
        header_layout.addWidget(self.menu_label)
        header_layout.addStretch()
        self.side_layout.addLayout(header_layout)

        # Controls Container
        self.controls_container = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_container)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_layout.setSpacing(15)

        # A. STATUS BOX
        self.status_box = QLabel("Idle")
        self.status_box.setObjectName("SidebarStatus")
        self.status_box.setAlignment(Qt.AlignCenter)
        self.status_box.setFixedHeight(60)
        self.controls_layout.addWidget(self.status_box)

        # --- HELPER FOR ICONS ---
        def get_icon(name):
            path = f"Assets/{name}"
            if os.path.exists(path): return QIcon(path)
            return QIcon()

        # B. PRIMARY ICONS ROW
        icon_row = QHBoxLayout()
        icon_row.setSpacing(15)

        self.btn_index = QPushButton()
        self.btn_index.setIcon(get_icon("index.png"))
        self.btn_index.setIconSize(QSize(30, 30))
        self.btn_index.setObjectName("circleBtn")
        self.btn_index.setFixedSize(60, 60)
        self.btn_index.clicked.connect(self.swap_hand_ui)

        self.btn_mic = QPushButton()
        self.btn_mic.setIcon(get_icon("mic.png"))
        self.btn_mic.setIconSize(QSize(35, 35))
        self.btn_mic.setObjectName("micBtn")
        self.btn_mic.setFixedSize(70, 70)
        self.btn_mic.setCheckable(True)
        self.btn_mic.clicked.connect(self.toggle_voice_ui)

        self.btn_fist = QPushButton()
        self.btn_fist.setIcon(get_icon("fist.png"))
        self.btn_fist.setIconSize(QSize(30, 30))
        self.btn_fist.setObjectName("circleBtn")
        self.btn_fist.setFixedSize(60, 60)
        self.btn_fist.setCheckable(True)
        self.btn_fist.setChecked(True)
        self.btn_fist.clicked.connect(lambda: self.toggle_gesture_ui(self.btn_fist, "drag"))

        icon_row.addWidget(self.btn_index)
        icon_row.addWidget(self.btn_mic)
        icon_row.addWidget(self.btn_fist)
        self.controls_layout.addLayout(icon_row)

        # --- HIDDEN EXTRA ICONS (Placed BEFORE More Button) ---
        self.extra_icons_frame = QFrame()
        self.extra_icons_frame.setVisible(False)
        extra_layout = QHBoxLayout(self.extra_icons_frame)
        extra_layout.setSpacing(15)
        extra_layout.setContentsMargins(0, 0, 0, 0)

        # Updated Filenames here
        self.btn_four = QPushButton()
        self.btn_four.setIcon(get_icon("four finger(index,middle,ring,little).png"))
        self.btn_four.setIconSize(QSize(30, 30))
        self.btn_four.setObjectName("circleBtn")
        self.btn_four.setFixedSize(50, 50)
        self.btn_four.setCheckable(True)
        self.btn_four.setChecked(True)
        self.btn_four.clicked.connect(lambda: self.toggle_gesture_ui(self.btn_four, "four_finger"))

        self.btn_pinch = QPushButton()
        self.btn_pinch.setIcon(get_icon("index+thumb.png"))
        self.btn_pinch.setIconSize(QSize(30, 30))
        self.btn_pinch.setObjectName("circleBtn")
        self.btn_pinch.setFixedSize(50, 50)
        self.btn_pinch.setCheckable(True)
        self.btn_pinch.setChecked(True)
        self.btn_pinch.clicked.connect(lambda: self.toggle_gesture_ui(self.btn_pinch, "left_click"))

        self.btn_mid = QPushButton()
        self.btn_mid.setIcon(get_icon("index+middle.png"))
        self.btn_mid.setIconSize(QSize(30, 30))
        self.btn_mid.setObjectName("circleBtn")
        self.btn_mid.setFixedSize(50, 50)
        self.btn_mid.setCheckable(True)
        self.btn_mid.setChecked(True)
        self.btn_mid.clicked.connect(lambda: self.toggle_gesture_ui(self.btn_mid, "right_click"))

        extra_layout.addWidget(self.btn_four)
        extra_layout.addWidget(self.btn_pinch)
        extra_layout.addWidget(self.btn_mid)
        self.controls_layout.addWidget(self.extra_icons_frame)

        # C. MORE BUTTON (After Extra Icons so it pushes down)
        self.btn_more = QPushButton("More ᐯ")
        self.btn_more.setObjectName("pillBtn")
        self.btn_more.setFixedHeight(30)
        self.btn_more.clicked.connect(self.toggle_extra_icons)
        self.controls_layout.addWidget(self.btn_more)

        self.controls_layout.addSpacing(10)

        # D. SLIDERS
        self.controls_layout.addWidget(QLabel("Cursor Sensitivity"))
        self.sens_slider = QSlider(Qt.Horizontal)
        self.sens_slider.setRange(10, 30)
        self.sens_slider.setValue(15)
        self.controls_layout.addWidget(self.sens_slider)

        self.controls_layout.addWidget(QLabel("Smoothing"))
        self.resp_slider = QSlider(Qt.Horizontal)
        self.resp_slider.setRange(1, 20)
        self.resp_slider.setValue(5)
        self.controls_layout.addWidget(self.resp_slider)

        self.controls_layout.addStretch()

        # E. COMMANDS
        self.cmd_frame = QFrame()
        self.cmd_frame.setVisible(False)
        cmd_layout = QVBoxLayout(self.cmd_frame)
        cmd_txt = QLabel(
            "• Index Move: Swap Hand\n"
            "• Pinch < 0.2s: Dbl Click\n"
            "• Fist: Drag & Drop\n"
            "• 4 Fingers: Toggle UI\n"
            "• 2 Hands Index: Volume"
        )
        cmd_txt.setStyleSheet("color: #aaa; background: #252525; padding: 10px; border-radius: 10px; font-size: 12px;")
        cmd_layout.addWidget(cmd_txt)
        self.controls_layout.addWidget(self.cmd_frame)

        self.btn_cmd = QPushButton("Commands")
        self.btn_cmd.setObjectName("pillBtnOutline")
        self.btn_cmd.setFixedHeight(45)
        self.btn_cmd.clicked.connect(self.toggle_commands)
        self.controls_layout.addWidget(self.btn_cmd)

        self.side_layout.addWidget(self.controls_container)

        # --- 3. OVERLAY PILL ---
        self.overlay_pill = QLabel("System Ready", self.central)
        self.overlay_pill.setObjectName("OverlayPill")
        self.overlay_pill.setAlignment(Qt.AlignCenter)
        self.overlay_pill.show()

        # Animation
        self.anim = QPropertyAnimation(self.sidebar, b"geometry")
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.is_open = True
        self.sidebar_w = 280
        self.worker = None
        self.is_hidden_mode = False

    def resizeEvent(self, event):
        h = self.height()
        # Sidebar Geometry update
        if self.is_open:
            self.sidebar.setGeometry(0, 0, self.sidebar_width, h)
        else:
            self.sidebar.setGeometry(0, 0, 70, h)

        # Center Pill update
        pill_w = 160
        center_x = (self.width() - pill_w) // 2
        self.overlay_pill.setGeometry(center_x, 30, pill_w, 40)
        super().resizeEvent(event)

    @property
    def sidebar_width(self):
        return 280

    def set_worker(self, worker):
        self.worker = worker
        worker.frame_ready.connect(self.update_frame)
        worker.status_update.connect(self.update_status)
        self.resp_slider.valueChanged.connect(lambda v: setattr(worker, 'smoothening', v))
        self.sens_slider.valueChanged.connect(lambda v: setattr(worker, 'sensitivity', v / 10))

    def toggle_voice_ui(self, checked):
        if self.worker:
            state = Qt.Checked if checked else Qt.Unchecked
            self.worker.toggle_voice(state)

        if checked:
            self.btn_mic.setStyleSheet("background-color: #1e1e1e; border: 2px solid #00ff00; border-radius: 35px;")
            self.status_box.setText("Listening...")
            self.status_box.setStyleSheet(
                "background-color: #004400; color: #00ff00; border-radius: 15px; font-weight: bold; font-size: 18px;")
        else:
            self.btn_mic.setStyleSheet("")
            self.status_box.setText("Idle")
            self.status_box.setStyleSheet(
                "background-color: black; color: white; border-radius: 15px; font-weight: bold; font-size: 18px;")

    def toggle_gesture_ui(self, btn, gesture):
        if self.worker:
            self.worker.toggle_gesture(gesture)
            if self.worker.gestures[gesture]:
                btn.setStyleSheet("")
                btn.setAlpha(1.0)
            else:
                btn.setStyleSheet("background-color: #222; border: 1px solid #444; color: #555;")

    def swap_hand_ui(self):
        if self.worker:
            self.worker.toggle_hand()

    def toggle_extra_icons(self):
        if self.extra_icons_frame.isVisible():
            self.extra_icons_frame.setVisible(False)
            self.btn_more.setText("More ᐯ")
        else:
            self.extra_icons_frame.setVisible(True)
            self.btn_more.setText("Less ᐱ")

    def toggle_commands(self):
        if self.cmd_frame.isVisible():
            self.cmd_frame.hide()
        else:
            self.cmd_frame.show()

    def toggle_sidebar(self):
        h = self.height()
        if self.is_open:
            start = QRect(0, 0, self.sidebar_width, h)
            end = QRect(0, 0, 70, h)
            self.menu_btn.setText("☰")
            self.menu_label.hide()
            self.controls_container.hide()
        else:
            start = QRect(0, 0, 70, h)
            end = QRect(0, 0, self.sidebar_width, h)
            self.menu_btn.setText("✕")
            QtCore.QTimer.singleShot(150, lambda: self.menu_label.show())
            QtCore.QTimer.singleShot(150, lambda: self.controls_container.show())

        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()
        self.is_open = not self.is_open

    @Slot(QImage)
    def update_frame(self, qimg):
        pix = QPixmap.fromImage(qimg)
        self.video_label.setPixmap(pix.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    @Slot(str, str)
    def update_status(self, text, color):
        if text == "TOGGLE_UI":
            if self.is_hidden_mode:
                self.sidebar.show()
                self.overlay_pill.show()
            else:
                self.sidebar.hide()
                self.overlay_pill.hide()
            self.is_hidden_mode = not self.is_hidden_mode
            return

        if text == "TOGGLE_SLEEP":
            if self.isHidden():
                self.showNormal()
            else:
                self.showMinimized()
            return

        self.overlay_pill.setText(text)
        self.overlay_pill.setStyleSheet(f"""
            background-color: rgba(0, 0, 0, 0.7);
            color: {color};
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        """)

        if not self.btn_mic.isChecked():
            self.status_box.setText(text)

    def qss(self):
        return """
        QMainWindow { background-color: #121212; }
        QLabel { color: white; font-family: 'Segoe UI', sans-serif; }
        #Sidebar { background-color: #1e1e1e; border-right: 1px solid #333; }
        #menuBtn { background: transparent; color: white; border: none; font-size: 24px; }
        #headerTitle { font-size: 20px; font-weight: bold; color: #eee; }
        #SidebarStatus { background-color: black; border-radius: 15px; font-size: 18px; font-weight: bold; color: white; border: 1px solid #333; }
        #circleBtn { background-color: #2d2d2d; border-radius: 25px; border: none; }
        #circleBtn:checked { background-color: #3d3d3d; border: 1px solid #555; }
        #micBtn { background-color: #eee; color: black; border-radius: 35px; border: none; }
        #pillBtn { background-color: #2d2d2d; border-radius: 15px; font-size: 12px; color: #ddd; }
        #pillBtnOutline { background-color: transparent; border: 1px solid #444; border-radius: 20px; font-size: 14px; color: #ddd; }
        QSlider::groove:horizontal { height: 4px; background: #444; border-radius: 2px; }
        QSlider::handle:horizontal { background: #00d4ff; width: 16px; height: 16px; margin: -6px 0; border-radius: 8px; }
        #OverlayPill { background-color: rgba(0,0,0,0.6); color: white; border-radius: 20px; }
        """