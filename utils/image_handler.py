from PIL import Image
import numpy as np
import math
import os
import shutil

def clear_folder(folder):
    """
    Deletes all files in a given folder.

    :param folder: the paths to the folder which content shall be removed
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # This will delete a file or a symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # This will delete a directory and all its contents
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def split_image(image_path, output_dir, grid_size=(8,6), tile_size=(512, 512)):
    """
    Splits the image at image_path into tiles of size tile_size and saves them to output_dir,
    discarding any part of the image that doesn't fit into the tiles exactly.

    :param image_path: Path to the image that shall be split.
    :parm output_dir: Output path of the tiles.
    :param tile_size: The size of the tiles, default 512px*512px.
    """
    # Load the image
    image = Image.open(image_path)
    clear_folder(output_dir)
    

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Split the image into tiles and save
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
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


# split_image("ImageExtractor\\Images\\aerial_1km.tif", "ImageExtractor\\Images\\Divided")


def merge_images(
    tiles_folder, output_image_path, grid_size=(8,6), tile_size=(512, 512)
):
    """
    Merges an array of images back into a single image.

    :param tiles_folder: Folder containing all the smaller images.
    :param output_image_path: Path to save the merged image.
    :parm grid_size: The amount of tiles in x and y direction, default 8*6.
    :param tile_size: Size of each tile (width, height).
    """
    # Create a new image with the correct size
    merged_image = Image.new("RGB", (grid_size[0] * tile_size[0], grid_size[1] * tile_size[1]))

    # Iterate over each tile position and paste it into the merged image
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            tile_path = os.path.join(tiles_folder, f"tile_{x}_{y}.png")
            tile = Image.open(tile_path)
            merged_image.paste(tile, (x * tile_size[0], y * tile_size[1]))

    # Save the merged image
    merged_image.save(output_image_path)


# merge_images("ImageExtractor\\Images\\Divided", "ImageExtractor\\Images\\OutputFile.png",8,6)


def merge_images_from_array(tiles, output_path, grid_size=(8,6), tile_size=(512, 512)):
    """
    Merge an array with images to one output image.

    :param tiles: Array of images that shall be merged.
    :param output_path: The path where the output image shall be stored:
    :parm grid_size: The amount of tiles in x and y direction, default 8*6.
    :param tile_size: The size of each tile, default 512*512 px.
    """

    # Create output image with the right dimentions
    merged_image = Image.new("RGB", (grid_size[0] * tile_size[0], grid_size[1] * tile_size[1]))

    # Iterate over each tile
    for i, tile in enumerate(tiles):
        # Define the x and y cordinated for the tile
        x = (i // grid_size[1]) * tile_size[0]
        y = (i % grid_size[1]) * tile_size[1]
        # Paste the tile on the right place in the output image
        merged_image.paste(tile, (x, y))
    
    # Saves image to the output_path
    merged_image.save(output_path)
    print("Image saved to output path!")
