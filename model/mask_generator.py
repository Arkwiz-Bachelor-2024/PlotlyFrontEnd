import sys
import os
import json

# Imports the root directory to the path in order to import project modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from matplotlib.colors import ListedColormap
import numpy as np
import tensorflow as tf
from tensorflow import keras

from utils.image_preparation import load_images_from_folder

from PIL import Image
import matplotlib.cm as cm

from model.generator import extract_predictions
from model.metrics import get_class_distribution

# * Pre-determined Colourmap
# White, Red, Green, Blue, Gray in RGB
colors = [
    (1, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0.5, 0.5, 0.5),
]
cmap = ListedColormap(colors)


def generate_masks_with_details(images, model_name):
    """
    Given an array of images and the name of the chosen model, this function will generate masks and class distribution details for each image.

    Returns a dictonary containing the respective masks and their associated class distribution.

    """
    if images is None:
        raise ValueError("No images provided")

    if model_name is None:
        raise ValueError("No model name provided")

    try:
        # Load and predict images
        print(f"Loading model:{model_name}, and starting to predict masks")
        model_path = f"model/models/{model_name}"
        model = keras.models.load_model(model_path, compile=False)
        masks = extract_predictions(images, model)

    except Exception as e:
        print(f"An error occured while generating masks: {e}")

    results = []

    for i in range(len(masks)):

        class_distribution = get_class_distribution(masks[i])

        # Convert mask labels to image
        # print(type(masks[i]))
        mapped_data = cmap(masks[i])
        image_data = (mapped_data[:, :, :3] * 255).astype(np.uint8)

        # Create the image
        mask_img = Image.fromarray(image_data, "RGB")

        results.append(
            {
                i: {
                    "mask_image": mask_img,
                    "class_distribution": class_distribution,
                }
            }
        )

    return results
