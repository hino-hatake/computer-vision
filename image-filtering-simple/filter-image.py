import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import random_noise
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim
import pandas as pd
import os
from sklearn.metrics import f1_score  # Import thêm F1-score từ sklearn

# Tạo thư mục output nếu chưa có
os.makedirs("output", exist_ok=True)

# 1. Đọc ảnh gốc và thêm nhiễu
original = cv2.imread("input/sample.png", cv2.IMREAD_COLOR)
original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

# Thêm nhiễu Salt & Pepper
noisy = random_noise(original_rgb, mode='s&p', amount=0.25)
noisy = np.array(255 * noisy, dtype=np.uint8)
cv2.imwrite("output/noisy.png", cv2.cvtColor(noisy, cv2.COLOR_RGB2BGR))

# Hiển thị ảnh gốc và ảnh nhiễu cạnh nhau
plt.figure(figsize=(12, 4))
plt.subplot(121)
plt.imshow(original_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(122)
plt.imshow(noisy)
plt.title("Noisy Image (Salt & Pepper)")
plt.axis("off")
plt.show()

# 3. Áp dụng các bộ lọc
mean_filtered = cv2.blur(noisy, (5, 5))
gaussian_filtered = cv2.GaussianBlur(noisy, (5, 5), sigmaX=1)
median_filtered = cv2.medianBlur(noisy, 5)

# Hàm tính Edge Map F1
def edge_map_f1_score(original, filtered):
    # Chuyển ảnh sang grayscale
    original_gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
    filtered_gray = cv2.cvtColor(filtered, cv2.COLOR_RGB2GRAY)
    
    # Áp dụng Canny Edge Detection
    edges_original = cv2.Canny(original_gray, 100, 200)
    edges_filtered = cv2.Canny(filtered_gray, 100, 200)
    
    # Chuẩn hóa giá trị bản đồ biên về 0 và 1
    edges_original_binary = (edges_original > 0).astype(np.uint8)
    edges_filtered_binary = (edges_filtered > 0).astype(np.uint8)
    
    # Flatten edges để tính F1-score
    edges_original_flat = edges_original_binary.flatten()
    edges_filtered_flat = edges_filtered_binary.flatten()
    
    # Tính F1-score
    return f1_score(edges_original_flat, edges_filtered_flat, average='binary')

# 4. Tính PSNR, SSIM và Edge Map F1
def evaluate_metrics(original, filtered):
    return {
        "PSNR": psnr(original, filtered, data_range=255),
        "SSIM": ssim(
            original, 
            filtered, 
            channel_axis=2,  # Specify RGB channel axis
            data_range=255,
            win_size=3  # Use smaller window size
        ),
        "Edge Map F1": edge_map_f1_score(original, filtered)
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
    # Đảm bảo ảnh ở định dạng uint8
    img_uint8 = np.array(img, dtype=np.uint8)
    cv2.imwrite(output_path, cv2.cvtColor(img_uint8, cv2.COLOR_RGB2BGR))

# 4. Áp dụng Laplacian sharpening cho các ảnh đã lọc
def apply_laplacian_sharpening(image, kernel_size=3, alpha=0.7):
    # Tạo kernel Laplacian
    laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=kernel_size)
    # Chuyển về uint8 và lấy giá trị tuyệt đối
    laplacian = np.uint8(np.absolute(laplacian))
    # Cộng với ảnh gốc để tăng cường biên với trọng số alpha
    sharpened = cv2.addWeighted(image, 1.0, laplacian, -alpha, 0)
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
    sharpened = apply_laplacian_sharpening(filtered_img, kernel_size=3, alpha=0.7)
    sharpened_images[f"{name}_sharpened"] = sharpened
    
    # Tính metrics cho ảnh đã sharpening
    sharpened_results[f"{name} + Sharpening"] = evaluate_metrics(original_rgb, sharpened)
    
# Lưu ảnh đã sharpening
for name, sharpened_img in sharpened_images.items():
    output_path = f"output/{name.lower()}.png"
    # Đảm bảo ảnh ở định dạng uint8
    sharpened_img_uint8 = np.array(sharpened_img, dtype=np.uint8)
    cv2.imwrite(output_path, cv2.cvtColor(sharpened_img_uint8, cv2.COLOR_RGB2BGR))

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
