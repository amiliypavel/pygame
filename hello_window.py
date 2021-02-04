import sys
import os
import pygame as pg
from time import sleep


class Map(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((1000, 700), pg.SRCALPHA)
        self.image.fill('white')
        self.map_img = load_image('map.png')
        self.map_img.set_alpha(150)
        self.image.blit(self.map_img, (0, 0))
        self.rect = self.image.get_rect()


class SquareButton(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color='black', text='', font_size=30, font_color='white',
                 border=None, border_color='black'):
        super().__init__()
        self.x, self.y, self.width, self.height, self.color, self.text = x, y, w, h, color, text
        self.border_size, self.border_color, self.font_size = border, border_color, font_size
        self.font_color = font_color
        self.image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        if border is not None:
            pg.draw.rect(self.image, self.border_color, (0, 0, self.width, self.height),
                         self.border_size)
        self.button_font = pg.font.Font(None, self.font_size)
        self.button_text = self.button_font.render(self.text, True, self.font_color)
        self.text_x = self.width // 2 - self.button_text.get_width() // 2
        self.text_y = self.height // 2 - self.button_text.get_height() // 2
        self.image.blit(self.button_text, (self.text_x, self.text_y))
    
    def pressed(self, pos):
        return True if self.rect.collidepoint(pos) else False


class CheckBox(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color='black', color_check='white', checked=True, border=None,
                 border_color='black'):
        super().__init__()
        self.x, self.y, self.width, self.height, self.color = x, y, w, h, color
        self.checked, self.border_size, self.border_color = checked, border, border_color
        self.color_check = color_check
        self.image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        if self.border_size is not None:
            pg.draw.rect(self.image, self.border_color, (0, 0, self.width, self.height),
                         self.border_size)
        if self.checked:
            pg.draw.line(self.image, self.color_check, (0, 0), (self.width // 2, self.height), 5)
            pg.draw.line(self.image, self.color_check, (self.width // 2, self.height),
                         (self.width, 0), 5)
    
    def pressed(self, pos):
        return True if self.rect.collidepoint(pos) else False
    
    def change(self):
        if self.checked:
            self.checked = False
            self.image.fill(self.color)
        else:
            self.checked = True
            pg.draw.line(self.image, self.color_check, (0, 0), (self.width // 2, self.height), 5)
            pg.draw.line(self.image, self.color_check, (self.width // 2, self.height),
                         (self.width, 0), 5)
        if self.border_size is not None:
            pg.draw.rect(self.image, self.border_color, (0, 0, self.width, self.height),
                         self.border_size)


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.tile_type = tile_type
        self.image = TILES[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_SIZE * pos_x, TILE_SIZE * pos_y)


class Board(pg.sprite.Sprite):
    def __init__(self, board_images, sprites):
        self.width = len(board_images) * TILE_SIZE
        self.height = len(board_images[0]) * TILE_SIZE
        self.left = WIDTH // 2 - self.width // 2
        self.top = HEIGHT // 2 - self.height // 2
        for tiles in board_images:
            for tile in tiles:
                tile.rect.x += self.left
                tile.rect.y += self.top
        for sprite in sprites:
            sprite.rect.x = self.left + sprite.x * TILE_SIZE
            sprite.rect.y = self.top + sprite.y * TILE_SIZE
        self.tiles = pg.sprite.Group(*board_images)
        self.sprites = pg.sprite.Group(*sprites)
        self.board_images = board_images
    
    def render(self, surf):
        self.tiles.draw(surf)
        self.sprites.draw(surf)
    
    def move(self, speedx, speedy):
        if speedx > 0 and speedx > -self.left:
            speedx = -self.left
        elif speedx < 0 and -speedx > self.width - (-self.left + WIDTH):
            speedx = self.width - (-self.left + WIDTH)
        if speedy > 0 and speedy > -self.top:
            speedy = -self.top
        elif speedy < 0 and -speedy > self.height - (-self.top + HEIGHT):
            speedy = self.height - (-self.top + HEIGHT)        
        for tile in self.tiles.sprites():
            tile.rect = tile.rect.move(speedx, speedy)
        for sprite in self.sprites.sprites():
            sprite.rect = sprite.rect.move(speedx, speedy)
        self.left += speedx
        self.top += speedy
    
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
        self.image = pg.Surface((1000, 250), pg.SRCALPHA)


class Character(pg.sprite.Sprite):
    def __init__(self, image_on_board, image_for_message, cell_x, cell_y, anim_walk=[],
                 anim_atack=[]):
        super().__init__()
        self.image, self.image_for_message = image_on_board, image_for_message
        self.rect = self.image.get_rect()
        self.x, self.y = cell_x, cell_y
    
    def replace(self, x, y):
        self.x, self.y = x, y
    
    def rotate(self):
        self.image = pg.transform.flip(self.image, True, False)


def draw_text(surf, text, x, y, font_size=30, font_color='white'):
    font = pg.font.Font(None, font_size)
    text = font.render(text, True, font_color)
    surf.blit(text, (x, y))

def draw_text_center(surf, text, centerx, centery, font_size=30, font_color='white'):
    font = pg.font.Font(None, font_size)
    text = font.render(text, True, font_color)
    text_x, text_y = centerx - text.get_width() // 2, centery - text.get_height() // 2
    surf.blit(text, (text_x, text_y))

def start_game():
    map_spr = Map()
    btn_play = SquareButton(*START_BUTTON_PLAY_SETTINGS)
    btn_settings = SquareButton(*START_BUTTON_SET_SETTINGS)
    btn_we = SquareButton(*START_BUTTON_WE_SETTINGS)
    start_group.add(map_spr, btn_play, btn_settings, btn_we)
    running_hello_window = True
    
    while running_hello_window:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.pressed(event.pos):
                    running_hello_window = False
                elif btn_we.pressed(event.pos):
                    draw_about_us()
                elif btn_settings.pressed(event.pos):
                    draw_settings()
        start_group.draw(screen)
        draw_text_center(screen, 'Освобождение', WIDTH // 2, 50, font_size=100, font_color='#990000')
        pg.display.flip()
    start()

def draw_about_us():
    about_us_img = pg.Surface(ABOUT_US_WINDOW_SIZE)
    about_us_img.fill('green')
    running_about_us_window = True
    btn_close = SquareButton(*ABOUT_US_BUTTON_CLOSE_SETTINGS)
    about_us_group.add(btn_close)
    while running_about_us_window:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.MOUSEBUTTONDOWN:
                if btn_close.pressed((event.pos[0] - (WIDTH // 2 - ABOUT_US_WINDOW_SIZE[0] // 2),
                                      event.pos[1] - (HEIGHT // 2 - ABOUT_US_WINDOW_SIZE[1] // 2))):
                    running_about_us_window = False
        about_us_group.draw(about_us_img)
        screen.blit(about_us_img, (WIDTH // 2 - ABOUT_US_WINDOW_SIZE[0] // 2,
                                   HEIGHT // 2 - ABOUT_US_WINDOW_SIZE[1] // 2))
        for line in ABOUT_US_TEXT:
            draw_text_center(about_us_img, line, ABOUT_US_WINDOW_SIZE[0] // 2,
                             ABOUT_US_TEXT.index(line) * 40 + 150, 40, 'blue')
        pg.display.flip()

def draw_settings():
    global is_sound, is_music
    settings_img = pg.Surface(SETTINGS_WINDOW_SIZE)
    settings_img.fill('green')
    btn_close = SquareButton(*SETTINGS_BUTTON_CLOSE_SETTINGS)
    if is_sound:
        check_sound = CheckBox(*SETTINGS_CHECKBOX_SOUND_T_SETTINGS)
    else:
        check_sound = CheckBox(*SETTINGS_CHECKBOX_SOUND_F_SETTINGS)
    if is_music:
        check_music = CheckBox(*SETTINGS_CHECKBOX_MUSIC_T_SETTINGS)
    else:
        check_music = CheckBox(*SETTINGS_CHECKBOX_MUSIC_F_SETTINGS)
    settings_group.add(check_sound, check_music, btn_close)
    running_settings_window = True
    while running_settings_window:
        for event in pg.event.get():
            try:
                pos_settings_window = (event.pos[0] - (WIDTH // 2 - SETTINGS_WINDOW_SIZE[0] // 2),
                                       event.pos[1] - (HEIGHT // 2 - SETTINGS_WINDOW_SIZE[1] // 2))
            except:
                if event.type == pg.QUIT:
                    terminate()                
                continue
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if btn_close.pressed(pos_settings_window):
                    if check_sound.checked:
                        is_sound = True
                    else:
                        is_sound = False
                    if check_music.checked:
                        is_music = True
                    else:
                        is_music = False
                    running_settings_window = False
                elif check_sound.pressed(pos_settings_window):
                    check_sound.change()
                elif check_music.pressed(pos_settings_window):
                    check_music.change()
        settings_group.draw(settings_img)
        screen.blit(settings_img, (WIDTH // 2 - SETTINGS_WINDOW_SIZE[0] // 2,
                                   HEIGHT // 2 - SETTINGS_WINDOW_SIZE[1] // 2))
        draw_text(settings_img, 'Звук', 50, 100, 60, 'blue')
        draw_text(settings_img, 'Музыка', 50, 200, 60, 'blue')
        pg.display.flip()

def terminate():# Прекратить работу программы
    os.remove('settings.txt')
    with open('settings.txt', 'w', encoding='utf-8') as set_file:
        print(f'sound-{is_sound}', file=set_file)
        print(f'music-{is_music}', file=set_file)
    pg.quit()
    sys.exit()

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

def generate_level(level_file):
    tiles = []
    with open(level_file, encoding='utf-8') as level_read:
        level = level_read.readlines()
        for y in range(len(level)):
            tiles.append([])
            for x in range(len(level[y])):
                if level[y][x] == '-':
                    tiles[y].append(Tile('grass', x, y))
                if level[y][x] == 'm':
                    tiles[y].append(Tile('mountain', x, y))
                if level[y][x] == 'r':
                    tiles[y].append(Tile('road', x, y))
                if level[y][x] == 's':
                    tiles[y].append(Tile('straightness', x, y))
                if level[y][x] == 'c':
                    tiles[y].append(Tile('castle', x, y))
    return tiles

def show_message(char, text, field=None):
    while field and not (0 <= char.rect.x <= WIDTH or 0 <= char.rect.y <= HEIGHT):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
        if char.rect.x < 0:
            field.move(3, 0)
        if char.rect.x >= WIDTH:
            field.move(-3, 0)
        if char.rect.y < 0:
            field.move(0, 3)
        if char.rect.y >= HEIGHT:
            field.move(0, -3)
        field.render(screen)
        pg.display.flip()
        clock.tick(FPS)
    message_img = pg.Surface((WIDTH, 250))
    message_img.fill(pg.Color((80, 80, 80)))
    message_img.blit(char.image_for_message, (0, 0))
    font = pg.font.Font(None, 35)
    for line in text:
        line_text = font.render(line, True, (255, 255, 255))
        text_x = 250 + MESSAGE_LEFT
        text_y = MESSAGE_TOP + (line_text.get_height() + MESSAGE_PAD) * text.index(line)
        message_img.blit(line_text, (text_x, text_y))
    screen.blit(message_img, (0, HEIGHT - 250))
    pg.display.flip()
    running_message = True
    while running_message:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                running_message = False

def start():
    start_dialog()
    fight_ork()

def start_dialog():
    global knight, mage
    knight = Character(load_image('knight.png'), load_image('knight_message.png'), 3, 2,
                       [load_image('knight_anim_step1.png'), load_image('knight_anim_step2.png')])
    mage = Character(load_image('mage.png'), load_image('mage_message.png'), 1, 2)
    mage.rotate()
    screen.fill('black')
    field = Board(generate_level('start_dialog_map.txt'), [knight, mage])
    field.render(screen)
    pg.display.flip()
    show_message(mage, ['Здравствуй, рыцарь!'])
    show_message(mage, ['Я призвал тебя служить своему королевству.'])
    show_message(knight, ['Я готов.'])
    show_message(mage, ['Тебе нужно найти один предмет.',
                        'Это древний манускрипт, давно потерянный магами.',
                        'Сейчас он хранится в хранилише тролля по имени Сургул.',
                        'Глупая тварь не понимает, для чего он предназначен,',
                        'но и отдавать с миром ничего не собирается.'])
    show_message(knight, ['Как его найти?'])
    show_message(mage, ['Тролль засел в северной пещере напротив Большого леса.',
                        'Чтобы туда добраться, нужно пересечь земли орков.',
                        'Поэтому я дам тебе огненный меч, который ты сможешь',
                        'оставить себе как награду.'])
    knight.image_for_message = load_image('knight_fire_message.png')
    show_message(knight, ['Оооо...'])
    show_message(knight, ['Я благодарю тебя. А теперь мне пора в путь.'])

def fight_ork():
    knight.replace(0, 14)
    ork1 = Character(load_image('ork.png'), load_image('ork_message.png'), 0, 2)
    ork2 = Character(load_image('ork.png'), load_image('ork_message.png'), 2, 3)
    ork3 = Character(load_image('ork.png'), load_image('ork_message.png'), 4, 4)
    ork4 = Character(load_image('ork.png'), load_image('ork_message.png'), 5, 4)
    ork5 = Character(load_image('ork.png'), load_image('ork_message.png'), 6, 4)
    ork6 = Character(load_image('ork.png'), load_image('ork_message.png'), 8, 4)
    ork7 = Character(load_image('ork.png'), load_image('ork_message.png'), 9, 4)
    ork8 = Character(load_image('ork.png'), load_image('ork_message.png'), 10, 4)
    ork9 = Character(load_image('ork.png'), load_image('ork_message.png'), 12, 3)
    ork10 = Character(load_image('ork.png'), load_image('ork_message.png'), 14, 2)
    ork_leader = Character(load_image('ork_leader.png'), load_image('ork_leader_message.png'), 7, 2)
    field = Board(generate_level('fight_ork_map.txt'), [knight, ork1, ork2, ork3, ork4, ork5, ork6,
                                                        ork7, ork8, ork9, ork10, ork_leader])
    running_fight_ork = True
    rotation = 0
    field.render(screen)
    pg.display.flip()    
    show_message(knight, ['Итак, я прошёл полпути. Маг был прав. Здесь засели орки.',
                          'Но это не их крепости, их построили люди. Надо выгнать',
                          'этих подлых существ!'], field)
    show_message(ork3, ['Шеф, к нам приближается какой-то человек'], field)
    show_message(ork_leader, ['Гром и молнии! У этого человека огненный меч. Я слышал', 
                              'о нём. Будьте осторожны, воины! Мы можем одолеть его',
                              'только числом.'], field)
    while running_fight_ork:
        screen.fill('black')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and event.pos == ():
                pass
        if pg.mouse.get_focused():
            if 0 <= pg.mouse.get_pos()[0] <= SCROLLING_PADDING:
                field.move(SPEED_SCROLLING, 0)
            if WIDTH - SCROLLING_PADDING <= pg.mouse.get_pos()[0] < WIDTH:
                field.move(-SPEED_SCROLLING, 0)
            if 0 <= pg.mouse.get_pos()[1] <= SCROLLING_PADDING:
                field.move(0, SPEED_SCROLLING)
            if HEIGHT - SCROLLING_PADDING <= pg.mouse.get_pos()[1] < HEIGHT:
                field.move(0, -SPEED_SCROLLING)
        field.render(screen)
        pg.display.flip()
        clock.tick(FPS)


SIZE = WIDTH, HEIGHT = 1000, 700

pg.init()
screen = pg.display.set_mode(SIZE)

FPS = 60
FILE_SETTINGS = [line.strip() for line in open('settings.txt', encoding='utf-8').readlines()]
START_BUTTON_PLAY_SETTINGS = (WIDTH // 2 - 100, 300, 200, 50, pg.Color(0, 51, 0, 200), 'Играть', 35,
                              pg.Color(255, 219, 77))
START_BUTTON_SET_SETTINGS = (WIDTH // 2 - 100, 200, 200, 50, pg.Color(0, 51, 0, 200), 'Настройки',
                             35, pg.Color(255, 219, 77))
START_BUTTON_WE_SETTINGS = (WIDTH // 2 - 100, 400, 200, 50, pg.Color(0, 51, 0, 200), 'О нас', 35,
                            pg.Color(255, 219, 77))
ABOUT_US_WINDOW_SIZE = 700, 400
ABOUT_US_BUTTON_CLOSE_SETTINGS = (ABOUT_US_WINDOW_SIZE[0] - 100, 0, 100, 100,
                                  pg.Color(102, 255, 255), 'X', 80, 'red')
ABOUT_US_TEXT = ['Я - начинающий разработчик', 'Если вы благодарны мне за создание этой игры',
                 'То, пожалуйста, положите вашу благодарность', 'на телефон 8-910-917-47-97']
SETTINGS_WINDOW_SIZE = 700, 400
SETTINGS_BUTTON_CLOSE_SETTINGS = ABOUT_US_BUTTON_CLOSE_SETTINGS
SETTINGS_CHECKBOX_SOUND_T_SETTINGS = [500, 100, 50, 50, 'white', 'black', True, 3, 'black']
SETTINGS_CHECKBOX_SOUND_F_SETTINGS = [500, 100, 50, 50, 'white', 'black', False, 3, 'black']
SETTINGS_CHECKBOX_MUSIC_T_SETTINGS = [500, 200, 50, 50, 'white', 'black', True, 3, 'black']
SETTINGS_CHECKBOX_MUSIC_F_SETTINGS = [500, 200, 50, 50, 'white', 'black', False, 3, 'black']
TILES = {'grass': load_image('grass.png'), 'mountain': load_image('mountain.png'),
         'road': load_image('road.png'), 'straightness': load_image('straightness.png'),
         'castle': load_image('castle.png')}
TILE_SIZE = 100
MESSAGE_TOP = 50
MESSAGE_LEFT = 20
MESSAGE_PAD = 10
SPEED_SCROLLING = 20
SCROLLING_PADDING = 30

start_group = pg.sprite.Group()
about_us_group = pg.sprite.Group()
settings_group = pg.sprite.Group()
clock = pg.time.Clock()
if FILE_SETTINGS[0].endswith('True'):
    is_sound = True
else:
    is_sound = False
if FILE_SETTINGS[1].endswith('True'):
    is_music = True
else:
    is_music = False

if __name__ == '__main__':
    start_game()
