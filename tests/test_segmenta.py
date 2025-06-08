import os
import sys
import cv2
import numpy as np

# Add the parent directory to sys.path to allow importing from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from segmenta import segmentar_feijoes

def test_segmentar_feijoes():
    """
    Test the segmentar_feijoes function by loading an image, segmenting the beans,
    and saving the results.
    """
    # Find an image to test with
    test_dirs = ['ruins', 'bons']
    test_image_path = None
    
    # Get the project root directory (parent of tests directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for dir_name in test_dirs:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path):
            for file_name in os.listdir(dir_path):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    test_image_path = os.path.join(dir_path, file_name)
                    break
            if test_image_path:
                break
    
    if not test_image_path:
        print("No test images found in 'ruins' or 'bons' directories.")
        return False
    
    # Load the image
    print(f"Testing with image: {test_image_path}")
    image = cv2.imread(test_image_path)
    if image is None:
        print(f"Failed to load image: {test_image_path}")
        return False
    
    # Segment the beans
    masks, bboxes = segmentar_feijoes(image)
    
    # Check if any beans were detected
    if not masks:
        print("No beans detected in the image.")
        return False
    
    print(f"Successfully detected {len(masks)} beans.")
    
    # Create a visualization of the segmentation
    result = image.copy()
    for i, (mask, bbox) in enumerate(zip(masks, bboxes)):
        x, y, w, h = bbox
        # Draw bounding box
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Draw contour
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(result, contours, -1, (0, 0, 255), 2)
        # Add label
        cv2.putText(result, f"Bean {i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Save the result
    output_path = os.path.join(project_root, "/tests/test_segmentation_result.jpg")
    cv2.imwrite(output_path, result)
    print(f"Saved visualization to: {output_path}")
    
    return True

if __name__ == "__main__":
    success = test_segmentar_feijoes()
    print(f"Test {'passed' if success else 'failed'}.")