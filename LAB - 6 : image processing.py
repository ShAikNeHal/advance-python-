import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np


class ImageEditor:

    def __init__(self, root):

        self.root = root
        self.root.title("Mini Image Editing Studio")
        self.root.geometry("1300x750")

        self.original = None
        self.processed = None

        ##########################
        # LEFT IMAGE PANEL
        ##########################

        self.left = tk.Frame(root, bg="gray")
        self.left.pack(side="left", fill="both", expand=True)

        self.image_label = tk.Label(self.left, bg="gray")
        self.image_label.pack(expand=True)

        ##########################
        # RIGHT CONTROL PANEL
        ##########################

        right = tk.Frame(root)
        right.pack(side="right", fill="y")

        canvas = tk.Canvas(right, width=320)
        scrollbar = tk.Scrollbar(right, orient="vertical", command=canvas.yview)

        self.control_frame = tk.Frame(canvas)

        self.control_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.control_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ##########################
        # Buttons
        ##########################

        tk.Button(
            self.control_frame,
            text="Upload Image",
            command=self.load_image,
            width=20,
            bg="lightgreen"
        ).pack(pady=10)

        self.make_slider("Brightness", -100, 100, 0)
        self.make_slider("Contrast", 0, 300, 100)
        self.make_slider("Gaussian Blur", 0, 20, 0)
        self.make_slider("Rotation", -180, 180, 0)
        self.make_slider("Zoom", 50, 200, 100)
        self.make_slider("Sharpen", 0, 10, 0)
        self.make_slider("Saturation", 0, 300, 100)
        self.make_slider("Hue", -180, 180, 0)

        tk.Button(
            self.control_frame,
            text="Reset",
            command=self.reset,
            bg="orange",
            width=20
        ).pack(pady=10)

        tk.Button(
            self.control_frame,
            text="Save Image",
            command=self.save_image,
            bg="lightblue",
            width=20
        ).pack(pady=10)

    #####################################################

    def make_slider(self, text, start, end, default):

        label = tk.Label(self.control_frame, text=text)
        label.pack()

        scale = tk.Scale(
            self.control_frame,
            from_=start,
            to=end,
            orient="horizontal",
            length=250,
            command=lambda x: self.update_image()
        )

        scale.set(default)
        scale.pack()

        setattr(self, text.replace(" ", "_").lower(), scale)

    #####################################################

    def load_image(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.jpg *.png *.jpeg *.bmp")
            ]
        )

        if path == "":
            return

        img = cv2.imread(path)

        self.original = img
        self.processed = img.copy()

        self.update_image()

    #####################################################

    def update_image(self):

        if self.original is None:
            return

        img = self.original.copy()

        ###################################
        # Brightness & Contrast
        ###################################

        brightness = self.brightness.get()
        contrast = self.contrast.get() / 100

        img = cv2.convertScaleAbs(
            img,
            alpha=contrast,
            beta=brightness
        )

        ###################################
        # Gaussian Blur
        ###################################

        blur = self.gaussian_blur.get()

        if blur > 0:
            k = blur * 2 + 1
            img = cv2.GaussianBlur(img, (k, k), 0)

        ###################################
        # Saturation + Hue
        ###################################

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        sat = self.saturation.get() / 100

        hsv[:, :, 1] = np.clip(
            hsv[:, :, 1] * sat,
            0,
            255
        )

        hue = self.hue.get()

        hsv[:, :, 0] = (
            hsv[:, :, 0].astype(int) + hue
        ) % 180

        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        ###################################
        # Sharpen
        ###################################

        sharp = self.sharpen.get()

        if sharp > 0:

            kernel = np.array([
                [0, -1, 0],
                [-1, 5 + sharp, -1],
                [0, -1, 0]
            ])

            img = cv2.filter2D(img, -1, kernel)

        ###################################
        # Rotation
        ###################################

        angle = self.rotation.get()

        h, w = img.shape[:2]

        M = cv2.getRotationMatrix2D(
            (w / 2, h / 2),
            angle,
            1
        )

        img = cv2.warpAffine(img, M, (w, h))

        ###################################
        # Zoom
        ###################################

        zoom = self.zoom.get() / 100

        img = cv2.resize(
            img,
            None,
            fx=zoom,
            fy=zoom
        )

        self.processed = img

        self.display(img)

    #####################################################

    def display(self, img):

        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(image)

        image.thumbnail((850, 650))

        imgtk = ImageTk.PhotoImage(image)

        self.image_label.configure(image=imgtk)

        self.image_label.image = imgtk

    #####################################################

    def reset(self):

        if self.original is None:
            return

        self.brightness.set(0)
        self.contrast.set(100)
        self.gaussian_blur.set(0)
        self.rotation.set(0)
        self.zoom.set(100)
        self.sharpen.set(0)
        self.saturation.set(100)
        self.hue.set(0)

        self.update_image()

    #####################################################

    def save_image(self):

        if self.processed is None:
            return

        file = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("BMP", "*.bmp")
            ]
        )

        if file:
            cv2.imwrite(file, self.processed)


##############################################################

root = tk.Tk()

app = ImageEditor(root)

root.mainloop()
