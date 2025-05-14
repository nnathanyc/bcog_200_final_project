#This will be the file for the image editor GUI
#Contents for the GUI will include a home page, containing brief instructions 
#will also have a button on the bottom that says "open image"
#after the process, there will be a button that gives the user an option to save the photo
#files that will be supported will be jpg and jpeg files from the user. 
#will strive to make the UI as modern as possible, while keeping it minimalistic

import tkinter as tk
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk
import numpy as np

#Create background image / custom theme 

#ui window (theme and dimensions)
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Separate Photo class (not nested)
class Photo:
    def __init__(self, file_path):
        self.filepath = file_path
        self.image = Image.open(file_path)
        self.photo = None

    #preview function
    def show_image(self, parent_frame):
        
        self.parent_frame = parent_frame 

        self.image.thumbnail((550, 550)) #preview size
        self.photo = ImageTk.PhotoImage(self.image)

        #creating thin border around preview
        border_width = 2
        canvas_width = self.photo.width() + 2 * border_width
        canvas_height = self.photo.height() + 2 * border_width

        image_canvas = tk.Canvas(parent_frame, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
        image_canvas.pack(pady=20)

        #centering the image (gui)
        image_canvas.create_image(border_width, border_width, anchor='nw', image=self.photo)

        # Keep a reference to avoid garbage collection
        image_canvas.image = self.photo

        # function for buttons under the preview (going to be assigned to different luts and filters)
        self.circle_filter_buttons()

    #Function used to create three buttons under preview of the photo
    
    def circle_filter_buttons(self):
        button_frame = customtkinter.CTkFrame(self.parent_frame)
        button_frame.pack(pady=10)

        #code for the first button (soft light filter)
        button_1 = customtkinter.CTkButton(button_frame, text = "soft light", command=self.placeholder_action)
        button_1.pack(side=tk.LEFT,padx=10)

        #code for the second button (film aesthetic filter)
        button_2 = customtkinter.CTkButton(button_frame, text = "film aesthetic", command=self.placeholder_action)
        button_2.pack(side=tk.LEFT,padx=10)

        #code for the third button (custom aesthetic filter for now)
        button_2 = customtkinter.CTkButton(button_frame, text = "custom aesthetic", command=self.placeholder_action)
        button_2.pack(side=tk.LEFT,padx=10)

    def placeholder_action(self):
        # Placeholder function for button actions
        pass

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg *.jpeg")])
        if save_path:
            self.image.save(save_path)

#ui window 
class FilmEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1980x1080")
        self.root.title("Film Filter Aesthetic Application")
        
        self.photo = None

        self.create_widgets() #Method to create widgets
    
    def create_widgets(self):
        #Title and brief introduction to the program
        title_font = customtkinter.CTkFont(family="Helvetica", size=20, weight="bold")
        title = customtkinter.CTkLabel(self.root, text="Film Filter Aesthetic Application", font=title_font)
        title.pack(padx=10, pady=10)

        #brief instructions
        instructions = customtkinter.CTkLabel(self.root, text="Upload an image, apply your filters, just a few clicks!", font=("Helvetica", 14))
        instructions.pack(padx=10, pady=5)

        #button to upload image
        self.upload_button = customtkinter.CTkButton(self.root, text="Open Image", command=self.image_upload, width=350, height=40)
        self.upload_button.pack(pady=10)

        #save button (initially disabled)
        self.save_btn = customtkinter.CTkButton(self.root, text="Save Image", command=self.save_image, state=tk.DISABLED, width=350, height=40)
        self.save_btn.pack(pady=10)

    #function to embed upload image feature
    def image_upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")], title="Open Image")

        if file_path:
            self.photo = Photo(file_path)
            self.photo.show_image(self.root)
            self.save_btn.configure(state=tk.NORMAL)

    #function to save image(should be after the edit)
    def save_image(self):
        if self.photo:
            self.photo.save_image()

    
    #function to apply lut(cubefile) photos
    


# main loop to launch the GUI
if __name__ == "__main__":
    root = customtkinter.CTk()
    app = FilmEditorApp(root)
    root.mainloop()
