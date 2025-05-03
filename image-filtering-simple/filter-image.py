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
noisy = random_noise(original_rgb, mode='s&p', amount=0.25)
noisy = np.array(255 * noisy, dtype=np.uint8)
cv2.imwrite("output/noisy.png", cv2.cvtColor(noisy, cv2.COLOR_RGB2BGR))
plt.imshow(noisy)
plt.title("Noisy Image (Salt & Pepper)")
plt.axis("off")
plt.show()

# 3. Áp dụng các bộ lọc
mean_filtered = cv2.blur(noisy, (5, 5))
gaussian_filtered = cv2.GaussianBlur(noisy, (5, 5), sigmaX=1)
median_filtered = cv2.medianBlur(noisy, 5)

# 4. Tính PSNR & SSIM
def evaluate_metrics(original, filtered):
    return {
        "PSNR": psnr(original, filtered, data_range=255),
        "SSIM": ssim(
            original, 
            filtered, 
            channel_axis=2,  # Specify RGB channel axis
            data_range=255,
            win_size=3  # Use smaller window size
        )
    }

results = {
    "Mean Filter": evaluate_metrics(original_rgb, mean_filtered),
    "Gaussian Filter": evaluate_metrics(original_rgb, gaussian_filtered),
    "Median Filter": evaluate_metrics(original_rgb, median_filtered),
}

# In và lưu bảng kết quả định lượng
df = pd.DataFrame(results).T
print("📊 Đánh giá định lượng:")
print(df)

# Lưu kết quả đánh giá vào file txt
metrics_output = "📊 Đánh giá định lượng:\n" + df.to_string()
with open("output/metrics_results.txt", "w", encoding="utf-8") as f:
    f.write(metrics_output)

# Lưu các ảnh đã lọc
for name, img in {
    "mean_filtered": mean_filtered,
    "gaussian_filtered": gaussian_filtered,
    "median_filtered": median_filtered
}.items():
    output_path = f"output/{name}.png"
    cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

# 4. Áp dụng Laplacian sharpening cho các ảnh đã lọc
def apply_laplacian_sharpening(image):
    # Tạo kernel Laplacian
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    # Chuyển về uint8 và lấy giá trị tuyệt đối
    laplacian = np.uint8(np.absolute(laplacian))
    # Cộng với ảnh gốc để tăng cường biên
    sharpened = cv2.addWeighted(image, 1.5, laplacian, -0.5, 0)
    return sharpened

# Áp dụng sharpening và tính metrics
sharpened_results = {}
sharpened_images = {}

for name, filtered_img in {
    "Mean": mean_filtered,
    "Gaussian": gaussian_filtered,
    "Median": median_filtered
}.items():
    # Áp dụng sharpening
    sharpened = apply_laplacian_sharpening(filtered_img)
    sharpened_images[f"{name}_sharpened"] = sharpened
    
    # Tính metrics cho ảnh đã sharpening
    sharpened_results[f"{name} + Sharpening"] = evaluate_metrics(original_rgb, sharpened)
    
    # Lưu ảnh đã sharpening
    output_path = f"output/{name.lower()}_sharpened.png"
    cv2.imwrite(output_path, cv2.cvtColor(sharpened, cv2.COLOR_RGB2BGR))

# Cập nhật bảng kết quả với cả metrics của ảnh đã sharpening
all_results = {**results, **sharpened_results}
df_all = pd.DataFrame(all_results).T
print("\n📊 Đánh giá định lượng (sau khi sharpening):")
print(df_all)

# Cập nhật file metrics
metrics_output = "📊 Đánh giá định lượng (bao gồm sharpening):\n" + df_all.to_string()
with open("output/metrics_results.txt", "w", encoding="utf-8") as f:
    f.write(metrics_output)

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

# Cập nhật hàm hiển thị để thêm kết quả sharpening
def show_enhanced_comparison():
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(16, 9))
    
    for i, (filter_name, filter_img) in enumerate([
        ("Mean", mean_filtered),
        ("Gaussian", gaussian_filtered),
        ("Median", median_filtered)
    ]):
        # Ảnh gốc
        axs[i, 0].imshow(original_rgb)
        axs[i, 0].set_title(f"{filter_name} - Original")
        
        # Ảnh nhiễu
        axs[i, 1].imshow(noisy)
        axs[i, 1].set_title(f"{filter_name} - Noisy")
        
        # Ảnh đã lọc
        axs[i, 2].imshow(filter_img)
        axs[i, 2].set_title(f"{filter_name} Filter")
        
        # Ảnh đã lọc và sharpening
        axs[i, 3].imshow(sharpened_images[f"{filter_name}_sharpened"])
        axs[i, 3].set_title(f"{filter_name} + Sharpening")
        
        for j in range(4):
            axs[i, j].axis("off")
    
    plt.tight_layout()
    plt.show()

# Hiển thị kết quả cuối cùng
show_enhanced_comparison()
