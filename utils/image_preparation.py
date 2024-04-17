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

def numerical_sort(filename):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(filename)
    parts[1::2] = map(int, parts[1::2])
    return parts



def load_images_from_folder(folder):
    """
    Loads images from a directory into a list of PIL Image objects, resizing and converting them appropriately.
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

    """

    input_files = natsorted(
        [os.path.join(input_dir, fname) for fname in os.listdir(input_dir)]
    )

    return input_files


def dictionary_to_array(list):
    """
    Extracts the masks from the mask details dictionary.


    """
    array = []
    for mask in list:
        key = next(iter(mask))
        array.append(mask[key][f"mask_image"])

    return array


# images = load_images_from_folder(".\\ImageExtractor\\Images\\Divided")

# merge_images_from_array(images,".\\ImageExtractor\\Images\\TestOutput.png")
