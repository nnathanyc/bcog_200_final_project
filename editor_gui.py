#This will be the file for the image editor GUI
#Contents for the GUI will include a home page, containing brief instructions 
#will also have a button on the bottom that says "open image"
#after the process, there will be a button that gives the user an option to save the photo
#files that will be supported will be jpg and jpeg files from the user. 
#will strive to make the UI as modern as possible, while keeping it minimalistic

import tkinter as tk
import customtkinter

#ui design

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1920x1080")
app.title("Film Photography Assistant")

#adding ui elements

title = customtkinter.CTkLabel


#keep app running
app.mainloop()