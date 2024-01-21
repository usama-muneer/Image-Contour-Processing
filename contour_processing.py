# contour_processor.py

from PIL import Image, ImageDraw, ImageFilter
import matplotlib.pyplot as plt
import argparse
import pathlib

def read_image(img_path):
    """Reads an image from the given path."""
    return Image.open(img_path)

def convert_to_grayscale(image):
    """Converts the given image to grayscale."""
    return image.convert('L')

def find_contours_mask(gray_image):
    """
    Finds contours in the given grayscale image using thresholding.
    Returns a binary image representing the contours.
    """
    return gray_image.point(lambda x: 0 if x < 128 else 255).convert("1").getdata()

def draw_contours_edge(original_image, gray_image, line_thickness=1, contour_thickness=0, threshold=128):
    """
    Enhances and visualizes contours in the given image.
    Returns a new image highlighting contours and edges.

    Parameters:
    - original_image: The original image
    - gray_image: Grayscale version of the original image
    - line_thickness: Thickness of contour lines
    - contour_thickness: Thickness of filled contour areas
    - threshold: Edge detection threshold
    """
    # Apply Gaussian blur to reduce noise and improve contour detection
    blurred_image = gray_image.filter(ImageFilter.GaussianBlur(radius=2))

    # Use the edge enhancement filter to emphasize edges
    edges_image = blurred_image.filter(ImageFilter.EDGE_ENHANCE)

    # Convert the image to binary using a threshold
    binary_image = edges_image.point(lambda x: 0 if x < threshold else 255, 'L')

    # Find contours in the binary image
    contours = binary_image.filter(ImageFilter.FIND_EDGES)

    # Exclude the corner coordinates from contours
    width, height = contours.size
    exclude_corners = [(0, 0), (0, height - 1), (width - 1, 0), (width - 1, height - 1)]

    # Create an image without contours
    no_contour_image = original_image.copy().convert('RGB')
    no_contour_image.paste((255, 0, 0), (0, 0, no_contour_image.width, no_contour_image.height), mask=contours)
    draw = ImageDraw.Draw(no_contour_image)

    # Iterate through pixels to draw contours with the specified thickness
    for y in range(0, contours.size[1], contour_thickness):
        for x in range(0, contours.size[0], contour_thickness):
            pixel_value = contours.getpixel((x, y))
            if pixel_value == 255:
                # Draw lines with increased thickness both horizontally and vertically
                draw.line([(x, y), (x + contour_thickness, y)], fill=(255, 0, 0), width=line_thickness)
                draw.line([(x, y), (x, y + contour_thickness)], fill=(255, 0, 0), width=line_thickness)

    return no_contour_image

def fill_contours(image, contours, thickness, fill_color):
    """
    Fills contours with a specified color in the given image.
    Returns the image with filled contours.

    Parameters:
    - image: Original image
    - contours: Binary contour data
    - thickness: Thickness of filled contour areas
    - fill_color: RGB color for filling contours
    """
    filled_contour_image = image.copy()
    draw = ImageDraw.Draw(filled_contour_image)

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if contours[y * image.size[0] + x] == 0:
                # Draw contour point
                draw.point((x, y), fill=fill_color)

    return filled_contour_image

def draw_contours(image, contours, fill_color, thickness=1):
    """
    Draws contour lines on the given image based on the binary contour data.
    Returns the image with drawn contours.

    Parameters:
    - image: Original image
    - contours: Binary contour data
    - thickness: User-defined thickness for the contour lines (default is 1)
    """
    contour_image = image.copy()
    draw = ImageDraw.Draw(contour_image)

    for y in range(image.size[1] - 1):
        for x in range(image.size[0] - 1):
            if contours[y * image.size[0] + x] == 0:
                # Draw lines connecting adjacent contour points
                draw.line([(x, y), (x + 1, y)], fill=fill_color, width=thickness)
                draw.line([(x, y), (x, y + 1)], fill=fill_color, width=thickness)

    return contour_image

def display_images(images, titles):
    """Displays a list of images with corresponding titles."""
    fig, axs = plt.subplots(1, len(images), figsize=(5 * len(images), 5))
    pathlib.Path('output').mkdir(parents=True, exist_ok=True)
    for i, (img, title) in enumerate(zip(images, titles)):
        axs[i].axis('off')
        axs[i].imshow(img)
        axs[i].set_title(title)
        img.save(f'output/{title.replace(" ", "_")}.png')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Process and visualize contours in images.')
    parser.add_argument('--img_path', type=str, help='Path to the image file')
    parser.add_argument('--contour_line_thickness', type=int, default=1, help='Thickness of contour lines')
    parser.add_argument('--white_bg', action='store_true', help='Display images with a white background')
    parser.add_argument('--contour_fill_color', type=str, default='white', help='RGB color for filling contours')
    
    args = parser.parse_args()

    # Step 1: Read the image
    original_image = read_image(args.img_path)

    # Step 2: Convert the image to grayscale
    gray_image = convert_to_grayscale(original_image)

    # Step 3: Find contours in the grayscale image
    contours = find_contours_mask(gray_image)

    # Step 4: Draw contours on the original image
    contours_without_edge = draw_contours(original_image, contours, fill_color=args.contour_fill_color)
    new_image = Image.new('RGB', contours_without_edge.size, (255, 255, 255)) if args.white_bg else contours_without_edge.copy()
    contours_with_edge = draw_contours_edge(new_image, gray_image, line_thickness=1, contour_thickness=1, threshold=128)

    # Step 5: Draw an outlined contour on the original image
    filled_contour_with_edge = draw_contours_edge(new_image, gray_image, line_thickness=args.contour_line_thickness, contour_thickness=1, threshold=128)

    # Step 6: Display the images
    display_images([original_image, contours_without_edge, contours_with_edge, filled_contour_with_edge],
                   ['Original Image', 'Contours Without Edge', 'Contours With Edge', 'Contours With Custom Edge Thickness'])

if __name__ == "__main__":
    main()
