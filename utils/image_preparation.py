import os
from PIL import Image


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
