def apply_median_filter(image, kernel_size):
    import cv2
    import numpy as np

    # Apply median filter to the image
    filtered_image = cv2.medianBlur(image, kernel_size)
    return filtered_image