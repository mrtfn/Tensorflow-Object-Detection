import sys
import cv2
import os
import uuid
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
                             QLineEdit, QInputDialog)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

# Configuration
IMAGES_PATH = 'path/to/save/images'  # Replace with your actual path
os.makedirs(IMAGES_PATH, exist_ok=True)

class ImageCollectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            self.close()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Update the frame every 20ms

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

    def initUI(self):
        self.setWindowTitle('Image Collector')
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        
        self.class_names_entry = QLineEdit(self)
        self.class_names_entry.setPlaceholderText("Enter class names, separated by commas")
        self.layout.addWidget(self.class_names_entry)
        
        self.repeat_count_entry = QLineEdit(self)
        self.repeat_count_entry.setPlaceholderText("Enter number of images per class")
        self.layout.addWidget(self.repeat_count_entry)

        self.countdown_entry = QLineEdit(self)
        self.countdown_entry.setPlaceholderText("Enter countdown seconds")
        self.layout.addWidget(self.countdown_entry)
        
        self.capture_button = QPushButton('Start Capture', self)
        self.capture_button.clicked.connect(self.start_capture)
        self.layout.addWidget(self.capture_button)

        self.countdown_label = QLabel(self)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.countdown_label)
        
        self.setLayout(self.layout)
        self.show()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
            self.label.setPixmap(pixmap)

    def start_capture(self):
        class_names = self.class_names_entry.text().split(',')
        self.class_names = [name.strip() for name in class_names if name.strip()]
        try:
            self.repeat_count = int(self.repeat_count_entry.text())
            self.countdown_seconds = int(self.countdown_entry.text())
        except ValueError:
            print("Please enter valid numbers for repeat count and countdown seconds.")
            return

        if not self.class_names or self.repeat_count <= 0 or self.countdown_seconds <= 0:
            print("Please enter valid class names, repeat count, and countdown seconds.")
            return
        
        self.current_class_index = 0
        self.current_repeat_count = 0
        self.current_countdown = self.countdown_seconds
        self.start_next_capture()

    def start_next_capture(self):
        if self.current_class_index < len(self.class_names):
            self.class_name = self.class_names[self.current_class_index]
            if self.current_repeat_count < self.repeat_count:
                self.current_countdown = self.countdown_seconds
                self.countdown_label.setText(str(self.current_countdown))
                self.countdown_timer.start(1000)  # Update countdown every second
            else:
                self.current_class_index += 1
                self.current_repeat_count = 0
                self.start_next_capture()
        else:
            self.countdown_label.setText("Capture Complete")
            self.current_class_index = 0
            self.current_repeat_count = 0

    def update_countdown(self):
        if self.current_countdown > 0:
            self.current_countdown -= 1
            self.countdown_label.setText(str(self.current_countdown))
        else:
            self.countdown_timer.stop()
            self.capture_image()
            self.current_repeat_count += 1
            self.start_next_capture()

    def capture_image(self):
        if not self.class_name:
            print("Please enter a class name.")
            return
        
        imgname = os.path.join(IMAGES_PATH, self.class_name, f'{self.class_name}.{uuid.uuid1()}.jpg')
        os.makedirs(os.path.dirname(imgname), exist_ok=True)
        cv2.imwrite(imgname, self.current_frame)
        print(f"Image saved: {imgname}")

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageCollectorApp()
    sys.exit(app.exec_())
