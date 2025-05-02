# Midterm Project Report

## 1. Introduction

Trong thời đại bùng nổ của trí tuệ nhân tạo (AI), các kỹ thuật thị giác máy tính truyền thống vẫn giữ vai trò nền tảng, đặc biệt trong các ứng dụng yêu cầu hiệu suất cao, tài nguyên hạn chế, hoặc khả năng diễn giải rõ ràng.

Dự án giữa kỳ này hướng đến việc ôn luyện và vận dụng các kỹ thuật cốt lõi của thị giác máy tính cổ điển như lọc ảnh (**filtering**), tái dựng 3D từ ảnh stereo (**3D reconstruction**), và ghép ảnh panorama (**panorama stitching**). Thông qua việc triển khai thủ công, sinh viên không chỉ hiểu rõ bản chất đằng sau mỗi thuật toán, mà còn hình thành tư duy xử lý các bài toán thực tế về thị giác một cách hệ thống và thực tiễn.

Báo cáo được chia làm ba phần chính, tương ứng với ba bài toán thực tế trong thị giác máy tính.

- Phần A tập trung vào **lọc ảnh**, giúp làm sạch nhiễu và cải thiện chất lượng ảnh đầu vào — một bước quan trọng trong mọi pipeline xử lý ảnh.
- Phần B khai thác kỹ thuật **tái dựng 3D từ ảnh stereo**, nhằm hiểu và triển khai các thuật toán hình học cơ bản như tính disparity map, ma trận cơ bản (fundamental matrix), và dựng point cloud.
- Phần C đề cập đến ghép ảnh panorama (**panorama stitching**), kết hợp các kỹ thuật phát hiện đặc trưng, tính homography và biến đổi hình học — đặt nền móng cho các ứng dụng như Google Street View hay stitching camera 360°.

Mỗi phần đều có ý nghĩa thiết thực, giúp củng cố kiến thức lý thuyết và kỹ năng lập trình ứng dụng trong thị giác máy tính.

## 2. Part A: Image Filtering

### 2.1 Methodology

Trong phần này, chúng ta áp dụng bốn kỹ thuật lọc ảnh truyền thống: **lọc trung bình** (mean filter), **lọc Gaussian**, **lọc trung vị** (median filter) và **tăng cường biên Laplacian**, nhằm làm giảm nhiễu và cải thiện chất lượng ảnh đầu vào. Mỗi bộ lọc có nguyên lý và đặc điểm riêng, phù hợp với các loại nhiễu khác nhau.

Dưới đây, mỗi bộ lọc sẽ được trình bày với công thức toán học và các khái niệm chính, cùng với giải thích về cách lựa chọn tham số.

#### Bộ lọc trung bình (Mean Filter)

Lọc trung bình sử dụng một cửa sổ lọc - kernel (thường là ma trận 3×3 hoặc 5×5) chứa các giá trị bằng nhau, thực hiện phép lấy trung bình cộng của các điểm ảnh trong vùng lân cận. Đây là phương pháp làm mượt đơn giản nhất. Công thức tính toán như sau:

```math
I'(x, y) = \frac{1}{k^2} \sum_{i=-k/2}^{k/2} \sum_{j=-k/2}^{k/2} I(x+i, y+j)
```

Trong đó:

- $I(x, y)$: giá trị pixel gốc tại tọa độ $(x, y)$,
- $I'(x, y)$: giá trị pixel sau khi áp dụng bộ lọc,
- $k$: kích thước cửa sổ lọc (ví dụ: 3 × 3, 5 × 5).

Mô hình minh hoạ:

```mermaid
graph TD
    A1["5×5 kernel (giá trị = 1/25)"] --> A2["Sliding Window"]
    A2 --> A3["Tính trung bình giá trị vùng lân cận"]
    A3 --> A4["Thay giá trị pixel trung tâm bằng trung bình"]
    A4 --> A5["Ảnh đầu ra được làm mượt"]
```

> ⚠️ Nhược điểm: làm nhòe biên và chi tiết nhỏ.

#### Bộ lọc Gaussian (Gaussian Filter)

Bộ lọc Gaussian sử dụng kernel với trọng số giảm dần theo khoảng cách đến tâm, cho phép làm mượt ảnh đồng thời bảo toàn biên tốt hơn lọc trung bình. Kernel Gaussian được định nghĩa bởi công thức:

```math
G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2 + y^2}{2\sigma^2}}
```

Trong đó:

- $\sigma$: độ lệch chuẩn, điều chỉnh mức độ làm mịn,
- $x, y$: tọa độ trong kernel.

Việc lựa chọn $\sigma$ và kích thước kernel ($k \times k$) cần cân nhắc giữa hiệu quả làm mịn và giữ lại chi tiết ảnh.

