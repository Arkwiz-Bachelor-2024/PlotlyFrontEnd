import sys
import os

# Imports the root directory to the path in order to import project modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from utils.ImageDivider import split_image, merge_images
from utils.image_preparation import load_images_from_folder
from model.mask_generator import generate_masks_with_details


def extract_masks():
    """
    Loads the images extracted from the ArcGIS API and extracts the masks using the base model.
    """

    # Paths for the images
    image_path = ".\\ImageExtractor\\Images\\output_image.tif"
    tiles_path = (".\\ImageExtractor\\Images\\Divided",)

    # Split the image into tiles
    ImageDivider.split_image(image_path, tiles_path)

    # Load the images
    images = load_images_from_folder(tiles_path)

    # Extract masks
    masks = generate_masks_with_details(images, "base_model.keras")

    # Dictonary containing the masks and its class distribution
    return masks
