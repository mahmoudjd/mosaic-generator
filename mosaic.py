import random

import numpy as np
import glob
from PIL import Image
from scipy import spatial
from counter import Counter


# > It imports all tiles from a list of paths, resizes them to a given size and returns a list of
# resized tiles
class TileImg:
    @classmethod
    def import_all_tiles(cls, paths):
        """
        > It takes a list of paths to images, opens each image, and returns a list of the opened images
        @param cls - The class that the method is being called on.
        @param paths - A list of paths to the tiles.
        @returns A list of all the tiles as images.
        """
        tiles = []
        print('[!] Importing all tiles as Images...')
        percent_counter = Counter(len(paths))
        for path in paths:
            tile = Image.open(path)
            tiles.append(tile)
            percent_counter.increment()

        print(f'[+] All tiles have been successfully imported ({len(tiles)} tiles).')
        return tiles

    @classmethod
    def resize_tiles(cls, tiles, size):
        """
        > Resize all tiles to a given size
        @param cls - The class that the method belongs to.
        @param tiles - A list of PIL.Image objects.
        @param size - The size of the tiles.
        @returns A list of resized tiles.
        """
        resized_tiles = []
        print('[!] Resizing all tiles ...')
        percent_counter = Counter(len(tiles))
        for tile in tiles:
            tile = tile.resize(size)
            resized_tiles.append(tile)
            percent_counter.increment()
        print(f'[+] All tiles have been to {size[0]}x{size[1]} resized.')
        return resized_tiles


