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
# Иконка и название окна программы
pygame.display.set_caption('SAVE THE YANDEX')
pygame.display.set_icon(pygame.image.load("data/logo.ico"))
screen_size = (1300, 750)
screen = pygame.display.set_mode(screen_size)
FPS = 60
count_FPS = 1

# Загружаем фоновую музыку
pygame.mixer.music.load('data/water.mp3')
pygame.mixer.music.set_volume(0.5)

# Загружаем все звуки спецэффектов, а также фоновую музыку для уровней
change_person_sound = pygame.mixer.Sound('data/change.wav')
click_of_button = pygame.mixer.Sound('data/button.mp3')
start_music = pygame.mixer.Sound('data/starting.mp3')
late_music = pygame.mixer.Sound('data/dalee.mp3')
fail = pygame.mixer.Sound('data/lose.mp3')
new_lvl = pygame.mixer.Sound('data/new_lvl.mp3')
win = pygame.mixer.Sound('data/win_melody.mp3')

# Загружаем все текстуры тайлов
tile_images = {
    'wall': load_image('google.png'),
    'empty': load_image('grass.png'),
    'wall2': load_image('box.png'),
    'empty2': load_image('block.png'),
    'grass': load_image('big grass.png'),
    'stone': load_image('stone.png'),
    'stone2': load_image('stone2.png'),
    'blood': load_image('blood.png')
}

# Загружаем скины персонажей, за которых будем играть
player_image = {
    'strix': load_image('gangstrix.png'),
    'teach': load_image('teacher.png')
}

# Загружаем скины врагов
tile_enemies = {
    'dino': load_image('dino.png'),
    'google': load_image('villain.png'),
    'bag': load_image('bag.png')
}

# Загружаем объекты перехода на новый уровень
door = {
    'door': load_image('exit.png'),
    'comp': load_image('win.png')
}

# Задаём размер и ширину одного тайла
tile_width = tile_height = 50

hero_name = ''


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


