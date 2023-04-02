from os import walk
from csv import reader
import pygame as pg


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def import_csv_layout(path):
    terrain_map = []

    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphics(path):
    surface = pg.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / 16)
    tile_num_y = int(surface.get_size()[1] / 16)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * 16
            y = row * 16
            new_surf = pg.Surface((16, 16), flags = pg.SRCALPHA)
            new_surf.blit(surface, (0, 0), pg.Rect(x, y, 16, 16))
            cut_tiles.append(new_surf)

    return cut_tiles