import sys
import os

# Imports the root directory to the path in order to import project modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from PIL import Image
from utils.image_divider import merge_images_from_array


def load_images_from_folder(folder):
    """
    Loads images from a directory into a list of PIL Image objects.
    """
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        try:
            with Image.open(img_path) as img:
                images.append(
                    img.copy()
                )  # Use img.copy() if you plan to close the image
        except IOError:
            # You can skip files that aren't images
            print(f"Failed to load {filename}")
    return images


def dictionary_to_array(list):
    """
    Extracts the masks from the mask details dictionary.

    
    """
    array = []

    for mask in list:
        array.append(mask["Mask image"])

    return array
# images = load_images_from_folder(".\\ImageExtractor\\Images\\Divided")
# merge_images_from_array(images,".\\ImageExtractor\\Images\\TestOutput.png")