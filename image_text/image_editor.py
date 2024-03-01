"""
    This ImageTextAdder class allows adding multiline text to an image center and calculates the bounding box and draw around the text.

    Usage:
    Instantiate the `ImageTextAdder` class with the required parameters.
    Call the `add_text_to_image()` method to add text to the image.
    Call the `save_image()` method to save the modified image.

"""

from PIL import Image, ImageDraw, ImageFont

class ImageTextAdder:
    def __init__(self, image_path, text, font_size, font_family, background_color):
        """
        Initialize ImageTextAdder object.

        Parameters:
        - image_path (str): Path to the input image file.
        - text (str): Text to be added to the image.
        - font_size (int): Font size of the text.
        - font_family (str): Online Link or Local Path to the font file.
        - background_color (string / tuple): Background color of the image in String ('white') or RGB format.
        """
        self.image_path = image_path
        self.text = text
        self.font_size = font_size
        self.font_family = font_family
        self.background_color = background_color
        self.image = None
    
    def add_text_to_image(self):
        """
        Add text to the image.

        Returns:
        - bool: True if the operation is successful, False otherwise.
        """
        # Open the image
        self.image = Image.open(self.image_path)
        
        # Get image dimensions and calculate center coordinates
        image_width, image_height = self.image.size
        ctd_w, ctd_h = image_width // 2, image_height // 2
        
        # Create a font object
        font = ImageFont.truetype(self.font_family, self.font_size)
        
        # Calculate text height
        text_lines = self.text.split('\n')
        total_text_height = sum(font.getbbox(line)[-1] for line in text_lines)
        
        # Calculate text size and position
        y_offset = (ctd_h - total_text_height // 2)
        draw = ImageDraw.Draw(self.image)
        y = y_offset
        x_min, y_min, x_max, y_max = 0, 0, 0, 0
        text_coords_list = []
        
        # Split text into multiple lines and calculate the global bounding box area
        for idx, text in enumerate(self.text.split('\n')):
            _, _, text_width, text_height = font.getbbox(text)
            x1, y1 = int(ctd_w - text_width // 2), int(ctd_h - text_height // 2)
            x2, y2 = int(ctd_w + text_width // 2), int(ctd_h + text_height // 2)
            
            # Update bounding box coordinates to get the global bounding box that contains complete text
            if x_min == 0 or x_min > x1:
                x_min = x1
            if y_min == 0 or y_min > y:
                y_min = y
            if x_max == 0 or x_max < x2:
                x_max = x2
            if y_max == 0 or y_max < y2:
                y_max = y
            
            text_coords_list.append([x1, y, text])
            y += text_height
            
            # # Draw debug markers
            # draw.text((ctd_w, ctd_h), '*', fill=(255, 0, 0), font=ImageFont.truetype(self.font_family, 50)) # image center point
            # draw.text((x1, y), 'x', fill=(255, 0, 0), font=ImageFont.truetype(self.font_family, 8)) # starting point of each box
            
            # Update y_max for the last line
            if idx + 1 == len(self.text.split('\n')):
                y_max = y
        
        # Draw global bounding box with WHITE background
        text_box = [x_min, y_min, x_max, y_max]
        draw.rectangle(text_box, fill=self.background_color) # white background
        
        # Draw text on image
        for x, y, text in text_coords_list:
            draw.text((x, y), text, font=font, fill=(0, 0, 0))
        
        return True
    
    def save_image(self, output_path):
        """
        Save the modified image.

        Parameters:
        - output_path (str): Path to save the modified image.

        Returns:
        - Image: The modified image object.
        """
        if self.image is not None:
            self.image.save(output_path)
            return self.image
        else:
            print("No image has been modified yet. Call add_text_to_image() first.")
            return None
    

if __name__ == "__main__":
    text_adder = ImageTextAdder(image_path="images/lenna-grey.png",
                                text="Sample text \n sample text",
                                font_size=50,
                                font_family="https://www.freefontspro.com/14454/arial.ttf",
                                background_color=(255, 255, 255))
    text_adder.add_text_to_image()
    img = text_adder.save_image(output_path="result.jpg")
    img.show()