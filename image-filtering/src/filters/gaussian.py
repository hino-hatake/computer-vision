def apply_gaussian_filter(image, sigma):
    import cv2
    import numpy as np

    # Apply Gaussian filter
    filtered_image = cv2.GaussianBlur(image, (0, 0), sigma)
    return filtered_image