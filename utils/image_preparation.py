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


def load_images_from_folder(folder):
    """
    Loads images from a directory into a list of PIL Image objects.
    """

    # images = __sort_directory__(folder)
    # for i in range(len(images)):

    #     img = images[i]
    #     img = tf_image.resize(img, (512, 512))
    #     img = tf.cast(img, tf.float32) / 255.0
    #     img = tf_image.convert_image_dtype(img, "float32")
    #     images.append(img)

    # return images

    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        try:
            with Image.open(img_path) as img:
                img = img.copy()
                img = tf_image.resize(img, (512, 512))
                img = tf.cast(img, tf.float32) / 255.0
                img = tf_image.convert_image_dtype(img, "float32")
                images.append(img)
        except IOError:
            # You can skip files that aren't images
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
