import sys
import os

# Imports the root directory to the path in order to import project modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from utils.image_divider import split_image, merge_images_from_array
from utils.image_preparation import load_images_from_folder
from model.mask_generator import generate_masks_with_details


# The machine learning model that shall preform the classification.
MACHINE_LEARNING_MODEL = (
    "UNETplus_2x_100e_16b_Poly_Adam_low_wBCE_milestones_warmup+DA_mid"
)


def extract_masks():
    """
    Loads the images extracted from the ArcGIS API and extracts the masks using the base model.
    """

    # Paths for the images
    image_path = ".\\ImageExtractor\\Images\\output_image.tif"
    tiles_path = ".\\ImageExtractor\\Images\\Divided"

    # Split the image into tiles
    split_image(image_path, tiles_path)

    # Load the images
    images = load_images_from_folder(tiles_path)

    # Extract masks
    masks = generate_masks_with_details(
        images,
        MACHINE_LEARNING_MODEL,
    )
    print("Mask predicted.")

    # Dictonary containing the masks and its class distribution
    return masks