# Экран начальной заставки игры
def start_screen():
    fon()
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# Отрисовка фона выбора персонажа
def change_person_screen():
    fon = pygame.transform.scale(load_image('change.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font_size_change = 50
    font_change = pygame.font.Font("data/18965.ttf", font_size_change)
    change = font_change.render("CHANGE YOUR PERSON", 1, pygame.Color('white'))
    screen.blit(change, (280, 60))


# Экран выбора персонажа
def change_screen():
    change_person_screen()
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(change_person_sound)
    one_pers = Button(250, 70)
    two_pers = Button(250, 70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            one_pers.draw_button(245, 600, 1)
            two_pers.draw_button(825, 600, 2)
        if hero_name:
            change_person_sound.stop()
            break

        clock.tick(FPS)
        pygame.display.flip()


# Функция, реализующая выбор персонажа и загрузку его скина в игру
def set_hero(num):
    global hero_name
    if num == 1:
        player_name = 'strix'
        hero_name = player_name
        return
    else:
        player_name = 'teach'
        hero_name = player_name
        return


# Отрисовка фона проигрыша
def lose_game_screen():
    fon = pygame.transform.scale(load_image('lose_fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font_size_change = 70
    font_change = pygame.font.Font("data/18965.ttf", font_size_change)
    change = font_change.render("YOU LOSE", 1, pygame.Color('white'))
    change2 = font_change.render("press space", 1, pygame.Color('white'))
    screen.blit(change, (450, 300))
    screen.blit(change2, (450, 600))


# Экран проигрыша игры
def lose_game():
    lose_game_screen()
    start_music.stop()
    late_music.stop()
    pygame.mixer.Sound.play(fail)
    fail.set_volume(0.1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # начинаем игру

        clock.tick(FPS)
        pygame.display.flip()


# Отрисовка фона победы
def win_screen():
    fon = pygame.transform.scale(load_image('win_fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font_size_change = 70
    font_change = pygame.font.Font("data/18965.ttf", font_size_change)
    change = font_change.render("WINNER", 1, pygame.Color('white'))
    screen.blit(change, (470, 50))


# Экран победы в игре
def win_game():
    win_screen()
    start_music.stop()
    late_music.stop()
    pygame.mixer.Sound.play(win)
    win.set_volume(0.1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                 event.type == pygame.MOUSEBUTTONDOWN:
                terminate()

        clock.tick(FPS)
        pygame.display.flip()


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
    global hero_name
    evil = []
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'o':
                Tile('empty', x, y)
                Tile('stone', x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Tile('grass', x, y)
            elif level[y][x] == 'x':
                Tile('empty2', x, y)
                Tile('stone2', x, y)
            elif level[y][x] == ':':
                Tile('empty2', x, y)
                Tile('blood', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '^':
                Tile('empty2', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '&':
                Tile('wall2', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(f'{hero_name}', x, y)
            elif level[y][x] == 'А':
                Tile('empty2', x, y)
                new_player = Player(f'{hero_name}', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                exit_of_game = Exit('door', x, y)
            elif level[y][x] == '?':
                Tile('empty2', x, y)
                exit_of_game = Exit('door', x, y)
            elif level[y][x] == '+':
                Tile('empty2', x, y)
                exit_of_game = Exit('comp', x, y)
            elif level[y][x] == '%':
                Tile('empty', x, y)
                evil.append(Enemies('google', x, y))
            elif level[y][x] == '5':
                Tile('empty2', x, y)
                evil.append(Enemies('dino', x, y))
            elif level[y][x] == '~':
                Tile('empty2', x, y)
                evil.append(Enemies('bag', x, y))
    # вернем игрока, размер поля в клетках, врагов, а также переход на новый уровень
    return new_player, x, y, exit_of_game, evil


# Класс кнопки, которая понадобиться нам при выборе персонажа
class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.off_color = pygame.Color("red")
        self.on_color = pygame.Color("white")

    # Функция отрисовки кнопки по заданным координатам
    def draw_button(self, x, y, num):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Если мышка находится в поле действия кнопки, то мы её подсвечиваем белым цветом
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.on_color, (x, y, self.width, self.height))
            # Если произошёл клик по кнопке, то мы выбираем соответствующего персонажа и загружаем в игру
            if click[0] == 1:
                pygame.mixer.Sound.play(click_of_button)
                click_of_button.set_volume(0.7)
                set_hero(num)
        else:
            pygame.draw.rect(screen, self.off_color, (x, y, self.width, self.height))

        # Отрисовка текста в кнопке
        font_size_button = 30
        font_button = pygame.font.Font("data/18965.ttf", font_size_button)
        font = font_button.render("READY", 1, pygame.Color('black'))
        screen.blit(font, (x + 60, y + 23))


# Класс для создания группы спрайтов
class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


# Класс текстур тайлов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, hero_type, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image[hero_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    # Логика передвижения игрока
    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


# Класс выхода
class Exit(pygame.sprite.Sprite):
    def __init__(self, exit_type, pos_x, pos_y):
        super().__init__(exit_group)
        self.image = door[exit_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# Класс врагов
class Enemies(pygame.sprite.Sprite):
    def __init__(self, enemies_type, pos_x, pos_y):
        super().__init__(enemies_group)
        self.image = tile_enemies[enemies_type]
        with open('data/vragi_' + str(current_level) + '_yrovna.txt', 'r') as f:
            lines = list(map(str.strip, f.readlines()))
        for line in lines:
            coord, dvig = line.split(':')
            if str(pos_x) + ',' + str(pos_y) == coord:
                self.dx, self.dy = [int(i) for i in dvig.split(',')]
                break
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    # Логика перемещения врагов
    def move(self):
        x = self.pos[0] + self.dx
        y = self.pos[1] + self.dy
        if x < 0 \
                or y < 0 \
                or level_map[y][x] == "x" \
                or level_map[y][x] == "o" \
                or level_map[y][x] == "#" \
                or level_map[y][x] == "~" \
                or level_map[y][x] == "&":
            self.dx = -self.dx
            self.dy = -self.dy
        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

    # Функция обновления состояния перемещения
    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


# Добавление всех основных параметров, групп спрайтов и переменных
player = None
winner = False
game_over = False
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
enemies_group = SpriteGroup()
exit_group = SpriteGroup()


# Функция перемещения игрока
def move(hero, movement):
    global game_over
    x, y = hero.pos
    # Мы можем входить в объекты, которые обозначаются символами, указанными ниже во всех направлениях
    # (слева, справа, снизу, сверху)
    if movement == "up":
        if y > 0 and level_map[y - 1][x] == "." \
                or level_map[y - 1][x] == "^" \
                or level_map[y - 1][x] == "?" \
                or level_map[y - 1][x] == '!' \
                or level_map[y - 1][x] == "+" \
                or level_map[y - 1][x] == "5" \
                or level_map[y - 1][x] == "А" \
                or level_map[y - 1][x] == "~" \
                or level_map[y - 1][x] == "%" \
                or level_map[y - 1][x] == "@" \
                or level_map[y - 1][x] == ":" \
                or level_map[y - 1][x] == "*":
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map[y + 1][x] == "." \
                or level_map[y + 1][x] == "^" \
                or level_map[y + 1][x] == "?" \
                or level_map[y + 1][x] == "+" \
                or level_map[y + 1][x] == '!' \
                or level_map[y + 1][x] == "5" \
                or level_map[y + 1][x] == "А" \
                or level_map[y + 1][x] == "~" \
                or level_map[y + 1][x] == "%" \
                or level_map[y + 1][x] == "@" \
                or level_map[y + 1][x] == ":" \
                or level_map[y + 1][x] == "*":
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] == "." \
                or level_map[y][x - 1] == "^" \
                or level_map[y][x - 1] == "?" \
                or level_map[y][x - 1] == "!" \
                or level_map[y][x - 1] == "+" \
                or level_map[y][x - 1] == "5" \
                or level_map[y][x - 1] == "А" \
                or level_map[y][x - 1] == "~" \
                or level_map[y][x - 1] == "%" \
                or level_map[y][x - 1] == "@" \
                or level_map[y][x - 1] == ":" \
                or level_map[y][x - 1] == "*":
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and level_map[y][x + 1] == "." \
                or level_map[y][x + 1] == "^" \
                or level_map[y][x + 1] == "?" \
                or level_map[y][x + 1] == "!" \
                or level_map[y][x + 1] == "+" \
                or level_map[y][x + 1] == "5" \
                or level_map[y][x + 1] == "А" \
                or level_map[y][x + 1] == "~" \
                or level_map[y][x + 1] == "%" \
                or level_map[y][x + 1] == "@" \
                or level_map[y][x + 1] == ":" \
                or level_map[y][x + 1] == "*":
            hero.move(x + 1, y)


# Основной цикл игры
current_level = 1
quantity_levels = 6
start_screen()
change_screen()
level_map = load_level("level_" + str(current_level) + ".txt")
hero, max_x, max_y, exit_game, zlo = generate_level(level_map)
pygame.mixer.Sound.play(start_music, -1)
start_music.set_volume(0.1)
while running:
    # Если игра пройдена, то запускаем экран победы
    if winner:
        win_game()
        winner = False
    # Если игра проиграна, запускаем её с первого уровня
    if game_over:
            lose_game()
            sprite_group.empty()
            exit_group.empty()
            hero_group.empty()
            enemies_group.empty()
            current_level = 1
            level_map = load_level("level_" + str(current_level) + ".txt")
            hero, max_x, max_y, exit_game, zlo = generate_level(level_map)
            pygame.mixer.Sound.play(start_music, -1)
            start_music.set_volume(0.1)
            for bad in zlo:
                bad.move()
            enemies_group.update()
            game_over = False
    count_FPS += 1
    if count_FPS % 10 == 0:
        for bad in zlo:
            bad.move()
    enemies_group.update()
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
    # Если мы пересекаемся с врагом, то игра становится проигранной
    for dino in zlo:
        if pygame.sprite.collide_mask(hero, dino):
            game_over = True
    # Если мы пересекаемся с выходом, то переходим на новый уровень
    if pygame.sprite.collide_mask(hero, exit_game):
        pygame.mixer.Sound.play(new_lvl)
        new_lvl.set_volume(0.1)
        current_level += 1
        # Если текущий уровень не больше 6, продолжаем игру. В противном случае выигрываем)
        if current_level != quantity_levels:
            # Если уровень равен 3-ему, меняем фоновую музыку
            if current_level == 3:
                start_music.stop()
                pygame.mixer.Sound.play(late_music, -1)
                late_music.set_volume(0.1)
                sprite_group.empty()
                exit_group.empty()
                enemies_group.empty()
                hero_group.empty()
                level_map = load_level("level_" + str(current_level) + ".txt")
                hero, max_x, max_y, exit_game, zlo = generate_level(level_map)
                for bad in zlo:
                    bad.move()
                enemies_group.update()
            # Иначе продолжаем играть первую фоновую мелодию
            else:
                sprite_group.empty()
                exit_group.empty()
                enemies_group.empty()
                hero_group.empty()
                level_map = load_level("level_" + str(current_level) + ".txt")
                hero, max_x, max_y, exit_game, zlo = generate_level(level_map)
                for bad in zlo:
                    bad.move()
                enemies_group.update()
        else:
            winner = True
        continue
    else:
        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)
        exit_group.draw(screen)
        enemies_group.draw(screen)
        hero_group.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()