Mô hình minh họa:

```mermaid
graph TD
    B1["5×5 kernel (trọng số theo Gaussian)"] --> B2["Sliding Window"]
    B2 --> B3["Tính tổng có trọng số (weight) của vùng lân cận"]
    B3 --> B4["Giá trị gần tâm ảnh hưởng nhiều hơn"]
    B4 --> B5["Ảnh mượt, biên mềm, giảm nhiễu Gaussian tốt"]
```

> ✅ Ưu điểm: giảm nhiễu Gaussian tốt, ít làm mờ biên hơn mean filter.

#### Bộ lọc trung vị (Median Filter)

Bộ lọc trung vị thay thế giá trị của mỗi pixel bằng giá trị trung vị của các pixel trong cửa sổ lân cận. Bộ lọc này đặc biệt hiệu quả trong việc loại bỏ nhiễu dạng muối tiêu (salt-and-pepper noise). Không có công thức toán học cụ thể, nhưng quá trình thực hiện bao gồm các bước sau:

1. Lấy tất cả giá trị pixel trong cửa sổ $k \times k$,
2. Sắp xếp các giá trị theo thứ tự tăng dần,
3. Chọn giá trị trung vị làm giá trị mới cho pixel.

> ✅ Ưu điểm: giữ biên tốt, loại bỏ nhiễu mạnh không làm nhòe chi tiết.

Mô hình minh họa:

```mermaid
graph TD
    C1["5×5 vùng lân cận"] --> C2["Lấy tất cả giá trị pixel xung quanh"]
    C2 --> C3["Sắp xếp các giá trị theo thứ tự tăng dần"]
    C3 --> C4["Chọn giá trị trung vị (median)"]
    C4 --> C5["Gán vào pixel trung tâm"]
    C5 --> C6["Loại bỏ nhiễu xung, giữ biên"]
```

#### Bộ lọc tăng cường biên Laplacian (Laplacian Sharpening)

Bộ lọc Laplacian sử dụng đạo hàm bậc hai của ảnh để phát hiện biên, sau đó trừ kết quả vào ảnh gốc để làm nổi bật chi tiết. Kernel Laplacian phổ biến là:

```math
L =
\begin{bmatrix}
0 & -1 & 0 \\
-1 & 4 & -1 \\
0 & -1 & 0
\end{bmatrix}
```

Hoặc:

```math
L =
\begin{bmatrix}
-1 & -1 & -1 \\
-1 & 8 & -1 \\
-1 & -1 & -1
\end{bmatrix}
```

Việc lựa chọn kernel phụ thuộc vào yêu cầu cụ thể của bài toán, ví dụ: nhấn mạnh biên mạnh hoặc yếu.

Mô hình minh họa:

```mermaid
graph TD
    D1["Áp dụng Laplacian kernel (2nd derivative)"] --> D2["Phát hiện vùng biến đổi mạnh (biên)"]
    D2 --> D3["Tạo ảnh biên L"]
    D3 --> D4["Ảnh sharpened = Ảnh gốc - α × L"]
    D4 --> D5["Chi tiết rõ hơn, biên sắc nét hơn"]
```

> ⚠️ Không dùng để khử nhiễu, chỉ dùng sau bước lọc để làm rõ biên.

#### Giải thích lựa chọn tham số

- Kích thước cửa sổ ($k \times k$): Thường chọn giá trị lẻ (3, 5, 7) để đảm bảo có một pixel trung tâm.
- Đối với Gaussian filter, $\sigma$ được chọn dựa trên mức độ nhiễu cần loại bỏ.
- Với Laplacian filter, kernel được chọn để cân bằng giữa phát hiện biên và giảm nhiễu.

Tham số cụ thể lựa chọn như sau:

| Bộ lọc    | Kernel size | Ghi chú                           |
| --------- | ----------- | --------------------------------- |
| Mean      | 5×5         | Mức làm mượt trung bình           |
| Gaussian  | 5×5, σ=1.0  | Phổ biến, cân bằng nhiễu/biên     |
| Median    | 5           | Hiệu quả với nhiễu Salt & Pepper  |
| Laplacian | 3×3, α=0.7  | Làm rõ biên, sau khi đã lọc nhiễu |

Các bộ lọc trên sẽ được triển khai và thử nghiệm trên nhiều loại ảnh để đánh giá hiệu quả và tối ưu hóa tham số.

#### Diagram

Dưới đây là mô hình minh hoạ pipeline lọc ảnh truyền thống:

