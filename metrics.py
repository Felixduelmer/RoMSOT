import csv
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import os
import pandas as pd

# Function to compute PSNR
def compute_psnr(image1, image2):
    return psnr(image1, image2)

# Function to compute SSIM
def compute_ssim(image1, image2):
    return ssim(image1, image2, data_range=1)

# Function to compute SNR
def compute_snr(image):
    mean_signal = np.mean(image)
    std_noise = np.std(image)
    return mean_signal / std_noise

# Function to compute and store all metrics in a CSV file
def compute_and_store_metrics(images, main_dir, case):
    reference_image = images[0]  # Reference image is the first image
    if np.min(images) < 0 or np.max(images) > 1:
        raise ValueError('Images should be normalized between 0 and 1')
    psnr_values = []
    ssim_values = []
    csv_file_path = os.path.join(main_dir, case + "_metrics.csv")
    # Prepare the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Image Index', 'PSNR', 'SSIM'])


        # Loop through all images (except the first one) to compute metrics
        for i in range(1, len(images)):
            image = images[i]
            # Compute metrics
            psnr_value = compute_psnr(reference_image, image)
            psnr_values.append(psnr_value)
            ssim_value = compute_ssim(reference_image, image)
            ssim_values.append(ssim_value)
            # Write results to CSV
            writer.writerow([i, psnr_value, ssim_value])
        

    print(f'Metrics saved to {csv_file_path}')

    if case == "speed":
        x_axis_data = [0.4, 0.6, 0.8, 1.0, 2.0, 3.0, 4.0]
        data = {
            'Speed [m/s]': x_axis_data,
            'PSNR': psnr_values,
            'SSIM': ssim_values
        }
    else:
        x_axis_data = np.arange(5, 31, 5)
        data = {
            'Angle [°]': x_axis_data,
            'PSNR': psnr_values,
            'SSIM': ssim_values
        }

    # Create a pandas DataFrame
    df = pd.DataFrame(data)
    output_excel = os.path.join(main_dir, case + "_metrics.xlsx")
    df.to_excel(output_excel, index=False)
    print(f'Metrics saved to {output_excel}')

    # change font size to be way bigger
    plt.rcParams.update({'font.size': 30})

    # Create a figure and axis
    fig, ax1 = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)

    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

    # First plot for PSNR
    ax1.plot(x_axis_data, psnr_values, 'b-', label='PSNR')
    ax1.set_xlabel('Tilting Angle [°]' if case == "tilting" else 'Speed [m/s]')
    ax1.set_ylabel('PSNR', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Second y-axis for SSIM
    ax2 = ax1.twinx()
    make_patch_spines_invisible(ax2)
    ax2.spines['left'].set_position(('outward', 100 if case == "tilting" else 140))  # Initially position on the right
    ax2.spines['left'].set_visible(True)
    ax2.plot(x_axis_data, ssim_values, 'g-', label='SSIM')
    ax2.set_ylabel('SSIM', color='g')
    ax2.tick_params(axis='y', labelcolor='g')
    ax2.yaxis.set_label_position('left')
    ax2.yaxis.set_ticks_position('left')


    # Adding legends for all lines
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()

    # Combine all legends in one
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right' if case == "tilting" else 'upper right')
    fig_name = os.path.join(main_dir, case + "_metrics.png")
    # Show plot
    fig.show()
    fig.savefig(fig_name, bbox_extra_artists=(ax2,), bbox_inches='tight')
    print(f'Plot saved to {fig_name}')
    fig.clear()


if __name__ == "__main__":

    # Example usage:
    images = np.float32(np.random.rand(5, 256, 256))  # Example of 5 grayscale images (values between 0-255)

    compute_and_store_metrics(images, 'image_quality_metrics.csv')

