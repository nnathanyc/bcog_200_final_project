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


#ui window

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1920x1080")
app.title("Film Filter Application")

#Background image for theme

custom_background = Image.open("your_wallpaper.jpg")  # Replace with your image file
custom_background = custom_background.resize((1920, 1080), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(custom_background)


#Function to upload image

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")], title="Select an Image")

#adding ui elements
title_font = customtkinter.CTkFont(family="Helvetica", size=20, weight="bold")
title = customtkinter.CTkLabel(app, text='Upload Image', font=title_font)
title.pack(padx=10, pady=10)

upload_btn = customtkinter.CTkButton(app, text="Open Image", command=upload_image)
upload_btn.pack(pady=10)


#photo upload input (copy link first then transform it to upload function)

link=customtkinter.CTkEntry(app, width=350, height=40)
link.pack()









#keep app running
app.mainloop()