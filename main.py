import pygame
pygame.init()

# ========== НАСТРОЙКИ ЭКРАНА ==========
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Hockey Manager')
try:
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
except:
    pass

try:
    back_icon = pygame.image.load('images/back.png')
    back_icon = pygame.transform.scale(back_icon, (60, 60))
except:
    back_icon = None

# ========== ШРИФТЫ ==========
try:
    myfont = pygame.font.Font('fonts/f.ttf', 100)
    font = pygame.font.Font('fonts/f.ttf', 42)
    table_font = pygame.font.Font('fonts/f.ttf', 24)
except:
    myfont = pygame.font.SysFont('Arial', 100)
    font = pygame.font.SysFont('Arial', 42)
    table_font = pygame.font.SysFont('Arial', 24)

# ========== КНОПКИ ==========
button_exit = myfont.render('Exit', True, 'Black')
button_play_exit = font.render('Back', True, 'White')
button_play = myfont.render('Play', True, 'Black')

exit_rect = pygame.Rect(1000, 125, 135, 110)
play_rect = pygame.Rect(1000, 240, 135, 110)

# ========== ФОН МЕНЮ ==========
try:
    menu_image = pygame.image.load('images/m.jpg')
except:
    menu_image = None

# ========== ТАБЛИЦЫ (только заглушки, без игровых данных) ==========
table_west = [
    ["Team","W","OW","L","OL","Points"],
    ["Metalurg","0","0","0","0","0"],
    ["Avangard","0","0","0","0","0"],
    ["Ak Bars","0","0","0","0","0"],
    ["Avtomobilist","0","0","0","0","0"],
    ["Salavat Yulayev","0","0","0","0","0"],
    ["Traktor","0","0","0","0","0"],
    ["Nephtehimik","0","0","0","0","0"],
    ["Sibir","0","0","0","0","0"],
    ["Admiral","0","0","0","0","0"],
    ["Barys","0","0","0","0","0"],
    ["Amur","0","0","0","0","0"]
]

table_east = [
    ["Team","W","OW","L","OL","Points"],
    ["Lokomotiv","0","0","0","0","0"],
    ["Dinamo Minsk","0","0","0","0","0"],
    ["Dinamo Moscow","0","0","0","0","0"],
    ["Severstal","0","0","0","0","0"],
    ["Torpedo","0","0","0","0","0"],
    ["Spartak","0","0","0","0","0"],
    ["SKA","0","0","0","0","0"],
    ["CSKA","0","0","0","0","0"],
    ["Dragons","0","0","0","0","0"],
    ["Lada","0","0","0","0","0"],
    ["Sochi","0","0","0","0","0"]
]

# ========== ФУНКЦИЯ ОТРИСОВКИ ТАБЛИЦЫ ==========
def draw_table(data, start_x, start_y, cell_width, cell_height, screen, font):
    rows = len(data)
    cols = len(data[0])
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(start_x + col * cell_width,
                               start_y + row * cell_height,
                               cell_width, cell_height)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)
            text = str(data[row][col])
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

# ========== ГЛАВНАЯ ПРОГРАММА ==========
def main():
    cell_w, cell_h = 140, 30
    west_x, west_y = 100, 150
    east_x = west_x
    east_y = west_y + len(table_west) * cell_h + 80

    clock = pygame.time.Clock()
    game_state = "menu"   # "menu" или "game"
    running = True

    west_title = font.render("WEST CONFERENCE", True, (0,0,0))
    east_title = font.render("EAST CONFERENCE", True, (0,0,0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "menu":
                    if exit_rect.collidepoint(event.pos):
                        running = False
                    elif play_rect.collidepoint(event.pos):
                        game_state = "game"
                elif game_state == "game":
                    if back_icon:
                        back_rect = back_icon.get_rect(topleft=(1530,0))
                    else:
                        back_rect = pygame.Rect(1530,0,button_play_exit.get_width(), button_play_exit.get_height())
                    if back_rect.collidepoint(event.pos):
                        game_state = "menu"

        # Отрисовка в зависимости от состояния
        if game_state == "menu":
            screen.fill((255,255,255))
            if menu_image:
                screen.blit(menu_image, (100, 100))
            screen.blit(button_play, (1000, 240))
            screen.blit(button_exit, (1000, 125))
        else:
            screen.fill((255, 255, 255))
            screen.blit(west_title,(west_x,west_y - 40))
            draw_table(table_west, west_x, west_y, cell_w, cell_h, screen, table_font)
            screen.blit(east_title,(east_x,east_y - 40))
            draw_table(table_east, east_x, east_y, cell_w, cell_h, screen, table_font)

            if back_icon:
                screen.blit(back_icon, (1530, 0))
            else:
                screen.blit(button_play_exit, (1530, 0))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
