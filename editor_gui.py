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

#Create background image / custom theme 



#ui window (theme and dimensions)

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

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
        title = customtkinter.CTkLabel(self.root, text="Film Filter Aesthetic Application", font=title_font )
        title.pack(padx=10, pady=10)

        #brief instructions
        instructions = customtkinter.CTkLabel(self.root, text="Upload an image, apply your filters, and save it!", font=("Helvetica", 14))
        instructions.pack(padx=10, pady=5)

        #button to upload image
        self.upload_button = customtkinter.CTkButton(self.root, text="Open Image", command=self.upload_image, width=350, height=40)
        self.upload_button.pack(pady=10)
    
    #function to embedd uplaod image feature in 
    def image_upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")], title="Open Image")

        if file_path:
            self.photo = Photo(file_path)
            
        

    

    

app = customtkinter.CTk()
app.geometry("1920x1080")
app.title("Film Filter Quick Tool")

#preview image function and its frame

image_canvas = None
photo = None

#Function to upload image

def upload_image():
    global image_canvas, photo
    file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")], title="Select an Image")

    if file_path:
        image = Image.open(file_path) #opens image preview from filepath
        image.thumbnail((550, 550)) #size of the image preview
        photo = ImageTk.PhotoImage(image)

    if image_canvas:
        image_canvas.destroy()
    
    #creating the image border (canvas), thin white profile
    border_width = 2
    canvas_width = photo.width() + 2 * border_width
    canvas_height = photo.height() + 2 * border_width
    
    image_canvas = tk.Canvas(app, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
    image_canvas.pack(pady=20)

    #centering the canvas so it looks like a border
    image_canvas.create_image(border_width, border_width, anchor='nw', image=photo)

    
#adding ui elements (keep in the middle of the screen )
title_font = customtkinter.CTkFont(family="Helvetica", size=20, weight="bold")
title = customtkinter.CTkLabel(app, text='Upload Image', font=title_font)
title.pack(padx=10, pady=10)

upload_btn = customtkinter.CTkButton(app, text="Open Image", command=upload_image, width=350, height=40)
upload_btn.pack(pady=10)


#photo upload input (copy link first then transform it to upload function)

link=customtkinter.CTkEntry(app, width=350, height=40)
link.pack()









#keep app running
app.mainloop()