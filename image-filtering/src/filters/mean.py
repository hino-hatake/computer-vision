def apply_mean_filter(image, kernel_size):
    import cv2
    import numpy as np

    # Create the mean filter kernel
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)

    # Apply the mean filter to the image
    filtered_image = cv2.filter2D(image, -1, kernel)

    return filtered_image