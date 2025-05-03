# Image Filtering Project

## Overview
This project implements various image filtering techniques using Python. It provides a Jupyter Notebook for interactive use, allowing users to load images, apply different filters, and visualize the results.

## Project Structure
```
image-filtering
├── notebooks
│   └── image_filtering.ipynb
├── src
│   ├── filters
│   │   ├── __init__.py
│   │   ├── gaussian.py
│   │   ├── laplacian.py
│   │   ├── mean.py
│   │   └── median.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── image_io.py
│   │   ├── metrics.py
│   │   └── plotting.py
│   └── __init__.py
├── data
│   ├── input
│   │   └── sample.png
│   └── output
├── requirements.txt
└── README.md
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd image-filtering
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Open the Jupyter Notebook:
   ```
   jupyter notebook notebooks/image_filtering.ipynb
   ```

2. Load an image from the `data/input` directory or use the provided `sample.png`.

3. Apply various filters:
   - Gaussian Filter
   - Laplacian Filter
   - Mean Filter
   - Median Filter

4. Visualize the results interactively.

## Filtering Techniques
- **Gaussian Filter**: Smooths the image and reduces noise using a Gaussian kernel.
- **Laplacian Filter**: Enhances edges by calculating the second derivative of the image.
- **Mean Filter**: Averages the pixel values in a neighborhood to reduce noise.
- **Median Filter**: Replaces each pixel with the median value of the neighboring pixels, effective for removing salt-and-pepper noise.

## Output
Filtered images will be saved in the `data/output` directory.

## License
This project is licensed under the MIT License.