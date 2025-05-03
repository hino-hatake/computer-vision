def apply_laplacian_filter(image):
    import cv2
    import numpy as np

    # Convert the image to grayscale if it is not already
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply the Laplacian filter
    laplacian = cv2.Laplacian(image, cv2.CV_64F)

    # Convert back to uint8
    laplacian = cv2.convertScaleAbs(laplacian)

    return laplacian