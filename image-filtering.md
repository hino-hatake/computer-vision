# Image Filtering

## ✅ Task 1: Source Code – Triển khai và so sánh các bộ lọc truyền thống

🎯 Mục tiêu:
- Làm sạch ảnh bị nhiễu (denoising)
- Cải thiện chi tiết/biên (enhancement)
- So sánh tác động của từng bộ lọc

🛠️ Bộ lọc cần triển khai:

| Bộ lọc            | Mục đích                          | OpenCV API          | Ghi chú                     |
|--------------------|-----------------------------------|---------------------|-----------------------------|
| Mean filter        | Làm mượt toàn cục, đơn giản       | `cv2.blur`          | Nhòe biên mạnh             |
| Gaussian filter    | Làm mượt có trọng số, giảm nhiễu Gaussian | `cv2.GaussianBlur`  | Bảo toàn biên tốt hơn Mean |
| Median filter      | Xử lý tốt Salt & Pepper noise     | `cv2.medianBlur`    | Không làm nhòe biên         |
| Laplacian sharpening | Làm rõ biên, tăng chi tiết       | `cv2.Laplacian`     | Không khử nhiễu, dễ tăng noise |

🖼️ Output cần có:
Ảnh gốc, ảnh nhiễu, ảnh sau mỗi filter

Trình bày side-by-side (horizontally or grid)

## ✅ Task 2: Comparative Analysis – So sánh các phương pháp
🎯 Mục tiêu:
- Đánh giá hiệu quả bộ lọc dựa trên tiêu chí định lượng và định tính.

📊 Đánh giá định lượng:

| Metric | Ý nghĩa | Công cụ |
|--------|---------|---------|
| PSNR (Peak Signal-to-Noise Ratio) | Đo chất lượng tái tạo so với ảnh gốc | `cv2.PSNR`, hoặc `10 * log10(MAX^2 / MSE)` |
| SSIM (Structural Similarity Index) | So sánh cấu trúc ảnh | `skimage.metrics.structural_similarity` |

> Note: Nếu dùng ảnh thật không có ground truth: chỉ so sánh định tính và độ sắc nét (variance of Laplacian).

👀 Đánh giá định tính:
- Mức độ làm mượt tổng thể
- Khả năng bảo toàn biên
- Ảnh có bị nhòe hay còn chi tiết

⚖️ Phân tích:
- Ưu nhược điểm từng bộ lọc
- Thử thay đổi kernel size (ví dụ: 3×3, 5×5, 7×7) để xem ảnh hưởng
- So sánh giữa Gaussian vs. Median trong khử nhiễu biên
- So sánh hiệu ứng sharpening sau lọc

## ✅ Task 3: Final Report Guidelines – Báo cáo kỹ thuật

```md
# Image Filtering – Midterm Project Part A

## 1. Introduction and Motivation
- Tầm quan trọng của filtering trong CV
- Loại nhiễu xử lý (Gaussian, Salt & Pepper...)

## 2. Methods
- Mô tả các filter, công thức toán học:
  - Mean: convolution với kernel đều
  - Gaussian: kernel 2D Gaussian
  - Median: non-linear filter
  - Laplacian: edge enhancement

## 3. Implementation
- Mã nguồn chính (rút gọn)
- Ảnh kết quả: gốc, nhiễu, từng filter

## 4. Comparative Analysis
- PSNR, SSIM
- Bảng so sánh (xem ví dụ dưới)
- Phân tích kết quả

## 5. Conclusion and Extensions
- Filter nào phù hợp loại nhiễu nào
- Có thể áp dụng cho ảnh y tế, CV thực tế
```

📊 Ví dụ bảng so sánh trong báo cáo:

| Filter        | PSNR (dB) | SSIM  | Edge Preservation | Ghi chú |
|---------------|-----------|-------|-------------------|--------|
| Mean (5x5)    | 22.3      | 0.73  | Yếu               | Làm mượt toàn ảnh |
| Gaussian (5x5)| 24.1      | 0.80  | Tốt               | Cân bằng giữa noise và detail |
| Median (5)    | 25.7      | 0.85  | Rất tốt           | Đặc biệt tốt với S&P noise |
| Laplacian     | NA        | NA    | Tăng cường biên   | Nên dùng sau khi lọc noise |

## 📌 Kết luận tổng quát cho Part A

| Tiêu chí               | Mức độ yêu cầu                              |
|------------------------|---------------------------------------------|
| Kỹ thuật lập trình     | Cơ bản đến trung bình                       |
| Hiểu biết toán học     | Trung bình (convolution, PSNR)              |
| Khả năng trình bày     | Quan trọng – ảnh, bảng, so sánh             |
| Mức độ phù hợp giáo trình | Vừa đủ mở rộng, kiểm tra kiến thức nền xử lý ảnh |