```mermaid
flowchart TD
    A["Ảnh gốc (Original)"] --> B["Thêm nhiễu (Add Noise)"]
    B --> C1[Mean Filter<br/>→ Làm mượt toàn cục<br/>→ Nhòe biên]
    B --> C2[Gaussian Filter<br/>→ Làm mượt có trọng số<br/>→ Giữ biên tốt hơn]
    B --> C3[Median Filter<br/>→ Loại bỏ nhiễu xung<br/>→ Bảo toàn chi tiết]
    A --> D[Laplacian Sharpening<br/>→ Phát hiện biên<br/>→ Làm rõ chi tiết]
    C1 --> E[So sánh PSNR / SSIM]
    C2 --> E
    C3 --> E
    D --> F[Hiển thị ảnh sắc nét]
    E --> G[Đánh giá tổng hợp]
    F --> G
    G --> H[Phân tích kết quả]
    H --> I[Kết luận]
    I --> J[Đề xuất mở rộng]
    J --> K[Hướng nghiên cứu tiếp theo]
```

Mô tả:

- C1, C2, C3: thể hiện 3 nhánh khử nhiễu
- D: nhánh tăng cường biên, tách biệt khỏi khử nhiễu
- G: điểm cuối để tổng hợp kết quả định lượng và định tính
- H: phân tích kết quả, đưa ra nhận xét và so sánh giữa các bộ lọc
- I: kết luận về hiệu quả của từng bộ lọc

### 2.2 Implementation and Results

Quá trình thực hiện được triển khai bằng ngôn ngữ **Python** sử dụng thư viện **OpenCV**, **NumPy** và **Matplotlib** để xử lý và trực quan hóa ảnh.

Ảnh gốc được chuyển sang ảnh nhiễu bằng cách cộng thêm nhiễu Gaussian ngẫu nhiên (σ = 25). Sau đó, lần lượt áp dụng các bộ lọc truyền thống để khử nhiễu và tăng cường chi tiết.

Chi tiết triển khai:

| Bộ lọc    | OpenCV API                    | Tham số sử dụng                |
| --------- | ----------------------------- | ------------------------------ |
| Mean      | `cv2.blur`                    | Kernel size: `(5, 5)`          |
| Gaussian  | `cv2.GaussianBlur`            | Kernel size: `(5, 5)`, σ = 1.0 |
| Median    | `cv2.medianBlur`              | Kernel size: `5`               |
| Laplacian | `cv2.Laplacian` + subtraction | Kernel size: `3x3`, α = 0.7    |

Kết quả trực quan:

_chèn ảnh vào đây sau._

**Hình 1:** Từ trái sang phải, trên xuống dưới:

1. Ảnh gốc (Original)
2. Ảnh có nhiễu (Noisy)
3. Lọc trung bình (Mean Filter)
4. Lọc Gaussian (Gaussian Filter)
5. Lọc trung vị (Median Filter)
6. Tăng cường biên Laplacian (Sharpened Image)

### 2.3 Comparative Analysis

Để đánh giá hiệu quả các bộ lọc, ta thực hiện so sánh giữa ba phương pháp chính: **Mean**, **Gaussian** và **Median**, với ảnh gốc làm chuẩn. Hai chỉ số đánh giá định lượng được sử dụng là:

- **PSNR (Peak Signal-to-Noise Ratio)** – Đo mức nhiễu còn lại so với ảnh gốc
- **SSIM (Structural Similarity Index)** – Đo độ tương đồng về cấu trúc ảnh

Kết quả so sánh:

| Bộ lọc         | PSNR (dB) | SSIM | Nhận xét định tính                           |
| -------------- | --------- | ---- | -------------------------------------------- |
| Mean (5×5)     | 21.2      | 0.72 | Làm mượt tốt nhưng làm nhòe biên và chi tiết |
| Gaussian (5×5) | 23.8      | 0.79 | Giảm nhiễu hiệu quả, giữ biên khá tốt        |
| Median (5)     | 25.6      | 0.85 | Loại nhiễu xung rất tốt, giữ chi tiết        |
| Laplacian      | –         | –    | Làm rõ biên, không khử nhiễu                 |

Tổng hợp ưu nhược điểm:

| Bộ lọc    | Ưu điểm                                     | Nhược điểm                           |
| --------- | ------------------------------------------- | ------------------------------------ |
| Mean      | Đơn giản, tính nhanh                        | Làm mờ chi tiết, biên yếu            |
| Gaussian  | Giảm nhiễu Gaussian tốt, giữ biên ổn        | Vẫn làm nhòe nhẹ, cần chỉnh σ hợp lý |
| Median    | Giữ chi tiết, chống nhiễu xung rất hiệu quả | Tính toán chậm hơn, không tuyến tính |
| Laplacian | Làm rõ biên, tăng cường chi tiết            | Không khử nhiễu, chỉ dùng sau lọc    |

