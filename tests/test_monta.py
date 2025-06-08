import os
import sys
import csv
import shutil

# Add the parent directory to sys.path to allow importing from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from monta import montar_dataset

def test_montar_dataset():
    """
    Test the montar_dataset function by creating a temporary test directory,
    copying a sample image, and generating a small dataset.
    """
    # Get the project root directory (parent of tests directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create a temporary test directory
    test_dir = os.path.join(project_root, "test_dataset")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Create subdirectories for beans
    os.makedirs(os.path.join(test_dir, "ruins"))
    os.makedirs(os.path.join(test_dir, "bons"))
    
    # Copy a sample image to the test directory
    sample_dirs = ['ruins', 'bons']
    sample_copied = False
    
    for dir_name in sample_dirs:
        source_dir = os.path.join(project_root, dir_name)
        if os.path.exists(source_dir):
            for file_name in os.listdir(source_dir):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    source_path = os.path.join(source_dir, file_name)
                    dest_path = os.path.join(test_dir, dir_name, file_name)
                    shutil.copy2(source_path, dest_path)
                    print(f"Copied {source_path} to {dest_path}")
                    sample_copied = True
                    break
            if sample_copied:
                break
    
    if not sample_copied:
        print("No sample images found to copy.")
        shutil.rmtree(test_dir)
        return False
    
    # Generate the dataset
    output_csv = os.path.join(test_dir, "test_dataset.csv")
    try:
        montar_dataset(test_dir, output_csv)
    except Exception as e:
        print(f"Error generating dataset: {e}")
        shutil.rmtree(test_dir)
        return False
    
    # Verify the CSV file was created and has data
    if not os.path.exists(output_csv):
        print(f"Output CSV file not created: {output_csv}")
        shutil.rmtree(test_dir)
        return False
    
    # Count rows in the CSV
    row_count = 0
    with open(output_csv, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            row_count += 1
    
    print(f"Generated dataset with {row_count-1} data rows (plus header).")
    
    # Check if the segmented images were created
    recorte_dir = os.path.join(test_dir, f"{sample_dirs[0]}_recorte")
    segregado_dir = os.path.join(test_dir, f"{sample_dirs[0]}_segregado")
    
    if not os.path.exists(recorte_dir) or not os.path.exists(segregado_dir):
        print("Recorte or segregado directories not created.")
        shutil.rmtree(test_dir)
        return False
    
    segregado_count = len(os.listdir(segregado_dir))
    print(f"Generated {segregado_count} segmented bean images.")
    
    # Clean up
    print(f"Test completed successfully. Cleaning up {test_dir}...")
    shutil.rmtree(test_dir)
    
    return True

if __name__ == "__main__":
    success = test_montar_dataset()
    print(f"Test {'passed' if success else 'failed'}.")