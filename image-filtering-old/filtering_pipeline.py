import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

def add_noise(img, noise_type='gaussian'):
    if noise_type == 'gaussian':
        row, col = img.shape
        mean = 0
        sigma = 25
        gauss = np.random.normal(mean, sigma, (row, col)).astype(np.float32)
        noisy = img.astype(np.float32) + gauss
        return np.clip(noisy, 0, 255).astype(np.uint8)
    elif noise_type == 'salt_pepper':
        s_vs_p = 0.5
        amount = 0.02
        noisy = img.copy()
        num_salt = np.ceil(amount * img.size * s_vs_p).astype(int)
        num_pepper = np.ceil(amount * img.size * (1. - s_vs_p)).astype(int)
        coords = [np.random.randint(0, i, num_salt) for i in img.shape]
        noisy[coords] = 255
        coords = [np.random.randint(0, i, num_pepper) for i in img.shape]
        noisy[coords] = 0
        return noisy
    else:
        return img

def psnr(img1, img2):
    mse = np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)
    if mse == 0: return float('inf')
    PIXEL_MAX = 255.0
    return 10 * np.log10((PIXEL_MAX ** 2) / mse)

img = cv2.imread('lena.jpg', cv2.IMREAD_GRAYSCALE)
noisy = add_noise(img, noise_type='gaussian')

# Apply filters
mean_filt = cv2.blur(noisy, (5, 5))
gauss_filt = cv2.GaussianBlur(noisy, (5, 5), 1)
median_filt = cv2.medianBlur(noisy, 5)
laplacian = cv2.Laplacian(img, cv2.CV_64F)
sharpened = cv2.convertScaleAbs(img - 0.7 * laplacian)

# Evaluation
for name, filtered in zip(
    ["Mean", "Gaussian", "Median"],
    [mean_filt, gauss_filt, median_filt]
):
    print(f"{name} PSNR: {psnr(img, filtered):.2f} dB")
    print(f"{name} SSIM: {ssim(img, filtered):.3f}")

# Display images
images = [img, noisy, mean_filt, gauss_filt, median_filt, sharpened]
titles = ["Original", "Noisy", "Mean", "Gaussian", "Median", "Sharpened"]

plt.figure(figsize=(12, 6))
for i in range(6):
    plt.subplot(2, 3, i+1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis("off")
plt.tight_layout()
plt.show()
