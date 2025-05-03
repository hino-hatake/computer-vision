def load_image(file_path):
    import cv2
    image = cv2.imread(file_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {file_path}")
    return image

def save_image(image, file_path):
    import cv2
    success = cv2.imwrite(file_path, image)
    if not success:
        raise IOError(f"Failed to save image at {file_path}")