import tkinter as tk
import cv2
import numpy as np
import datetime
from PIL import Image, ImageTk


class App:
    def __init__(self, master):
        self.master = master
        self.cap = cv2.VideoCapture(0)

        # Set the resolution of the camera to 1:1 ratio
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.btn_capture = tk.Button(self.master, text="Capture", command=self.capture)
        self.btn_capture.pack(pady=10)

        # Create a label to display the video feed
        self.lbl_video = tk.Label(self.master)
        self.lbl_video.pack()

        # Create a label to display the counter
        self.lbl_counter = tk.Label(self.master, text="0")
        self.lbl_counter.pack(pady=5)

        # Create a button to take the next photo
        self.btn_next = tk.Button(self.master, text="Next", command=self.next_photo)
        self.btn_next.pack(pady=5)

        self.photo_counter = 0
        self.update_video_feed()

    def update_video_feed(self):
        # Get a frame from the video feed
        ret, frame = self.cap.read()

        # Resize the frame to fit in the label
        frame = cv2.resize(frame, (640, 480))

        # Convert the frame to an RGB image and display it in the label
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.lbl_video.img = img
        self.lbl_video.configure(image=img)

        # Schedule the next update of the video feed
        self.lbl_video.after(10, self.update_video_feed)

    def capture(self):
        ret, frame = self.cap.read()

        # Crop the frame to a square shape
        h, w, _ = frame.shape
        size = min(h, w)
        x = (w - size) // 2
        y = (h - size) // 2
        frame = frame[y:y + size, x:x + size]

        # Resize the frame to 720x720 resolution
        frame = cv2.resize(frame, (720, 720))

        # Get the current date and time
        now = datetime.datetime.now()
        date_time = now.strftime("%Y%m%d_%H%M%S")

        # Save the image with a unique name containing the date and time
        filename = f"captured_image_{date_time}_{self.photo_counter}.jpg"
        cv2.imwrite(filename, frame)

        self.photo_counter += 1
        self.lbl_counter.configure(text=str(self.photo_counter))

    def next_photo(self):
        self.lbl_counter.configure(text="0")
        self.photo_counter = 0

    def __del__(self):
        self.cap.release()


root = tk.Tk()
app = App(root)
root.mainloop()
