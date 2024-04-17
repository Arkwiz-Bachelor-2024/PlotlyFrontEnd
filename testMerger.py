from PIL import Image
import numpy as np
import math
import os

from utils.image_preparation import load_images_from_folder,__sort_directory__


def split_image(image_path, output_dir, tile_size=(512, 512)):
    """
    Splits the image at image_path into tiles of size tile_size and saves them to output_dir,
    discarding any part of the image that doesn't fit into the tiles exactly.
    """
    # Load the image
    image = Image.open(image_path)

    # Calculate the number of tiles in each dimension
    img_width, img_height = image.size
    tiles_x = img_width // tile_size[0]  # Use floor division to round down
    tiles_y = img_height // tile_size[1]  # Use floor division to round down

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Split the image into tiles and save
    for x in range(tiles_x):
        for y in range(tiles_y):
            # Define the coordinates of the rectangle for this tile
            left = x * tile_size[0]
            upper = y * tile_size[1]
            right = left + tile_size[0]
            lower = upper + tile_size[1]

            # Crop the image to this rectangle
            tile = image.crop((left, upper, right, lower))

            # Save the tile
            tile_path = os.path.join(output_dir, f"tile_{x}_{y}.png")
            tile.save(tile_path)


# Example usage
# split_image("ImageExtractor\\Images\\aerial_1km.tif", "ImageExtractor\\Images\\Divided")


def merge_images(
    tiles_folder, output_image_path, tiles_x, tiles_y, tile_size=(512, 512)
):
    """
    Merges an array of images back into a single image.

    :param tiles_folder: Folder containing all the smaller images.
    :param output_image_path: Path to save the merged image.
    :param tiles_x: Number of tile images along the x-axis.
    :param tiles_y: Number of tile images along the y-axis.
    :param tile_size: Size of each tile (width, height).
    """
    # Create a new image with the correct size
    merged_image = Image.new("RGB", (tiles_x * tile_size[0], tiles_y * tile_size[1]))

    # Iterate over each tile position and paste it into the merged image
    for x in range(tiles_x):
        for y in range(tiles_y):
            tile_path = os.path.join(tiles_folder, f"tile_{x}_{y}.png")
            tile = Image.open(tile_path)
            merged_image.paste(tile, (x * tile_size[0], y * tile_size[1]))

    # Save the merged image
    merged_image.save(output_image_path)


# merge_images("ImageExtractor\\Images\\Divided", "ImageExtractor\\Images\\OutputFile.png",8,6)


def merge_images_from_array(tiles, output_path, grid_size=(8,6), tile_size=(512, 512)):
    """
    Merge an array with images to one output image
    """

    # These should be set to the number of tiles horizontally and vertically
    merged_image = Image.new("RGB", (grid_size[0] * tile_size[0], grid_size[1] * tile_size[1]))
    for i, tile in enumerate(tiles):
        x = (i // grid_size[1]) * tile_size[0]
        y = (i % grid_size[1]) * tile_size[1]
        merged_image.paste(tile, (x, y))
    merged_image.save(output_path)
    print("Image saved to output path!")

# __sort_directory__("./ImageExtractor/Images/Divided")
merge_images_from_array(load_images_from_folder("./ImageExtractor/Images/Divided"),"./ImageExtractor/Images/MergedImage.png")