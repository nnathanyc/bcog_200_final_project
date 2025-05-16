import tkinter as tk
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np

# Set theme
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


# --- Photo Class ---
class Photo:
    def __init__(self, file_path):
        self.filepath = file_path
        self.image = Image.open(file_path)
        self.original_image = self.image.copy()  # Store original for reapplying filters
        self.original_size = self.image.size     # For saving in native resolution
        self.filtered_image_fullres = self.original_image.copy()  # Placeholder for full-res filtered version
        self.photo = None
        self.parent_frame = None

    def show_image(self, parent_frame, on_preview_ready=None):
        self.parent_frame = parent_frame

        # Clear previous preview
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Resize for preview (not for saving)
        preview_image = self.image.copy()
        preview_image.thumbnail((550, 550))
        self.photo = ImageTk.PhotoImage(preview_image)

        # Canvas with border
        border_width = 2
        canvas_width = self.photo.width() + 2 * border_width
        canvas_height = self.photo.height() + 2 * border_width

        image_canvas = tk.Canvas(parent_frame, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
        image_canvas.pack(pady=20)
        image_canvas.create_image(border_width, border_width, anchor='nw', image=self.photo)
        image_canvas.image = self.photo  # Prevent garbage collection

        self.circle_filter_buttons()

        if on_preview_ready:
            on_preview_ready()

    def apply_dreamy(self):
        img = self.original_image.copy()
        img = img.filter(ImageFilter.GaussianBlur(radius=2))

        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)

        colorenhancer = ImageEnhance.Color(img)
        img = colorenhancer.enhance(1.1)

        self.image = img
        self.filtered_image_fullres = img.copy()
        self.show_image(self.parent_frame)

    def apply_grainyfilm(self):
        img = self.original_image.copy()
        np_img = np.array(img)

        grain = np.random.normal(loc=0, scale=20, size=np_img.shape).astype(np.int16)
        noisy_img = np_img + grain
        noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)

        filtered_img = Image.fromarray(noisy_img)
        self.image = filtered_img
        self.filtered_image_fullres = filtered_img.copy()
        self.show_image(self.parent_frame)

    def placeholder_action(self):
        # Placeholder for future filter
        pass

    def circle_filter_buttons(self):
        button_frame = customtkinter.CTkFrame(self.parent_frame)
        button_frame.pack(pady=10)

        button_1 = customtkinter.CTkButton(button_frame, text="SoftLight", command=self.apply_dreamy)
        button_1.pack(side=tk.LEFT, padx=10)

        button_2 = customtkinter.CTkButton(button_frame, text="GrainyFilm", command=self.apply_grainyfilm)
        button_2.pack(side=tk.LEFT, padx=10)

        button_3 = customtkinter.CTkButton(button_frame, text="Custom Aesthetic", command=self.placeholder_action)
        button_3.pack(side=tk.LEFT, padx=10)

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg *.jpeg")])
        if save_path:
            if hasattr(self, 'filtered_image_fullres'):
                self.filtered_image_fullres.save(save_path)
            else:
                self.original_image.save(save_path)


# --- Main App Class ---
class FilmEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1980x1080")
        self.root.title("Film Filter Aesthetic Application")

        self.photo = None
        self.preview_frame = customtkinter.CTkFrame(self.root)
        self.preview_frame.pack()

        self.create_widgets()

    def create_widgets(self):
        title_font = customtkinter.CTkFont(family="Helvetica", size=20, weight="bold")
        title = customtkinter.CTkLabel(self.root, text="Film Filter Aesthetic Application", font=title_font)
        title.pack(padx=10, pady=10)

        instructions = customtkinter.CTkLabel(self.root, text="Upload an image, apply your filters, just a few clicks!", font=("Helvetica", 14))
        instructions.pack(padx=10, pady=5)

        self.upload_button = customtkinter.CTkButton(self.root, text="Open Image", command=self.image_upload, width=350, height=40)
        self.upload_button.pack(pady=10)

        self.save_btn = customtkinter.CTkButton(self.root, text="Save Image", command=self.save_image, width=350, height=40, state=tk.DISABLED)
        self.save_btn.pack(pady=10)

    def image_upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")], title="Open Image")
        if file_path:
            self.photo = Photo(file_path)
            self.photo.show_image(self.preview_frame, on_preview_ready=lambda: self.save_btn.configure(state=tk.NORMAL))

    def save_image(self):
        if self.photo:
            self.photo.save_image()


# --- Launch App ---
if __name__ == "__main__":
    root = customtkinter.CTk()
    app = FilmEditorApp(root)
    root.mainloop()
