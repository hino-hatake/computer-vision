def plot_images(original, filtered):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(filtered, cmap='gray')
    plt.title('Filtered Image')
    plt.axis('off')

    plt.show()