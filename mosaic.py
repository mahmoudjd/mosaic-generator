import os
import numpy as np
import glob as glob
from PIL import Image
from scipy.spatial.distance import cdist


class Counter:
    def __init__(self, total):
        """
        @param total - The total number of items to be processed.
        """
        self.total = total
        self.counter = 0

    def increment(self):
        """
        It takes a counter and a total, and prints a percentage of the counter to the total
        """
        self.counter += 1
        actual_value = (self.counter * 100) / self.total
        print('[...] processing: {:02.0f}%'.format(actual_value), flush=True, end='\r')


def import_all_tiles(paths):
    """
    Import all tiles as images.
    """
    tiles = [Image.open(path) for path in paths]
    print(f'[+] All tiles have been successfully imported ({len(tiles)} tiles).')
    return tiles

def resize_tiles(tiles, size):
    """
    Resize all tiles to a given size.
    """
    resized_tiles = [tile.resize(size) for tile in tiles]
    print(f'[+] All tiles have been resized to {size[0]}x{size[1]}.')
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
        Create a mosaic image from the target image using the tiles.
        """
        self.create(self.target_img, self.output_img, self.tiles, self.x, self.y)

    def create(self, target_image, output_image, tiles_dir, x, y):
        """
        Create a mosaic of the target image using the tiles.
        """
        print(f'[!] Creating Mosaic like {target_image}....')
        tiles_directory = os.path.join(tiles_dir, '*')
        tiles_size = (x, y)
        tiles_paths = glob.glob(tiles_directory)
        tiles_before = import_all_tiles(tiles_paths)
        tiles = resize_tiles(tiles_before, tiles_size)
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
        Return the size of the tiles.
        """
        return (x, y)

    @staticmethod
    def get_paths(tiles):
        """
        Return a list of paths to all the tiles in the directory.
        """
        print(f'[!] Reading tiles from directory {tiles[0:-2]}...')
        tile_paths = glob.glob(tiles)
        print(f'[+] All paths of tiles have been successfully readied.')
        return tile_paths

    @staticmethod
    def find_avg_colors(imgs):
        """
        Return a list of average colors for each image.
        """
        print('[!] Searching average colors...')
        # avg_colors = [np.mean(np.asarray(img), axis=(0, 1)) for img in imgs]
        avg_colors = []
        percent_counter = Counter(len(imgs))
        for img in imgs:
            avg_colors.append(np.mean(np.asarray(img), axis=(0,1)))

            percent_counter.increment()
        print('[+] Processed colors.')
        return avg_colors

    @staticmethod
    def resize_target_img(image, x, y):
        """
        Resize the target image.
        """
        print('[!] Processing target image...')
        img = Image.open(image)
        img_x, img_y = img.size
        width = int(np.round(img_x / x))
        height = int(np.round(img_y / y))
        resized_img = img.resize((width, height))
        print('[+] Target image has been processed.')
        return resized_img

    @staticmethod
    def find_nearst_tile(image, avg_colors):
        print('[!] Searching the nearest tiles...')
        w, h = image.size
        map_nearest = np.zeros((w, h), dtype=np.uint32)
        percent_counter = Counter(w * h)

        for i in range(w):
            for j in range(h):
                percent_counter.increment()
                pixel = image.getpixel((i, j))
                distances = cdist([pixel], avg_colors, 'euclidean')
                nearest_tile_index = np.argmin(distances)
                map_nearest[i, j] = nearest_tile_index

        print('[+] The nearest tiles have been successfully found.')
        return map_nearest

    @staticmethod
    def draw_tiles(w1, h1, image, w2, h2, tiles, nearst_tiles):
        """
        Draw all tiles.
        """
        print('[!] Drawing all tiles...')
        percent_counter = Counter(w1 * h1)
        for i in range(w1):
            for j in range(h1):
                percent_counter.increment()
                x = i * w2
                y = j * h2
                index = nearst_tiles[i, j]
                img = tiles[index]
                image.paste(img, (x, y))
        print('[+] Drawing has been successfully finished.')
        return image

    @staticmethod
    def save_mosaic(image, output_name):
        """
        Save the photo mosaic.
        """
        image.save(output_name)
        print(f'[+] Photo mosaic has been successfully saved to "{output_name}".')

