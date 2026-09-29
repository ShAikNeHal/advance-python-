import cv2
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import numpy as np

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Image Studio")
        self.root.geometry("1100x700")

        self.original_image = None
        self.processed_image = None
        
        # UI Layout
        self.left_frame = tk.Frame(root, width=700)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.left_frame, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(root, width=300)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollable Control Area
        self.scroll_canvas = tk.Canvas(self.right_frame)
        self.scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.scroll_canvas.yview)
        self.controls = tk.Frame(self.scroll_canvas)
        
        self.controls.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 0), window=self.controls, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        tk.Button(self.controls, text="Upload Image", command=self.upload_image).pack(fill=tk.X)
        tk.Button(self.controls, text="Reset", command=self.reset_image).pack(fill=tk.X)
        tk.Button(self.controls, text="Save Image", command=self.save_image).pack(fill=tk.X)

        # Sliders
        self.sliders = {}
        self.add_slider("Brightness", 0, 200, 100)
        self.add_slider("Contrast", 0, 200, 100)
        self.add_slider("Blur", 0, 50, 0)
        self.add_slider("Rotation", 0, 360, 0)
        self.add_slider("Zoom", 50, 150, 100)
        self.add_slider("Saturation", 0, 200, 100)
        self.add_slider("Hue", 0, 180, 0)

    def add_slider(self, label, min_val, max_val, default):
        tk.Label(self.controls, text=label).pack()
        slider = tk.Scale(self.controls, from_=min_val, to=max_val, orient=tk.HORIZONTAL, command=self.apply_processing)
        slider.set(default)
        slider.pack(fill=tk.X)
        self.sliders[label] = slider

    def upload_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_image = cv2.imread(path)
            self.apply_processing()

    def apply_processing(self, event=None):
        if self.original_image is None: return
        
        img = self.original_image.copy()

        # Adjustments
        brightness = self.sliders["Brightness"].get() / 100
        contrast = self.sliders["Contrast"].get() / 100
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=(brightness-1)*100)

        # Blur
        blur_val = self.sliders["Blur"].get()
        if blur_val > 0:
            img = cv2.GaussianBlur(img, (blur_val*2+1, blur_val*2+1), 0)

        # Rotate
        rows, cols = img.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2, rows/2), self.sliders["Rotation"].get(), 1)
        img = cv2.warpAffine(img, M, (cols, rows))

        # Zoom
        zoom = self.sliders["Zoom"].get() / 100
        img = cv2.resize(img, None, fx=zoom, fy=zoom)
        img = img[0:rows, 0:cols] if zoom > 1 else img

        # Color Space (Hue/Sat)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")
        hsv[:,:,1] = hsv[:,:,1] * (self.sliders["Saturation"].get() / 100)
        hsv[:,:,0] = (hsv[:,:,0] + self.sliders["Hue"].get()) % 180
        img = cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

        self.processed_image = img
        self.display_image(img)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil.resize((600, 500)))
        self.canvas.create_image(350, 250, image=img_tk)
        self.canvas.image = img_tk

    def reset_image(self):
        for s in self.sliders.values(): s.set(100 if "Blur" not in str(s) and "Rotation" not in str(s) and "Hue" not in str(s) else 0)
        self.apply_processing()

    def save_image(self):
        if self.processed_image is not None:
            path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if path: cv2.imwrite(path, self.processed_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