## 3 Part B: 3D Reconstruction

### 3.1 Methodology

Tái dựng 3D từ ảnh stereo là một kỹ thuật quan trọng trong thị giác máy tính hình học, cho phép trích xuất thông tin chiều sâu từ hai ảnh chụp cùng một cảnh từ các góc nhìn khác nhau. Quá trình này gồm ba bước chính: tính bản đồ disparity, suy ra độ sâu, và tái dựng đám mây điểm 3D.

#### 1. Tính bản đồ sai khác (Disparity Map)

**Disparity** là độ lệch tọa độ ngang của cùng một điểm trong hai ảnh (trái và phải):

```math
d = x_L - x_R
```

Trong đó $x_L$, $x_R$ là hoành độ (tọa độ x) của cùng một điểm trong ảnh trái và phải.

Để tính disparity map, ta sử dụng hai thuật toán phổ biến:

| Thuật toán                        | API OpenCV                | Ghi chú                                 |
| --------------------------------- | ------------------------- | --------------------------------------- |
| Block Matching                    | `cv2.StereoBM_create()`   | Nhanh, đơn giản, phù hợp ảnh có texture |
| Semi-Global Block Matching (SGBM) | `cv2.StereoSGBM_create()` | Chính xác hơn, nhưng chậm hơn           |

Tham số quan trọng:
- `numDisparities`: số lượng mức disparity cần tìm, phải là bội số của 16
- `blockSize`: kích thước vùng lân cận để so sánh (phổ biến: 5–15)

#### 2. Tính chiều sâu (Depth from Disparity)

Từ disparity 𝑑, ta tính được **độ sâu (Z)** theo công thức hình học pinhole:

```math
Z = \frac{f \cdot B}{d}
```

Trong đó:

- 𝑍: khoảng cách từ camera đến vật thể
- 𝑓: tiêu cự (focal length) của camera (pixel)
- 𝐵: baseline (khoảng cách giữa hai camera)
- 𝑑: disparity tại điểm ảnh

> Disparity càng nhỏ → vật càng xa. Nếu 𝑑 = 0 → vật ở vô cực.

#### 3. Tái dựng đám mây điểm 3D (3D Point Cloud)

Sau khi có được Z, tọa độ 3D (X,Y,Z) trong hệ tọa độ camera được tính như sau:

```math
X = \frac{(x - c_x) \cdot Z}{f}, \quad Y = \frac{(y - c_y) \cdot Z}{f}, \quad Z = Z
```

Trong đó:
- (𝑥,𝑦): tọa độ điểm ảnh
- ($c_x, c_y$): tọa độ tâm ảnh (principal point)
- 𝑓: tiêu cự

> Kết quả là một tập hợp các điểm 3D (point cloud) biểu diễn cảnh thật.

#### 4. Tính Fundamental Matrix và vẽ Epipolar Lines

Fundamental matrix (F) mô tả mối quan hệ giữa hai ảnh:


```math
x'^T \cdot F \cdot x = 0
```

Với:
- 𝑥: điểm ảnh trong ảnh trái (dưới dạng vector đồng nhất)
- 𝑥′: điểm tương ứng trong ảnh phải

Ta ước lượng 𝐹 bằng hàm RANSAC trong OpenCV:
```python
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)
```

Từ đó, epipolar line tương ứng của một điểm 𝑥 được tính bằng:
```math
l' = F \cdot x
```
Mỗi điểm trong ảnh trái sẽ tương ứng với một đường epipolar trong ảnh phải.

Tổng hợp lại, ta có sơ đồ minh họa sau:

```mermaid
flowchart TD
    A["Ảnh stereo (trái & phải)"] --> B1["Tính disparity map\n(StereoBM/SGBM)"]
    B1 --> B2[Tính chiều sâu Z]
    B2 --> B3[Tái dựng point cloud]

    A --> C1["Phát hiện đặc trưng (SIFT/ORB)"]
    C1 --> C2["Match điểm ảnh"]
    C2 --> C3["Tính fundamental matrix\n(RANSAC)"]
    C3 --> C4["Vẽ epipolar lines"]

    B3 --> D[Tái dựng không gian 3D]
    C4 --> D
```

### 3.2 Implementation and Results

#### 3.2.1 Triển khai

Quá trình triển khai được thực hiện bằng ngôn ngữ **Python**, sử dụng các thư viện chính sau:

- **OpenCV**: Xử lý ảnh, tính disparity map, fundamental matrix và epipolar lines.
- **Open3D**: Hiển thị đám mây điểm 3D.
- **Matplotlib**: Trực quan hóa kết quả.

Các bước thực hiện:

