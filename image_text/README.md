# ImageTextAdder

The image_editor.py file `ImageTextAdder` class allows you to add multiline text to an image. It calculates the bounding box around the text and draws it on the image.

## Usage

1. Instantiate the `ImageTextAdder` class with the required parameters.
2. Call the `add_text_to_image()` method to add text to the image.
3. Call the `save_image()` method to save the modified image.

## Parameters

- `image_path` (str): Path to the input image file.
- `text` (str): Text to be added to the image.
- `font_size` (int): Font size of the text.
- `font_family` (str): Online Link or Local Path to the font file.
- `background_color` (string / tuple): Background color of the image in String ('white') or RGB format.

## Example Usage

```python
from ImageTextAdder import ImageTextAdder

text_adder = ImageTextAdder(image_path="images/1.jpg",
                            text="SAMPLE TEXT \n sample text",
                            font_size=45,
                            font_family="https://www.freefontspro.com/14454/arial.ttf",
                            background_color=(255, 45, 62))
text_adder.add_text_to_image()
img = text_adder.save_image(output_path="result.jpg")
img.show()
