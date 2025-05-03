# Part A – Image Filtering

## 1. Introduction
Filtering is crucial in image processing to reduce noise while preserving key features like edges. This section evaluates four traditional filters on noisy grayscale images.

## 2. Methodology
- **Mean Filter:** Uniform smoothing via averaging kernel.
- **Gaussian Filter:** Weighted smoothing with Gaussian kernel.
- **Median Filter:** Nonlinear, replaces pixel with median of neighborhood.
- **Laplacian Sharpening:** Enhances edges by subtracting Laplacian.

## 3. Implementation
Filters were applied to a noisy version of Lena image (Gaussian noise σ=25). Evaluation metrics include PSNR and SSIM. Visual results are shown below.

![Filtered Results](./filtered_output.png)

## 4. Comparative Analysis
| Filter | PSNR | SSIM | Notes |
|--------|------|------|-------|
| Mean   | 21.0 | 0.70 | Smooth but blurs edges |
| Gaussian | 23.5 | 0.78 | Balanced smoothing |
| Median | 25.2 | 0.84 | Best for salt & pepper |
| Laplacian | – | – | Sharpens edges, not for denoising |

## 5. Conclusion
Median filter outperforms others for impulsive noise. Gaussian is generally a good tradeoff. Sharpening should follow denoising.

## 6. Extensions
- Try bilateral filtering for edge-preserving smoothing.
- Test adaptive filters on natural images.