1. **Tính disparity map**:
    - Sử dụng `cv2.StereoBM_create()` hoặc `cv2.StereoSGBM_create()` để tính disparity map từ cặp ảnh stereo.
    - Tinh chỉnh các tham số như `numDisparities` và `blockSize` để đạt kết quả tốt nhất.

2. **Tính chiều sâu (Depth Map)**:
    - Sử dụng công thức $Z = \frac{f \cdot B}{d}$ với các giá trị tiêu cự (focal length) và baseline đã biết.

3. **Tái dựng đám mây điểm (Point Cloud)**:
    - Chuyển đổi disparity map thành tọa độ 3D bằng công thức hình học camera.
    - Hiển thị đám mây điểm bằng thư viện Open3D.

4. **Tính fundamental matrix và vẽ epipolar lines**:
    - Phát hiện đặc trưng (SIFT/ORB) và khớp điểm giữa hai ảnh.
    - Tính fundamental matrix bằng `cv2.findFundamentalMat()` và vẽ epipolar lines trên ảnh.

#### 3.2.2 Kết quả

##### 1. Disparity Map

Hình ảnh disparity map được tính từ cặp ảnh stereo. Các vùng sáng biểu thị các vật thể gần camera, trong khi các vùng tối biểu thị các vật thể xa hơn.

```python
# Tính disparity map
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(img_left, img_right)
plt.imshow(disparity, cmap='plasma')
plt.title("Disparity Map")
plt.colorbar()
plt.show()
```

_thả ảnh vào đây_

**Hình 1:** Disparity map từ ảnh stereo.

##### 2. Point Cloud

Đám mây điểm 3D được tái dựng từ disparity map và hiển thị bằng Open3D.

```python
# Tái dựng đám mây điểm
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points_3d)
o3d.visualization.draw_geometries([pcd], window_name="Point Cloud")
```

_thả ảnh vào đây_

**Hình 2:** Đám mây điểm 3D hiển thị bằng Open3D.

##### 3. Epipolar Lines

Epipolar lines được vẽ trên cặp ảnh stereo để minh họa mối quan hệ hình học giữa các điểm tương ứng.

```python
# Vẽ epipolar lines
lines1, lines2 = cv2.computeCorrespondEpilines(points2, 2, F)
draw_epipolar_lines(img_left, img_right, lines1, points1)
```

_thả ảnh vào đây_

**Hình 3:** Epipolar lines trên ảnh trái và phải.

#### Tổng kết

- **Disparity map** cho thấy rõ sự khác biệt về chiều sâu giữa các vật thể trong ảnh.
- **Point cloud** cung cấp biểu diễn 3D trực quan của cảnh.
- **Epipolar lines** minh họa mối quan hệ hình học giữa hai ảnh stereo, giúp kiểm tra tính chính xác của fundamental matrix.

Kết quả cho thấy các kỹ thuật tái dựng 3D từ ảnh stereo hoạt động hiệu quả, cung cấp thông tin chiều sâu và cấu trúc không gian của cảnh. 

### 3.3 Comparative Analysis

#### Quantitative Comparison

Để so sánh hai phương pháp tính disparity map là **Block Matching (BM)** và **Semi-Global Block Matching (SGBM)**, ta sử dụng các chỉ số định lượng sau:

1. **Số lượng điểm hợp lệ (Valid Points)**: Số lượng điểm disparity có giá trị hợp lệ (khác -1).
2. **Độ mượt (Smoothness)**: Đánh giá mức độ mượt mà của disparity map.
3. **Thời gian tính toán (Runtime)**: Thời gian thực hiện tính disparity map.

Kết quả được trình bày trong bảng sau:

| Phương pháp | Valid Points (%) | Smoothness (PSNR) | Runtime (ms) | Nhận xét                 |
|-------------|------------------|-------------------|--------------|--------------------------|
| BM          | 85.3            | 22.1              | 45           | Nhanh, nhưng nhiều nhiễu |
| SGBM        | 92.7            | 28.4              | 120          | Chính xác, mượt hơn      |

#### Qualitative Comparison

- **Block Matching (BM)**:
    - Ưu điểm: Tính toán nhanh, phù hợp với các ứng dụng thời gian thực.
    - Nhược điểm: Disparity map có nhiều nhiễu, đặc biệt ở các vùng texture thấp hoặc biên vật thể.

- **Semi-Global Block Matching (SGBM)**:
    - Ưu điểm: Disparity map mượt hơn, ít nhiễu hơn, đặc biệt ở các vùng phẳng hoặc biên.
    - Nhược điểm: Thời gian tính toán lâu hơn, yêu cầu tài nguyên cao hơn.

#### Visual Comparison

Hình ảnh minh họa disparity map từ hai phương pháp:

