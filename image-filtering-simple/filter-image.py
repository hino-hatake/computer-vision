import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import random_noise
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim
import pandas as pd
import os

# Tạo thư mục output nếu chưa có
os.makedirs("output", exist_ok=True)

# 1. Đọc ảnh gốc
original = cv2.imread("input/sample.png", cv2.IMREAD_COLOR)
original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
plt.imshow(original_rgb)
plt.title("Original Image")
plt.axis("off")
plt.show()

# 2. Thêm nhiễu Salt & Pepper
noisy = random_noise(original_rgb, mode='s&p', amount=0.05)
noisy = np.array(255 * noisy, dtype=np.uint8)
cv2.imwrite("output/noisy.png", cv2.cvtColor(noisy, cv2.COLOR_RGB2BGR))
plt.imshow(noisy)
plt.title("Noisy Image (Salt & Pepper)")
plt.axis("off")
plt.show()

# 3. Áp dụng các bộ lọc
mean_filtered = cv2.blur(noisy, (3, 3))
gaussian_filtered = cv2.GaussianBlur(noisy, (3, 3), sigmaX=1)
median_filtered = cv2.medianBlur(noisy, 3)

# 4. Tính PSNR & SSIM
def evaluate_metrics(original, filtered):
    return {
        "PSNR": psnr(original, filtered, data_range=255),
        "SSIM": ssim(original, filtered, multichannel=True, data_range=255)
    }

results = {
    "Mean Filter": evaluate_metrics(original_rgb, mean_filtered),
    "Gaussian Filter": evaluate_metrics(original_rgb, gaussian_filtered),
    "Median Filter": evaluate_metrics(original_rgb, median_filtered),
}

# In bảng kết quả định lượng
df = pd.DataFrame(results).T
print("📊 Đánh giá định lượng:")
print(df)

# 5. Hiển thị bảng ảnh
def show_comparison():
    filters = {
        "Mean Filter": mean_filtered,
        "Gaussian Filter": gaussian_filtered,
        "Median Filter": median_filtered
    }

    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(12, 9))
    titles = ["Original", "Noisy", "Filtered"]

    for i, (name, filt_img) in enumerate(filters.items()):
        axs[i, 0].imshow(original_rgb)
        axs[i, 0].set_title(f"{name} - Original")
        axs[i, 1].imshow(noisy)
        axs[i, 1].set_title(f"{name} - Noisy")
        axs[i, 2].imshow(filt_img)
        axs[i, 2].set_title(f"{name} - Filtered")
        for j in range(3):
            axs[i, j].axis("off")

    plt.tight_layout()
    plt.show()

show_comparison()
