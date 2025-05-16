#Method used to alter the looks of images while preserving native resolution of users image


'''''
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
'''