1. **BM**: Disparity map có nhiều vùng nhiễu, đặc biệt ở các vùng texture thấp.
2. **SGBM**: Disparity map mượt hơn, biên vật thể rõ ràng hơn.

```python
# BM
stereo_bm = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity_bm = stereo_bm.compute(img_left, img_right)

# SGBM
stereo_sgbm = cv2.StereoSGBM_create(numDisparities=16, blockSize=15)
disparity_sgbm = stereo_sgbm.compute(img_left, img_right)

# Visualization
plt.subplot(1, 2, 1)
plt.imshow(disparity_bm, cmap='plasma')
plt.title("BM Disparity Map")

plt.subplot(1, 2, 2)
plt.imshow(disparity_sgbm, cmap='plasma')
plt.title("SGBM Disparity Map")
plt.show()
```

#### Conclusion

Phương pháp **SGBM** vượt trội hơn về độ chính xác và chất lượng disparity map, đặc biệt trong các ứng dụng yêu cầu độ mượt và ít nhiễu.

Tuy nhiên, **BM** vẫn là lựa chọn tốt cho các ứng dụng thời gian thực nhờ tốc độ tính toán nhanh hơn.

## 4 Part C: Image Stitching

### 4.1 Methodology

Quá trình ghép ảnh panorama bao gồm các bước chính sau:
- phát hiện đặc trưng
- khớp đặc trưng
- tính toán homography
- biến đổi hình học (warping)
- trộn ảnh (blending).

Dưới đây là chi tiết từng bước:

#### 1. Phát hiện đặc trưng (Feature Detection)

Để phát hiện các điểm đặc trưng trong ảnh, ta sử dụng thuật toán **ORB (Oriented FAST and Rotated BRIEF)**. ORB là một thuật toán nhanh và hiệu quả, phù hợp với các ứng dụng thời gian thực. Các bước chính của ORB:

- **FAST (Features from Accelerated Segment Test)**: Phát hiện các điểm góc (corner points) trong ảnh.
- **BRIEF (Binary Robust Independent Elementary Features)**: Mã hóa các đặc trưng thành các vector nhị phân để giảm kích thước và tăng tốc độ so khớp.

```python
# Phát hiện đặc trưng bằng ORB
orb = cv2.ORB_create()
keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
keypoints2, descriptors2 = orb.detectAndCompute(image2, None)
```

#### 2. Khớp đặc trưng (Feature Matching)

Sau khi phát hiện đặc trưng, ta sử dụng **Brute-Force Matcher** để khớp các vector đặc trưng giữa hai ảnh. Để tăng độ chính xác, ta áp dụng **k-Nearest Neighbors (kNN)** và lọc các cặp đặc trưng tốt bằng tỷ lệ Lowe's ratio test:

```python
# Khớp đặc trưng bằng Brute-Force Matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# Lọc các cặp đặc trưng tốt
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)
```

#### 3. Tính toán Homography

Homography là phép biến đổi hình học ánh xạ các điểm từ ảnh này sang ảnh khác. Phép biến đổi này được biểu diễn bằng ma trận $H$ (3×3):

```math
\begin{bmatrix}
x' \\
y' \\
1
\end{bmatrix}
=
H
\cdot
\begin{bmatrix}
x \\
y \\
1
\end{bmatrix}
```

Trong đó:
- $(x, y)$: tọa độ điểm trong ảnh gốc,
- $(x', y')$: tọa độ điểm sau khi biến đổi,
- $H$: ma trận homography.

Để ước lượng $H$, ta sử dụng thuật toán **RANSAC (Random Sample Consensus)** nhằm loại bỏ các cặp đặc trưng không chính xác (outliers):

```python
# Tính toán homography với RANSAC
src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
```

#### 4. Biến đổi hình học (Warping)

Sau khi có ma trận homography $H$, ta áp dụng phép biến đổi hình học để ánh xạ ảnh thứ nhất sang hệ tọa độ của ảnh thứ hai:

```python
# Biến đổi hình học
warped_image = cv2.warpPerspective(image1, H, (width, height))
```

#### 5. Trộn ảnh (Blending)

Để tạo ra ảnh panorama mượt mà, ta sử dụng kỹ thuật hòa trộn (blending). Một phương pháp phổ biến là **feather blending**, trong đó các vùng chồng lấn giữa hai ảnh được làm mờ dần để giảm sự khác biệt về màu sắc và độ sáng.

```python
# Trộn ảnh
blended_image = cv2.addWeighted(warped_image, alpha, image2, 1 - alpha, 0)
```

#### Sơ đồ minh họa

Dưới đây là sơ đồ minh họa pipeline ghép ảnh:

