import cv2
import os
import uuid
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

# Configuration
IMAGES_PATH = 'path/to/save/images'  # Replace with your actual path
os.makedirs(IMAGES_PATH, exist_ok=True)

class ImageCollectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Collector")
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            self.root.destroy()
        
        self.label = tk.Label(root)
        self.label.pack()
        
        self.class_name = tk.StringVar()
        self.class_entry = tk.Entry(root, textvariable=self.class_name)
        self.class_entry.pack()
        
        self.capture_button = tk.Button(root, text="Capture Image", command=self.capture_image)
        self.capture_button.pack()
        
        self.root.bind('<space>', self.capture_image_event)
        
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        self.root.after(10, self.update_frame)

    def capture_image(self):
        class_name = self.class_name.get()
        if not class_name:
            print("Please enter a class name.")
            return
        
        imgname = os.path.join(IMAGES_PATH, class_name, f'{class_name}.{uuid.uuid1()}.jpg')
        os.makedirs(os.path.dirname(imgname), exist_ok=True)
        cv2.imwrite(imgname, self.current_frame)
        print(f"Image saved: {imgname}")

    def capture_image_event(self, event):
        self.capture_image()

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCollectorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
