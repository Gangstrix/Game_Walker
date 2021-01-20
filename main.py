import pygame
import sys
import os


# Функция для загрузки изображения
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


# Инициализация PyGame
pygame.init()
pygame.display.set_caption('SAVE THE YANDEX')
pygame.display.set_icon(pygame.image.load("data/logo.ico"))
screen_size = (1300, 750)
screen = pygame.display.set_mode(screen_size)
FPS = 60

tile_images = {
    'wall': load_image('google.png'),
    'empty': load_image('grass.png'),
    'wall2': load_image('box.png'),
    'empty2': load_image('block.png')
}
player_image = load_image('gangstrix.png')
tile_enemies = {
    'dino': load_image('dino.png'),
    'google': load_image('villain.png')
}
exit_game = load_image('exit.png')

tile_width = tile_height = 50


# Аварийный выход из игры
def terminate():
    pygame.quit()
    sys.exit()


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


# Загрузка уровня
def load_level(filename):
    global screen

    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    with open(filename, 'r') as mapFile:
        max_height = len([line.strip() for line in mapFile])
    max_width = max(map(len, level_map))
    screen_size = (max_width * tile_width, max_height * tile_height)
    screen = pygame.display.set_mode(screen_size)
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


# Отрисовка уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                exit_of_game = Exit(x, y)
    # вернем игрока, размер поля в клетках, а так же переход на новый уровень
    return new_player, x, y, exit_of_game


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 1300, 750)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group)
        self.image = exit_game
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Enemies(pygame.sprite.Sprite):
    pass


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
exit_group = SpriteGroup()


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] == ".":
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map[y + 1][x] == ".":
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] == ".":
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and level_map[y][x + 1] == ".":
            hero.move(x + 1, y)


current_level = 1
quantity_levels = 6
start_screen()
level_map = load_level("level_" + str(current_level) + ".txt")
hero, max_x, max_y, exit_game = generate_level(level_map)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, "up")
            elif event.key == pygame.K_DOWN:
                move(hero, "down")
            elif event.key == pygame.K_LEFT:
                move(hero, "left")
            elif event.key == pygame.K_RIGHT:
                move(hero, "right")
            if not pygame.sprite.collide_rect(hero, exit_game):
                screen.fill(pygame.Color("black"))
                sprite_group.draw(screen)
                exit_group.draw(screen)
                hero_group.draw(screen)
            else:
                current_level += 1
                if current_level != quantity_levels:
                    level_map = load_level("level_" + str(current_level) + ".txt")
                    hero, max_x, max_y, exit_game = generate_level(level_map)
                sprite_group.empty()
                exit_group.empty()
                hero_group.empty()
                break

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