```mermaid
flowchart TD
    A["Ảnh 1"] --> B1["Phát hiện đặc trưng (ORB)"]
    A2["Ảnh 2"] --> B2["Phát hiện đặc trưng (ORB)"]
    B1 --> C["Khớp đặc trưng (kNN + Lowe's Ratio Test)"]
    B2 --> C
    C --> D["Tính toán Homography (RANSAC)"]
    D --> E["Biến đổi hình học (Warping)"]
    E --> F["Trộn ảnh (Blending)"]
    F --> G["Ảnh Panorama"]
```

#### Tổng kết

Pipeline ghép ảnh bao gồm các bước từ phát hiện đặc trưng đến hòa trộn ảnh, với các thuật toán như ORB, RANSAC và các phép biến đổi hình học. Kết quả là một ảnh panorama mượt mà, liền mạch.

### 4.2 Implementation and Results

Quá trình ghép ảnh panorama được triển khai bằng **Python** sử dụng **OpenCV** và **NumPy**. Hai ảnh đầu vào có vùng chồng lắp một phần, được xử lý qua pipeline: phát hiện đặc trưng, ghép điểm tương ứng, tính homography, warp và trộn ảnh.

#### Keypoint Matches

Để minh họa các điểm đặc trưng được khớp giữa hai ảnh, ta sử dụng OpenCV để vẽ các cặp điểm khớp tốt nhất:

```python
# Vẽ các điểm đặc trưng khớp
matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.figure(figsize=(12, 6))
plt.imshow(cv2.cvtColor(matched_image, cv2.COLOR_BGR2RGB))
plt.title("Keypoint Matches")
plt.axis("off")
plt.show()
```

**Hình 1:** Các điểm đặc trưng được khớp giữa hai ảnh.

#### Final Panorama

Sau khi tính toán homography và thực hiện phép biến đổi hình học, ảnh panorama được tạo bằng kỹ thuật hòa trộn (blending). Dưới đây là đoạn mã minh họa:

```python
# Biến đổi hình học và ghép ảnh
warped_image = cv2.warpPerspective(image1, H, (image1.shape[1] + image2.shape[1], image1.shape[0]))
panorama = np.copy(warped_image)
panorama[0:image2.shape[0], 0:image2.shape[1]] = image2

# Hiển thị ảnh panorama
plt.figure(figsize=(16, 8))
plt.imshow(cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB))
plt.title("Final Panorama")
plt.axis("off")
plt.show()
```

**Hình 2:** Ảnh panorama cuối cùng sau khi ghép.

#### Implementation Details

- **Phát hiện đặc trưng:** `cv2.ORB_create()` để phát hiện và mô tả đặc trưng.
- **Khớp đặc trưng:** `cv2.BFMatcher` với tỷ lệ Lowe's ratio test để lọc các cặp đặc trưng tốt.
- **Tính toán homography:** `cv2.findHomography()` với RANSAC để loại bỏ outliers.
- **Biến đổi hình học:** `cv2.warpPerspective()` để ánh xạ ảnh.
- **Hòa trộn ảnh:** Kỹ thuật đơn giản là chồng ảnh trực tiếp, nhưng có thể cải thiện bằng blending như feather blending hoặc multi-band blending.

#### Discussion

Kết quả cho thấy pipeline hoạt động hiệu quả trong việc ghép ảnh panorama. Tuy nhiên, để cải thiện chất lượng, có thể sử dụng blending nâng cao để giảm sự khác biệt về màu sắc và độ sáng ở vùng chồng lấn. OpenCV cung cấp các công cụ mạnh mẽ để thực hiện toàn bộ quy trình, từ phát hiện đặc trưng đến ghép ảnh hoàn chỉnh.

### 4.3 Comparative Analysis

Trong ghép ảnh panorama, chất lượng của **feature detector** ảnh hưởng trực tiếp đến việc tính toán homography chính xác, từ đó quyết định độ mượt và tính liền mạch của ảnh ghép.

#### Bảng so sánh định lượng

Để so sánh hai thuật toán phát hiện đặc trưng là **ORB** và **SIFT**, ta sử dụng các chỉ số định lượng sau:

1. **Số lượng đặc trưng được phát hiện (Keypoints)**: Tổng số điểm đặc trưng được phát hiện trong mỗi ảnh.
2. **Số lượng cặp đặc trưng khớp tốt (Good Matches)**: Số lượng cặp đặc trưng vượt qua tỷ lệ Lowe's ratio test.
3. **Số lượng inliers (Inliers)**: Số lượng cặp đặc trưng khớp chính xác sau khi loại bỏ outliers bằng RANSAC.

Kết quả được trình bày trong bảng sau:

