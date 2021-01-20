import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)  # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
pygame.display.set_caption('SAVE THE YANDEX')
pygame.display.set_icon(pygame.image.load("data/logo.ico"))
screen_size = (1300, 750)
screen = pygame.display.set_mode(screen_size)
FPS = 60


# Отрисовка начальной заставки игры
def fon():
    intro_text = ["Правила игры:",
                  "На планету Яндекса напал Гугл!!!",
                  "Ваша цель - пробраться через базы злодея,",
                  "найти священный компьютер Яндекса и запустить его,",
                  "чтобы вернуть прежний вид нашей земле."]

    fon = pygame.transform.scale(load_image('fon 2.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font_size_rules = 20
    font_rules = pygame.font.Font("data/18965.ttf", font_size_rules)
    text_coord = 550
    for line in intro_text:
        string_rendered = font_rules.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 510
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    font_size_NameOfGame = 50
    font_NameOfGame = pygame.font.Font("data/18965.ttf", font_size_NameOfGame)
    nameOfGame = font_NameOfGame.render("SAVE THE YANDEX", 1, pygame.Color('white'))
    screen.blit(nameOfGame, (370, 100))


# Начальная заставка игры
def start_screen():
    fon()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(name):
    fullname = "data/" + name
    with open(fullname, 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            level_map.append(line)
    return level_map


def draw_level(level_map):
    new_player, x, y = None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                Tile('ice.png', x, y)
            elif level_map[y][x] == '#':
                Tile('box.png', x, y)
            elif level_map[y][x] == '@':
                Tile('ice.png', x, y)
                new_player = Player(x, y)
            # цветок будет обозначен на карте уровня знаком "&"
            elif level_map[y][x] == '&':
                Tile('ice.png', x, y)
                flower = Flower(x, y)
    return new_player, x, y, flower


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(tile_type)
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)

        self.add(tiles_group, all_sprites)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('snowman.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(player_group, all_sprites)

    def move_up(self):
        self.rect = self.rect.move(0, -50)

    def move_down(self):
        self.rect = self.rect.move(0, +50)

    def move_left(self):
        self.rect = self.rect.move(-50, 0)

    def move_right(self):
        self.rect = self.rect.move(+50, 0)

    # класс для задания цветка


class Flower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('flower.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(flower_group, all_sprites)


# описание загрузки первого уровня
def level_1():
    player, level_x, level_y, flower = draw_level(load_level("level_1.txt"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()

            if event.type == pygame.QUIT:
                terminate()

        if not pygame.sprite.collide_rect(player, flower):
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            flower_group.draw(screen)
        else:
            all_sprites.empty()
            player_group.empty()
            tiles_group.empty()
            flower_group.empty()
            return

        pygame.display.flip()
        clock.tick(fps)


# описание загрузки второго уровня после нахождения цветка
def level_2():
    player, level_x, level_y, flower = draw_level(load_level("level_2.txt"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()

            if event.type == pygame.QUIT:
                terminate()

        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        flower_group.draw(screen)

        pygame.display.flip()
        clock.tick(fps)


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
flower_group = pygame.sprite.Group()

# последовательный вызов первого уровня,
# по завершении которого вызовется второй уровень
level_1()
level_2()

terminate()
