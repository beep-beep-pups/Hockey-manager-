import pygame
import sys
import os
import json
from league import League, Team, Player
from simulate_match import run_match_with_result
from selection_screen import choose_team_screen

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Hockey Manager')
try:
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
except:
    pass

# Шрифты
try:
    myfont = pygame.font.Font('fonts/f.ttf', 100)
    font = pygame.font.Font('fonts/table.ttf', 26)
    table_font = pygame.font.Font('fonts/table.ttf', 11)
except:
    myfont = pygame.font.SysFont('Arial', 100)
    font = pygame.font.SysFont('Arial', 42)
    table_font = pygame.font.SysFont('Arial', 18)

# Кнопки меню
button_exit = myfont.render('Exit', True, 'Black')
button_tables = myfont.render('Tables', True, 'Black')
button_match = myfont.render('Match', True, 'Black')
button_new_career = myfont.render('New Career', True, 'Black')
button_new_season = myfont.render('New Season', True, 'Black')
exit_rect = pygame.Rect(1000, 125, 135, 110)
tables_rect = pygame.Rect(1000, 240, 135, 110)
match_rect = pygame.Rect(1000, 355, 135, 110)
new_career_rect = pygame.Rect(1000, 470, 200, 110)
new_season_rect = pygame.Rect(1000, 580, 200, 110)

button_back = font.render('Back', True, 'Black')
back_rect = pygame.Rect(1550, 0, 100, 40)

try:
    menu_image = pygame.image.load('images/m.jpg')
except:
    menu_image = None

table_west = [["Team","GP","W","OW","L","OL","Points"]]
table_east = [["Team","GP","W","OW","L","OL","Points"]]

