import numpy as np
import datetime
from PIL import Image, ImageDraw


def create_zoomed_image(image, zoom_factor=4, draw_rectangle_on_zoomed=False):
    """
    Create a zoomed version of an image by cropping and magnifying the center region.
    
    Args:
        image: PIL Image to zoom
        zoom_factor: Factor to determine the crop size (default: 4)
        draw_rectangle_on_zoomed: Whether to draw a red rectangle on the zoomed image (default: False)
    
    Returns:
        tuple: (zoomed_image, (left, top, zoom_width, zoom_height))
    """
    width, height = image.size
    zoom_width = width // zoom_factor
    zoom_height = height // zoom_factor

    # Calculate the coordinates of the center square
    left = (width - zoom_width) // 2 + 30
    top = (height - zoom_height) // 2 + 10
    right = left + zoom_width
    bottom = top + zoom_height

    # Crop the center square
    cropped = image.crop((left, top, right, bottom))

    # Resize the cropped area to original image size (magnify)
    zoomed = cropped.resize(
        (zoom_width * int(zoom_factor / 2), zoom_height * int(zoom_factor / 2)),
        Image.LANCZOS,
    )

    # Draw red rectangles on the original image
    draw = ImageDraw.Draw(image)
    draw.rectangle([left, top, right, bottom], outline="red", width=2)

    # Optionally draw rectangle on zoomed image
    if draw_rectangle_on_zoomed:
        draw_zoomed = ImageDraw.Draw(zoomed)
        draw_zoomed.rectangle(
            [0, 0, zoom_width * int(zoom_factor / 2) - 1, zoom_height * int(zoom_factor / 2) - 1],
            outline="red",
            width=2,
        )

    return zoomed, (left, top, zoom_width, zoom_height)


def loadTracking(file_path):
    # Initialize a list to hold the transformation matrices
    poses = []
    timestamps = []

    # Open the file in read mode ('r')
    with open(file_path, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Split the line into components
            components = line.strip().split('\t')
            # Exclude the last two components (index and the constant 0)
            matrix_values = components[:-2]
            # Convert the string values to float
            matrix_values = list(map(float, matrix_values))
            # Reshape the flat list back into a matrix
            # Assuming the original matrix size was 4x4
            pose = np.array(matrix_values).reshape((4, 4), order='F')

            # Append the reconstructed matrix to the list
            poses.append(pose)
            # append timestamp from unix time
            timestamps.append(datetime.datetime.fromtimestamp(float(components[-2])))


    # poses = correct_poses(poses)
    tracking =  {"tracking": poses, "time": timestamps}

    return tracking