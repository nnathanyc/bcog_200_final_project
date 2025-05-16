#MAIN APP
#Main application file
#Will contain all the elements that are needed to execute the process of altering the photo
#load the image
#analyze each pixel of the image, and change accordingly to the LUT file
#display and show the option to save the final image

#CUSTOM UI
# This will be the file for the image editor GUI
# Contents for the GUI will include a home page, containing brief instructions 
# will also have a button on the bottom that says "open image"
# after the process, there will be a button that gives the user an option to save the photo
# files that will be supported will be jpg and jpeg files from the user. 
# will strive to make the UI as modern as possible, while keeping it minimalistic

import tkinter as tk
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk
from PIL import ImageEnhance, ImageFilter
import numpy as np
import os  # (to hard-code background image)

# Create background image / custom theme

# UI window (theme and dimensions)
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

# photo class to show preview, and apply filters to preview/original image
class Photo:
    def __init__(self, file_path):
        self.filepath = file_path
        self.original_image = Image.open(file_path)
        self.image = self.original_image.copy()  # Start with a copy of the original
        self.original_size = self.image.size  # Makes sure that user downloads photo in their native resolution
        self.photo = None

    # Preview function
    def show_image(self, parent_frame):
        self.parent_frame = parent_frame

        # Clear any previous image from the preview
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        preview_image = self.image.copy()  # Preview size
        preview_image.thumbnail((550, 550))  # thumbnail dimensions (doesn't apply to native resolution)

        self.photo = ImageTk.PhotoImage(preview_image)  # must store this to avoid garbage collection

        # Creating thin border around preview (black color)
        border_width = 2
        canvas_width = self.photo.width() + 2 * border_width
        canvas_height = self.photo.height() + 2 * border_width

        image_canvas = tk.Canvas(parent_frame, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
        image_canvas.pack(pady=20)

        # Centering the image (GUI)
        image_canvas.create_image(border_width, border_width, anchor='nw', image=self.photo)

        # Keep a reference to avoid garbage collection
        image_canvas.image = self.photo

        # Function for buttons under the preview (going to be assigned to different LUTs and filters)
        self.circle_filter_buttons()

    def apply_dreamy(self):
        # Reset the image to the original before applying the filter
        img = self.original_image.copy()

        # Apply stronger Gaussian blur
        img = img.filter(ImageFilter.GaussianBlur(radius=2.5))

        # Increase brightness slightly
        enhance_brightness = ImageEnhance.Brightness(img)
        img = enhance_brightness.enhance(1.3)

        # Slightly soften contrast for a dreamier look
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(0.9)

        # Increase vibrancy slightly for glow effect
        color_enhancer = ImageEnhance.Color(img)
        img = color_enhancer.enhance(1.2)

        self.image = img
        self.show_image(self.parent_frame)

    def apply_grainyfilm(self):
        img = self.original_image.copy()
        np_img = np.array(img).astype(np.int16)

        # Adding grain and artificial noise to the image
        grain = np.random.normal(loc=0, scale=25, size=np_img.shape).astype(np.int16)
        noisy_img = np.clip(np_img + grain, 0, 255).astype(np.uint8)
        img = Image.fromarray(noisy_img)

        # Reduce saturation and decrease the sharpness of colors
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.7)

        # Increase warmth in photo, boosting red colors and reducing sharp blues
        r, g, b = img.split()
        r = r.point(lambda i: min(255, i + 15)) #red modification 
        b = b.point(lambda i: max(0, i - 10))    #blue modification
        img = Image.merge("RGB", (r, g, b))

        # reduce contrast to make it look more washed and faded
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(0.85)

        self.image = img
        self.show_image(self.parent_frame)

    # Function used to create three buttons under preview of the photo
    def circle_filter_buttons(self):
        button_frame = customtkinter.CTkFrame(self.parent_frame)
        button_frame.pack(pady=10)

        # Code for the first button (soft light filter)
        button_1 = customtkinter.CTkButton(button_frame, text="Soft Light", command=self.apply_dreamy)
        button_1.pack(side=tk.LEFT, padx=10)

        # Code for the second button (film aesthetic filter)
        button_2 = customtkinter.CTkButton(button_frame, text="Washed Film", command=self.apply_grainyfilm)
        button_2.pack(side=tk.LEFT, padx=10)

        # Code for the third button (custom aesthetic filter for now) - now monotone filter
        button_3 = customtkinter.CTkButton(button_frame, text="Monotone Film", command=self.monotone_film)
        button_3.pack(side=tk.LEFT, padx=10)

    def monotone_film(self):
        img = self.original_image.copy().convert("L")  #grayscale conversion

        np_img = np.array(img).astype(np.int16)

        # adding strong noise and grain to photo to replicate vintage look
        grain = np.random.normal(loc=0, scale=35, size=np_img.shape).astype(np.int16)
        noisy_img = np.clip(np_img + grain, 0, 255).astype(np.uint8)

        img = Image.fromarray(noisy_img).convert("RGB")  

        # reducing brightness by 1.1x
        brightness = ImageEnhance.Brightness(img)
        img = brightness.enhance(0.9)

        # Reduce contrast by 1.2x
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(0.8)

        # gaussian blur to add distortion
        img = img.filter(ImageFilter.GaussianBlur(radius=1))

        self.image = img
        self.show_image(self.parent_frame)

    def save_image(self):
        # Save the image in its native resolution (regular size, no compressing)
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg *.jpeg")])
        if save_path:
            self.image.save(save_path)

# UI window 
# class for widgets and ui interactive design
class FilmEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1080x720")
        self.root.title("Film Filter App")
        self.photo = None

        # background image hard-coded from project folder
        background_path = os.path.join(os.path.dirname(__file__), "background.jpg")
        background_image = Image.open(background_path).resize((1920, 1080), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)  # <-- fixed syntax here

        # Use a label to place background image
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Place UI frame on top of background
        self.widget_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.widget_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_widgets()  # Method to create widgets

    def create_widgets(self):
        # Title and brief introduction to the program
        title_font = customtkinter.CTkFont(family="Helvetica", size=20, weight="bold")
        title = customtkinter.CTkLabel(self.widget_frame, text="Film Filter Aesthetic Application", font=title_font)
        title.pack(padx=10, pady=10)

        # Brief instructions
        instructions = customtkinter.CTkLabel(self.widget_frame, text="Upload an image, apply your filters, just a few clicks!", font=("Helvetica", 14))
        instructions.pack(padx=10, pady=5)

        # Button to upload image
        self.upload_button = customtkinter.CTkButton(self.widget_frame, text="Open Image", command=self.image_upload, width=350, height=40)
        self.upload_button.pack(pady=10)

        # Image preview frame (in widget_frame to sit over background)
        self.image_preview_frame = customtkinter.CTkFrame(self.widget_frame, fg_color="transparent")
        self.image_preview_frame.pack(pady=10)

        # Save button (initially disabled)
        self.save_btn = customtkinter.CTkButton(self.widget_frame, text="Save Image", command=self.save_image, state=tk.DISABLED, width=350, height=40)
        self.save_btn.pack(pady=10)

    # Function to embed upload image feature
    def image_upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")], title="Open Image")

        if file_path:
            self.photo = Photo(file_path)
            self.photo.show_image(self.image_preview_frame)
            self.save_btn.configure(state=tk.NORMAL)

    # Function to save image (should be after the edit)
    def save_image(self):
        if self.photo:
            self.photo.save_image()

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = FilmEditorApp(root)
    root.mainloop()