def draw_table(data, start_x, start_y, col_widths, cell_height, screen, font):
    rows = len(data)
    cols = len(data[0])
    for row in range(rows):
        x = start_x
        for col in range(cols):
            width = col_widths[col]
            rect = pygame.Rect(x, start_y + row * cell_height, width, cell_height)
            pygame.draw.rect(screen, (200,200,200), rect, 1)
            text = str(data[row][col])
            text_surface = font.render(text, True, (0,0,0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
            x += width

def update_display_tables(league):
    global table_west, table_east
    west_names = ["Metalurg","Avangard","Ak Bars","Avtomobilist","Salavat Yulayev",
                  "Traktor","Nephtehimik","Sibir","Admiral","Barys","Amur"]
    east_names = ["Lokomotiv","Dinamo Minsk","Dinamo Moscow","Severstal","Torpedo",
                  "Spartak","SKA","CSKA","Dragons","Lada","Sochi"]
    sorted_teams = league.get_standings()
    west_teams = [t for t in sorted_teams if t.name in west_names]
    east_teams = [t for t in sorted_teams if t.name in east_names]
    table_west = [["Team","GP","W","OW","L","OL","Points"]]
    for t in west_teams:
        gp = t.wins + t.wins_ot + t.loses + t.loses_ot
        table_west.append([t.name, str(gp), str(t.wins), str(t.wins_ot), str(t.loses), str(t.loses_ot), str(t.points)])
    table_east = [["Team","GP","W","OW","L","OL","Points"]]
    for t in east_teams:
        gp = t.wins + t.wins_ot + t.loses + t.loses_ot
        table_east.append([t.name, str(gp), str(t.wins), str(t.wins_ot), str(t.loses), str(t.loses_ot), str(t.points)])

def save_game(league):
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(league.to_dict(), f, ensure_ascii=False, indent=4)

def load_game():
    if not os.path.exists("save.json"):
        return None
    with open("save.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("teams.json", "r", encoding="utf-8") as f:
        teams_data = json.load(f)
    teams_dict = {}
    for t_data in teams_data:
        team = Team(t_data["name"], t_data["budget"])
        for p_data in t_data["players"]:
            team.add_player(Player(p_data["name"], p_data["position"], p_data["skill"], p_data["price"]))
        teams_dict[t_data["name"]] = team
    league = League.from_dict(data, teams_dict)
    return league

def init_new_game():
    with open("teams.json", "r", encoding="utf-8") as f:
        teams_data = json.load(f)
    teams = []
    for t_data in teams_data:
        team = Team(t_data["name"], t_data["budget"])
        for p_data in t_data["players"]:
            team.add_player(Player(p_data["name"], p_data["position"], p_data["skill"], p_data["price"]))
        teams.append(team)
    league = League(teams)
    league.generate_schedule_by_rounds(rounds_per_pair=2)
    chosen_team = choose_team_screen(screen, teams_data, font)
    league.user_team = chosen_team
    save_game(league)
    return league

def reset_career():
    if os.path.exists("save.json"):
        os.remove("save.json")
    return init_new_game()

def show_round_results(screen, results):
    WIDTH, HEIGHT = screen.get_size()
    font_small = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        screen.fill((255,255,255))
        title = font.render("Round Results", True, (0,0,0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        y = 120
        for (t1, t2, g1, g2, wtype) in results:
            text = f"{t1.name} {g1} : {g2} {t2.name}   ({wtype})"
            surf = font_small.render(text, True, (0,0,0))
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += 40
        prompt = font_small.render("Press any key to continue...", True, (0,0,0))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT - 100))
        pygame.display.flip()
        clock.tick(30)

def main():
    league = load_game()
    if league is None:
        league = init_new_game()
    if league.user_team is None:
        league = reset_career()
    col_widths = [160, 40, 40, 40, 40, 40, 50]
    cell_h = 30
    west_x, west_y = 30, 50
    east_x = west_x
    clock = pygame.time.Clock()
    game_state = "menu"
    running = True
    west_title = font.render("WESTERN CONFERENCE", True, (0,0,0))
    east_title = font.render("EASTERN CONFERENCE", True, (0,0,0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "menu":
                    if exit_rect.collidepoint(event.pos):
                        running = False
                    elif tables_rect.collidepoint(event.pos):
                        game_state = "tables"
                    elif match_rect.collidepoint(event.pos):
                        if not league.playoff_active:
                            if league.regular_season_over:
                                print("Сезон уже завершён. Нажмите New Season для нового сезона или New Career для смены команды.")
                                continue
                            user_match = league.simulate_next_user_match_and_round()
                            if user_match is None:
                                league.generate_playoff()
                                save_game(league)
                                print("Регулярный сезон завершён! Плей-офф создан.")
                            else:
                                t1, t2 = user_match
                                goals1, goals2, win_type = run_match_with_result(screen, t1, t2, is_playoff=False)
                                league.record_match_result(t1, t2, goals1, goals2, win_type)
                                results = league.simulate_remaining_matches_in_current_round()
                                save_game(league)
                                show_round_results(screen, results)
                                update_display_tables(league)
                        else:
                            playoff_match = league.get_next_playoff_match()
                            if playoff_match is None:
                                print("Play-off over!")
                                update_display_tables(league)
                            else:
                                t1, t2 = playoff_match
                                goals1, goals2, win_type = run_match_with_result(screen, t1, t2, is_playoff=True)
                                league.record_playoff_match_result(t1, t2, goals1, goals2)
                                save_game(league)
                                update_display_tables(league)
                    elif new_career_rect.collidepoint(event.pos):
                        league = reset_career()
                        update_display_tables(league)
                    elif new_season_rect.collidepoint(event.pos):
                        if not league.playoff_active and league.regular_season_over:
                            league.start_new_season()
                            save_game(league)
                            update_display_tables(league)
                            print("New season started!")
                        else:
                            print("Новый сезон можно начать только после окончания текущего.")
                elif game_state == "tables":
                    if back_rect.collidepoint(event.pos):
                        game_state = "menu"

        if game_state == "menu":
            screen.fill((255,255,255))
            if menu_image:
                screen.blit(menu_image, (100,100))
            screen.blit(button_tables, (1000,240))
            screen.blit(button_exit, (1000,125))
            screen.blit(button_match, (1000,355))
            screen.blit(button_new_career, (1000,470))
            screen.blit(button_new_season, (1000,580))
        elif game_state == "tables":
            update_display_tables(league)
            east_y = west_y + len(table_west) * cell_h + 80
            screen.fill((255,255,255))
            screen.blit(west_title, (west_x, west_y-50))
            draw_table(table_west, west_x, west_y, col_widths, cell_h, screen, table_font)
            screen.blit(east_title, (east_x, east_y-50))
            draw_table(table_east, east_x, east_y, col_widths, cell_h, screen, table_font)
            pygame.draw.rect(screen, (200,200,200), back_rect)
            screen.blit(button_back, (back_rect.x+10, back_rect.y+5))
            # Отображение сетки плей-офф (все раунды)
            if league.playoff_rounds:
                y_offset = 100
                screen.blit(font.render("PLAYOFF BRACKET", True, (0,0,0)), (west_x + 800, 50))
                for round_idx, round_pairs in enumerate(league.playoff_rounds):
                    round_name = ["First round","Quarterfinals", "Semifinals", "Finals"][round_idx] if round_idx < 3 else ""
                    screen.blit(table_font.render(round_name, True, (0,0,0)), (west_x + 800, y_offset))
                    y_offset += 25
                    for pair in round_pairs:
                        t1, t2, w1, w2 = pair
                        t1_name = t1.name if t1 else "?"
                        t2_name = t2.name if t2 else "?"
                        text = f"{t1_name} ({w1}) – ({w2}) {t2_name}"
                        screen.blit(table_font.render(text, True, (0,0,0)), (west_x + 810, y_offset))
                        y_offset += 25
                    y_offset += 10
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()