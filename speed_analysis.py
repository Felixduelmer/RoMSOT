import os
from PIL import Image
import numpy as np
from utils import loadTracking, create_zoomed_image
from metrics import compute_and_store_metrics


def main():
    """
    Run the speed analysis to reproduce the corresponding figures and metrics.

    Expects the speed data to be located under `data/speed/Scan_1` ... `Scan_7`.
    """
    # Define the main directory where the "Scan_X" folders are located
    main_dir = "data/speed"

    # Initialize an empty list to store the images
    images = []
    position = []

    # Loop through the folders
    for i in range(1, 9):
        folder_name = f"Scan_{i}"
        # load tracking file
        tracking_file = os.path.join(main_dir, folder_name, "800_tracking.ts")
        tracking = loadTracking(tracking_file)

        if len(position) == 0:
            # select the x, y, z position in the middle of the tracking
            position = tracking["tracking"][len(tracking["tracking"]) // 2][:3, 3]
            # store the index of the position
            index = len(tracking["tracking"]) // 2
        else:
            # iterate through the tracking and select the x, y, z position closest to the previous position
            temp_position = tracking["tracking"][0][:3, 3]
            for idx, track in enumerate(tracking["tracking"]):
                if np.linalg.norm(track[:3, 3] - position) < np.linalg.norm(
                    temp_position - position
                ):
                    temp_position = track[:3, 3]
                    # store the index of the position
                    index = idx

        image_path = os.path.join(main_dir, folder_name, "800")
        # Get the first image in the "800" folder
        image_files = sorted(os.listdir(image_path))
        closest_image_idx = image_files[index]
        closest_image = Image.open(
            os.path.join(image_path, closest_image_idx)
        ).convert("RGB")

        # Append the image to the list
        images.append(closest_image)

    # convert PIL images to numpy arrays
    images = [np.array(image) for image in images]
    # normalize between 0 and 1
    images = np.float32([(image[:, :, 0] / 255) for image in images])

    compute_and_store_metrics(images, main_dir, "speed")


if __name__ == "__main__":
    main()
