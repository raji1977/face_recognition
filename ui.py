import tkinter as tk
from tkinter import filedialog, Label, Button
import cv2
from PIL import Image, ImageTk
from recognizer import recognize_faces, load_known_faces
import os

class FaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")
        self.root.geometry("500x500")
        self.known_encodings, self.known_names = load_known_faces()

        self.label = Label(root, text="Face Recognition", font=("Helvetica", 16))
        self.label.pack(pady=10)

        Button(root, text="Upload Image", command=self.upload, width=20, bg="#1976D2", fg="white").pack(pady=10)
        Button(root, text="Use Camera", command=self.capture, width=20, bg="#388E3C", fg="white").pack(pady=10)

        self.result = Label(root, text="", fg="green", font=("Arial", 12))
        self.result.pack(pady=20)

        self.img_label = Label(root)
        self.img_label.pack()

    def upload(self):
        path = filedialog.askopenfilename()
        if path:
            img = Image.open(path).resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.img_label.config(image=img_tk)
            self.img_label.image = img_tk

            results = recognize_faces(path, self.known_encodings, self.known_names)
            self.result.config(text="Recognized: " + ", ".join(results))

    def capture(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        img_path = "static/images/captured.jpg"
        if ret:
            cv2.imwrite(img_path, frame)
            cap.release()
            results = recognize_faces(img_path, self.known_encodings, self.known_names)
            self.result.config(text="Recognized: " + ", ".join(results))

            img = Image.open(img_path).resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.img_label.config(image=img_tk)
            self.img_label.image = img_tk
        cap.release()
