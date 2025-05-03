def calculate_psnr(original, filtered):
    mse = ((original - filtered) ** 2).mean()
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def calculate_ssim(original, filtered):
    from skimage.metrics import structural_similarity as ssim
    return ssim(original, filtered, multichannel=True)