import sys
import os

# Imports the root directory to the path in order to import project modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from natsort import natsorted
from PIL import Image
from utils.image_divider import merge_images_from_array
import tensorflow as tf
from tensorflow import data as tf_data
from tensorflow import io as tf_io
from tensorflow import image as tf_image
from tensorflow import cast, float32
import re
import numpy as np


def load_images_from_folder(folder):
    """
    Loads images from a directory into a list of PIL Image objects, resizing and converting them appropriately.

    :param folder: the folder where the images are located
    """
    images = []
    img_paths = __sort_directory__(folder)
    for filename in img_paths:
        try:
            with Image.open(filename) as img:
                img = img.copy()
                img = tf_image.resize(img, (512, 512))
                img = tf.cast(img, tf.float32) / 255.0
                img = tf_image.convert_image_dtype(img, "float32")
                images.append(img)
        except IOError:
            print(f"Failed to load {filename}")
            
    return images


def __sort_directory__(input_dir):
    """
    Extracts files from a directory into a naturally sorted array.

    :param input_dir: the directory where content shall be sorted.
    """

    input_files = natsorted(
        [os.path.join(input_dir, fname) for fname in os.listdir(input_dir)]
    )

    return input_files


def dictionary_to_array(dictionary, dictkey):
    """
    Extractracts information from a dictionary.

    :param dictionary: The dictionary which information shall be retrieved from.
    :param dictkey: The key of which information shall be retrieved.

    :returns: Array with the objects specified in the dictionary.

    """
    array = []
    for mask in dictionary:
        key = next(iter(mask))
        array.append(mask[key][dictkey])

    return array

def prepare_distribution(distribution):
    """
    Prepare the class distributions for further usage. Summerize all the distributions into an array consisting
    of the general class distributions over all the distributions.
    
    :param distribution: array of dictionaries with the class distributions 
    """

    # Prepare an empty array for the distributions
    sum_classes = np.zeros(5)

    for distributions in distribution:
        for cls, percent in distributions.items():
            sum_classes[cls] += percent

    # Checks if the sum is exsisting, to avoid division by zero.
    total = np.sum(sum_classes)
    if total > 0:
        # Convert the sum of the classes to percentages
        percent_classes = (sum_classes / total) * 100
    else:
        percent_classes = np.zeros(5)  

    return percent_classes

        


# images = load_images_from_folder(".\\ImageExtractor\\Images\\Divided")

# merge_images_from_array(images,".\\ImageExtractor\\Images\\TestOutput.png")