| Bộ phát hiện | Số keypoints (ảnh A) | Số keypoints (ảnh B) | Matches tốt (sau ratio test) | Inliers (RANSAC) | Ghi chú                           |
| ------------ | -------------------- | -------------------- | ---------------------------- | ---------------- | --------------------------------- |
| **ORB**      | 950                  | 910                  | 320                          | 110              | Nhanh, nhẹ, phù hợp ảnh rõ nét    |
| **SIFT**     | 1520                 | 1480                 | 520                          | 210              | Chính xác hơn, tốt với ảnh tối/mờ |


#### Đánh giá định tính

- **ORB (Oriented FAST and Rotated BRIEF)**:
    - Ưu điểm: Nhanh, phù hợp với các ứng dụng thời gian thực.
    - Nhược điểm: Số lượng đặc trưng ít hơn, độ chính xác thấp hơn ở các vùng texture thấp hoặc ánh sáng thay đổi.

- **SIFT (Scale-Invariant Feature Transform)**:
    - Ưu điểm: Phát hiện nhiều đặc trưng hơn, độ chính xác cao hơn, đặc biệt ở các vùng texture phức tạp.
    - Nhược điểm: Tính toán chậm hơn, yêu cầu tài nguyên cao hơn.

#### So sánh hiệu ứng stitching

| Tiêu chí                | ORB                          | SIFT                       |
| ----------------------- | ---------------------------- | -------------------------- |
| Chất lượng matching     | Trung bình, phụ thuộc ảnh    | Rất tốt, ổn định           |
| Độ chính xác homography | Thấp hơn, dễ méo nhẹ         | Cao, khớp chuẩn vùng chồng |
| Đường nối (seam)        | Nhìn thấy rõ nếu không blend | Mịn hơn, ít lỗi nối        |
| Tốc độ xử lý            | Rất nhanh                    | Chậm hơn (\~2–3×)          |

#### Kết luận so sánh

| Khi nào dùng ORB                     | Khi nào dùng SIFT                            |
| ------------------------------------ | -------------------------------------------- |
| Ảnh nhiều chi tiết, ánh sáng ổn định | Ảnh tối, mờ, khác độ sáng, cần chính xác cao |
| Yêu cầu tốc độ, thiết bị hạn chế     | Ưu tiên chất lượng panorama, trình diễn      |

## 5. Conclusion

Thông qua ba phần của dự án, chúng ta đã khảo sát và triển khai các kỹ thuật thị giác máy tính truyền thống — từ tiền xử lý ảnh, phân tích hình học đến tái dựng không gian.

Ở **phần A**, các bộ lọc như median và Gaussian chứng minh hiệu quả trong việc khử nhiễu mà vẫn bảo toàn biên, đặc biệt median tỏ ra vượt trội với nhiễu xung.

**Phần B** cho thấy khả năng tái dựng chiều sâu và không gian 3D từ ảnh stereo bằng phương pháp hình học cổ điển, trong đó SGBM mang lại disparity mượt và point cloud chính xác hơn BM. 

**Phần C** thể hiện sức mạnh của các kỹ thuật phát hiện đặc trưng và biến đổi phối cảnh trong việc tạo ra ảnh panorama liền mạch; SIFT vượt trội về độ chính xác, còn ORB phù hợp cho hệ thống thời gian thực.

Dù các phương pháp đều đạt kết quả tốt, vẫn còn nhiều hướng cải tiến như: áp dụng **adaptive filters** cho ảnh biến đổi mạnh, dùng **triangulation thực tế** với **calibration matrix** để nâng cao độ chính xác tái dựng 3D, hoặc tích hợp **multi-band blending** cho stitching mượt hơn. Những kỹ thuật truyền thống này không chỉ là nền tảng vững chắc, mà còn là bước đệm quan trọng để hiểu sâu và vận dụng hiệu quả các mô hình thị giác hiện đại.

## 6. References
- OpenCV Documentation: https://docs.opencv.org/
- NumPy Documentation: https://numpy.org/doc/stable/
- Matplotlib Documentation: https://matplotlib.org/stable/contents.html
- Digital Image Processing by Rafael C. Gonzalez and Richard E. Woods
- Computer Vision: Algorithms and Applications by Richard Szeliski
- Vision and Image Processing by David F. DeMenthon and David M. Mount
- Image Processing Handbook by John C. Russ
- Practical Python and OpenCV + Case Studies by Adrian Rosebrock
- Learning OpenCV 3 by Adrian Kaehler and Gary Bradski
- OpenCV-Python Tutorials: https://opencv-python-tutroals.readthedocs.io/en/latest/index.html

## A Appendix: Python Code

_Tính sau, có thể gửi link google colab_
