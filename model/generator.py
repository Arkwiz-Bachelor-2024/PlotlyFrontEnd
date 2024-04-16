import sys
import os

# Imports the root directory to the path in order to import project modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt




def extract_predictions(images, model):
    """
    This function extracts specific images and predictions based on the provided images and model.

    """

    pred_masks = []

    for image in images:

        # Prediction
        image = np.expand_dims(image, axis=0)
        pred_mask_probs = model.predict(image)
        pred_mask = np.argmax(pred_mask_probs.squeeze(), axis=-1)

        # Collection
        pred_masks.append(pred_mask)

    return pred_masks

