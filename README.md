# Image Contour Processing
This script processes an image, extracting and visualizing contours using the Pillow (PIL) library. Contours represent the boundaries of distinct objects or features within an image.

## Table of Contents
- [Objective](#objective)
- [Functionality](#functionality)
- [Parameters for Customization](#parameters-for-customization)
- [Edge Enhancement](#edge-enhancement)
- [Visualization](#visualization)
- [Code Structure](#code-structure)
- [Instructions](#instructions)
- [Customization](#customization)

## Objective
The objective of this script is to enhance and visualize contours in images, providing insights into object boundaries.

## Functionality
- Reads an image from the provided path.
- Converts the image to grayscale, a common preprocessing step.
- Detects contours using thresholding techniques.
- Visualizes contours and edges, providing an insightful representation of image structures.

## Parameters for Customization
- **Contour Line Thickness:** Users can customize the thickness of contour lines.
- **White Background:** Option to display images with a white background.
- **Contour Fill Color:** Customizable color for filling contour areas.

## Edge Enhancement
- Applies Gaussian blur to reduce noise and improve contour detection.
- Utilizes edge enhancement filters to emphasize image edges.

## Visualization
- Displays original images alongside versions with enhanced contours.

## Code Structure
The script is organized into several functions for modular and clear code structure:
1. `read_image(img_path)`: Reads an image from the provided path.
2. `convert_to_grayscale(image)`: Converts the given image to grayscale.
3. `find_contours_mask(gray_image)`: Finds contours in the grayscale image using thresholding.
4. `draw_contours_edge(original_image, gray_image, line_thickness, contour_thickness, threshold)`: Enhances and visualizes contours in the given image, returning a new image highlighting contours and edges.
5. `fill_contours(image, contours, thickness, fill_color)`: Fills contours with a specified color in the given image.
6. `draw_contours(image, contours, fill_color, thickness)`: Draws contour lines on the given image based on binary contour data.
7. `display_images(images, titles)`: Displays a list of images with corresponding titles.
8. `main(img_path, contour_line_thickness, white_bg=False, contour_fill_color=(253, 253, 253))`: Main function orchestrating the processing steps and allowing customization.

## Instructions
1. **Installation:**
   - Install required libraries: `Pillow` and `matplotlib`.
   - Ensure Python is installed on the system.

2. **Usage:**
   - Modify `img_path` to the desired image file path.
   - Customize optional parameters in the `main` function.
   - Run the script to visualize image contours.

3. **Customization:**
   - Adjust `contour_line_thickness` for varying line thickness.
   - Set `white_bg` to `True` for a white background.
   - Modify `contour_fill_color` to change the filled contour color.
