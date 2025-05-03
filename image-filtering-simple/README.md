# Image Filtering (Simple)

## Install

```sh
# tạo môi trường ảo
python -m venv venv
source venv/bin/activate

# cài thư viện
pip install -r requirements.txt

# run
python filter-image.py
```

## Flow

```mermaid
graph LR
A[Ảnh nhiễu] --> B[Lọc nhiễu]
B --> C[Đánh giá lần 1]
B --> D[Tăng cường biên]
D --> E[Đánh giá lần 2]
```

## Guideline

### PSNR (Peak Signal-to-Noise Ratio)

- Đơn vị: dB (decibel)
- Ý nghĩa: So sánh mức độ nhiễu so với tín hiệu gốc. Giá trị càng cao → ảnh càng giống ảnh gốc (ít noise hơn).
- MSE: mean squared error

📈 Cách đọc:

| PSNR (dB) | Chất lượng tái tạo          |
| --------- | --------------------------- |
| < 20      | Rất tệ (nhiễu cao)          |
| 20 – 30   | Trung bình                  |
| 30 – 40   | Tốt                         |
| > 40      | Rất tốt (gần như giống gốc) |

### SSIM (Structural Similarity Index)

- Đơn vị: không đơn vị (giá trị từ 0 đến 1)
- Ý nghĩa: So sánh sự tương đồng cấu trúc giữa 2 ảnh (tốt hơn MSE vì xét cả độ sáng, tương phản và cấu trúc)

📈 Cách đọc:

| SSIM      | Mức độ giống ảnh gốc        |
| --------- | --------------------------- |
| < 0.5     | Tệ                          |
| 0.5 – 0.7 | Chấp nhận được              |
| 0.7 – 0.9 | Tốt                         |
| > 0.9     | Rất tốt (gần như giống gốc) |
