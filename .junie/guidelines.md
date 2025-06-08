# Bean Image Processing Project Guidelines

This document provides guidelines for development, testing, and configuration of the Bean Image Processing project.

## Build/Configuration Instructions

### Environment Setup

1. **Python Environment**: This project requires Python 3.6 or higher.

2. **Dependencies Installation**:
   ```bash
   pip install -r requirements.txt
   ```

   The project depends on the following packages:
   - opencv-python: For image processing operations
   - numpy: For numerical operations
   - scikit-learn: For machine learning algorithms
   - pandas: For data manipulation

3. **Directory Structure**:
   The project expects the following directory structure:
   ```
   project_root/
   ├── bons/                  # Directory containing "good" bean images
   ├── ruins/                 # Directory containing "bad" bean images
   ├── bons_recorte/          # Auto-generated cropped images of good beans
   ├── bons_segregado/        # Auto-generated segmented good bean images
   ├── ruins_recorte/         # Auto-generated cropped images of bad beans
   ├── ruins_segregado/       # Auto-generated segmented bad bean images
   ├── monta.py               # Main script for dataset generation
   ├── segmenta.py            # Module for bean segmentation
   └── requirements.txt       # Project dependencies
   ```

   The directories `*_recorte` and `*_segregado` will be created automatically if they don't exist.

## Testing Information

### Running Existing Tests

1. **Segmentation Test**:
   ```bash
   python test_segmenta.py
   ```
   This test verifies the bean segmentation functionality by:
   - Loading a sample image from the 'ruins' or 'bons' directory
   - Segmenting the beans in the image
   - Creating a visualization with bounding boxes and contours
   - Saving the visualization to 'test_segmentation_result.jpg'

2. **Dataset Generation Test**:
   ```bash
   python test_monta.py
   ```
   This test verifies the dataset generation functionality by:
   - Creating a temporary test directory
   - Copying a sample image to the test directory
   - Generating a dataset from the sample image
   - Verifying that the CSV file and segmented images were created correctly

### Adding New Tests

When adding new tests to the project, follow these guidelines:

1. **Test File Naming**: Name test files with the prefix `test_` followed by the name of the module being tested (e.g., `test_segmenta.py`).

2. **Test Function Structure**:
   - Each test function should focus on testing a specific functionality
   - Use descriptive function names that indicate what is being tested
   - Include docstrings explaining the purpose of the test
   - Return a boolean indicating success or failure

3. **Test Cleanup**: Ensure that tests clean up any temporary files or directories they create.

4. **Example Test Structure**:
   ```python
   def test_some_functionality():
       """
       Test description explaining what is being tested and how.
       """
       # Setup
       # ...
       
       # Execute the functionality being tested
       # ...
       
       # Verify the results
       # ...
       
       # Cleanup
       # ...
       
       return success_boolean
   ```

## Development Guidelines

### Code Style

1. **PEP 8**: Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.

2. **Docstrings**: Include docstrings for all modules, classes, and functions following the [NumPy docstring style](https://numpydoc.readthedocs.io/en/latest/format.html).

3. **Type Hints**: Consider adding type hints to function signatures to improve code readability and enable static type checking.

### Image Processing Workflow

The project follows this general workflow for processing bean images:

1. **Image Loading**: Load images using `cv2.imread()`.

2. **Preprocessing**:
   - Convert to grayscale using `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
   - Apply Gaussian blur to reduce noise using `cv2.GaussianBlur()`

3. **Segmentation**:
   - Apply binary thresholding with Otsu's method
   - Use morphological operations to clean up the binary image
   - Find contours of the beans

4. **Feature Extraction**:
   - Extract color features (mean and standard deviation of BGR channels)
   - Extract shape features (area, perimeter, circularity, etc.)
   - Extract texture features (entropy, Hu moments, etc.)

5. **Dataset Generation**:
   - Save features to a CSV file
   - Save segmented bean images

### Debugging Tips

1. **Visualization**: Use OpenCV's visualization functions to debug image processing steps:
   ```python
   cv2.imwrite("debug_step_name.jpg", debug_image)
   ```

2. **Contour Filtering**: When segmenting beans, adjust the area threshold in `segmentar_feijoes()` if too many or too few beans are being detected:
   ```python
   if area < 200:  # Adjust this threshold as needed
       continue
   ```

3. **HSV Thresholding**: When cropping the sheet in `recortar_folha()`, adjust the HSV thresholds if the sheet is not being detected correctly:
   ```python
   lower_white = np.array([0, 0, 200])  # Adjust these values as needed
   upper_white = np.array([180, 60, 255])
   ```

### Performance Considerations

1. **Image Size**: Large images may slow down processing. Consider resizing images if performance is an issue.

2. **Batch Processing**: When processing multiple images, use batch processing to avoid loading all images into memory at once.

3. **Parallel Processing**: Consider using multiprocessing for CPU-bound tasks like feature extraction.