class MosaicGenerator:
    def __init__(self, target_img, output_img, tiles, x, y):
        self.target_img = target_img
        self.output_img = output_img
        self.tiles = tiles
        self.x = x
        self.y = y

    def create_Mosaic(self):
        """
        It creates a mosaic image from the target image using the tiles.
        """
        self.create(self.target_img, self.output_img, self.tiles, self.x, self.y)

    def create(self, target_image, output_image, tiles_dir, x, y):
        """
        > The function takes in the target image, the output image, the directory of the tiles, the x and y
        size of the tiles, and creates a mosaic of the target image using the tiles
        @param target_image - The image you want to create a mosaic of.
        @param output_image - The name of the output image.
        @param tiles_dir - the directory where the tiles are stored
        @param x - the number of tiles in the x direction
        @param y - the number of tiles in the y direction
        """
        print(f'[!] create Mosaic like {target_image}....')
        tiles_directory = tiles_dir + '/*'
        tiles_size = self.get_size(x, y)
        tiles_paths = self.get_paths(tiles_directory)
        tiles_before = TileImg.import_all_tiles(tiles_paths)
        tiles = TileImg.resize_tiles(tiles_before, tiles_size)
        avg_colors = self.find_avg_colors(tiles)
        resized_photo = self.resize_target_img(target_image, tiles_size[0], tiles_size[1])
        width, height = resized_photo.size
        nearst_tiles = self.find_nearst_tile(resized_photo, avg_colors)
        main_img = Image.open(target_image)
        output = Image.new('RGB', main_img.size)
        image = self.draw_tiles(width, height, output, tiles_size[0], tiles_size[1], tiles, nearst_tiles)
        self.save_mosaic(image, output_image)

    @staticmethod
    def get_size(x, y):
        """
        It returns the size of the tiles.
        @param x - The width of the tile in pixels.
        @param y - The y coordinate of the tile.
        @returns the tiles_size variable.
        """
        tiles_size = (x, y)
        return tiles_size

    @staticmethod
    def get_paths(tiles):
        """
        It takes a string of a directory path, and returns a list of all the paths of the tiles in that
        directory.
        @param tiles - The directory of the tiles you want to stitch.
        @returns A list of paths to all the tiles in the directory.
        """
        tile_paths = []
        print(f'[!] Reading tiles from directory {tiles[0:-2]}...')
        for path in glob.glob(tiles):
            tile_paths.append(path)
        print(f'[+] All paths of tiles have been successfully readied.')
        return tile_paths

    @staticmethod
    def find_avg_colors(imgs):
        """
        It takes a list of images and returns a list of average colors for each image
        @param imgs - a list of images
        @returns A list of average colors for each image.
        """
        avg_colors = []
        print('[!] Searching average colors...')
        percent_counter = Counter(len(imgs))
        for img in imgs:
            colors = np.asarray(img)  # make three-dimensional numpy arrays from image ([[r0,g0,b0],[r1,g1,b1], ...])
            avg_color_row = np.mean(colors, axis=0)  # calculate average color per row
            avg_color = np.mean(avg_color_row, axis=0)  # calculate average color for all rows
            avg_colors.append(avg_color)
            percent_counter.increment()
        print('[+] Processed colors.')
        return avg_colors

    @staticmethod
    def resize_target_img(image, x, y):
        """
        > This function takes in an image, and the number of pixels you want to divide the image into,
        and returns a resized image
        @param image - the path to the image you want to resize
        @param x - The number of pixels in the x-direction of the target image.
        @param y - The number of rows in the target image.
        @returns The resized image.
        """
        print('[!] Processing target image...')
        img = Image.open(image)
        img_x = img.size[0]
        img_y = img.size[1]
        width = int(np.round(img_x / x))
        height = int(np.round(img_y / y))
        resized_img = img.resize((width, height))
        print('[+] Target image has been processed.')
        return resized_img

    @staticmethod
    def find_nearst_tile(image, avg_color):
        """
        For each pixel in the image, find the nearest 5 tiles, then randomly choose one of them to be the
        nearest tile for that pixel
        @param image - The image to be pixelated.
        @param avg_color - a list of RGB tuples, each representing the average color of a tile.
        @returns a 2D array of the same size as the image,
                where each element is the index of the nearest tile.
        """
        print('[!] Searching the nearst tiles...')
        w = image.size[0]
        h = image.size[1]
        map_nearst = np.zeros((w, h), dtype=np.uint32)
        tree = spatial.KDTree(avg_color)
        percent_counter = Counter(w * h)
        for i in range(w):
            for j in range(h):
                pixel = image.getpixel((i, j))
                nearst_tiles = tree.query(pixel, k=5)
                # Query the kd-tree to find nearest neighbors for pixel (i,j).
                rnd = random.randint(0, 4)
                map_nearst[i, j] = nearst_tiles[1][rnd]
                percent_counter.increment()
                # You may notice the ‘K = 5’ argument
                # for the KDTree query… I found that the final image had a lot of repetitions,
                # because pixels close to each other shared a very similar value.
                # So I asked the tree to return the nearest 5 values for each pixel,
                # then used a random int from 0 to 4 to chose which one would make the cut.
                # Now there are much fewer repeats.
        print('[+] The nearst tiles have been successfully founded.')
        return map_nearst

    @staticmethod
    def draw_tiles(w1, h1, image, w2, h2, tiles, nearst_tiles):
        """
        It takes a big image and a bunch of small images, and pastes the small images into the big image
        @param w1 - width of the image
        @param h1 - height of the image
        @param image - the image to be processed
        @param w2 - width of the tile
        @param h2 - height of the tile
        @param tiles - a list of images
        @param nearst_tiles - a 2D array of the nearest tile index for each pixel in the original image.
        @returns The image is being returned.
        """
        print('[!] Drawing all tiles...')
        percent_counter = Counter(w1 * h1)
        for i in range(w1):
            for j in range(h1):
                x = i * w2
                y = j * h2
                index = nearst_tiles[i, j]
                img = tiles[index]
                image.paste(img, (x, y))
                percent_counter.increment()
        print('[+] Drawing has been successfully finished.')
        return image

    @staticmethod
    def save_mosaic(image, output_name):
        """
        It takes in an image and an output name, and saves the image to the output name.
        @param image - the image to be converted to a mosaic
        @param output_name - The name of the output file.
        """
        image.save(output_name)
        print(f'[+] Photo mosaic has been successfully saved to "{output_name}".')
