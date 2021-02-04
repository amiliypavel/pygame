import pygame as pg
import os
from functions import *


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.tile_type = tile_type
        self.image = TILES[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_SIZE * pos_x, TILE_SIZE * pos_y)


class Board(pg.sprite.Sprite):
    def __init__(self, board_images):
        self.width = len(board_images)
        self.height = len(board_images[0])
        self.tiles = pg.sprite.Group(*board_images)
        self.left = WIDTH // 2 - self.width // 2
        self.top = HEIGHT // 2 - self.height // 2
    
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    
    def render(self, surf):
        self.tiles.draw(surf)
        #for i in range(self.width):
            #for j in range(self.height):
                #if level[y][x] == '-':
                    #Tile('grass', x, y)
                #screen.blit(self.images[i][j], (self.left + i * self.cell_cize,
                                                #self.top + j * self.cell_size))
    
    def get_cell(self, mouse_pos):
        if mouse_pos[0] <= self.left or mouse_pos[0] > self.left + self.width * self.cell_size or mouse_pos[1] <= self.top or mouse_pos[1] > self.top + self.height * self.cell_size:
            return None
        cell_x = (mouse_pos[0] - self.left + self.cell_size - 1) // self.cell_size - 1
        cell_y = (mouse_pos[1] - self.top + self.cell_size - 1) // self.cell_size - 1
        return (cell_x, cell_y)

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Message(pg.sprite.Sprite):
    def __init__(self, sprite, text):
        super().__init__()
        self.sprite, self.text = sprite, text


def generate_level(level_file):
    tiles = []
    with open(level_file, encoding='utf-8') as level_read:
        level = level_read.readlines()
        for y in range(len(level)):
            tiles.append([])
            for x in range(len(level[y])):
                if level[y][x] == '-':
                    tiles[y].append(Tile('grass', x, y))
    return tiles

def start():
    start_dialog()

def start_dialog():
    field = Board(generate_level('start_dialog_map.txt'))
    running_start_dialog = True
    while running_start_dialog:
        field.render(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()

#def terminate():# Прекратить работу программы
    #os.remove('settings.txt')
    #with open('settings.txt', 'w', encoding='utf-8') as set_file:
        #print(f'sound-{is_sound}', file=set_file)
        #print(f'music-{is_music}', file=set_file)
    #pg.quit()
    #sys.exit()

def load_image(name, colorkey=None):# Загрузка изображения
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


SIZE = WIDTH, HEIGHT = 1000, 700

pg.init()
screen = pg.display.set_mode(SIZE)

TILES = {'grass': load_image('grass.png'), 'knight': load_image('knight.png')}
TILE_SIZE = 100

if __name__ == '__main__':
    start()
