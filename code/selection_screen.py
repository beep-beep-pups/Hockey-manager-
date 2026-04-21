import pygame

def choose_team_screen(screen, teams_data, font):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    selected = None
    scroll_y = 0
    line_height = 40
    visible_lines = (HEIGHT - 200) // line_height

    team_names = [t["name"] for t in teams_data]
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_y = max(0, scroll_y - 1)
                elif event.button == 5:
                    scroll_y = min(len(team_names) - visible_lines, scroll_y + 1)
                else:
                    mouse_x, mouse_y = event.pos
                    start_y = 150
                    for i, name in enumerate(team_names):
                        if i < scroll_y or i >= scroll_y + visible_lines:
                            continue
                        rect = pygame.Rect(WIDTH//4, start_y + (i - scroll_y)*line_height, 200, line_height-5)
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected = name
                            break
        screen.fill((255,255,255))
        title = font.render("Choose your team:", True, (0,0,0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        start_y = 150
        for i, name in enumerate(team_names):
            if i < scroll_y or i >= scroll_y + visible_lines:
                continue
            rect = pygame.Rect(WIDTH//4, start_y + (i - scroll_y)*line_height, 200, line_height-5)
            pygame.draw.rect(screen, (200,200,200), rect)
            text_surf = font.render(name, True, (0,0,0))
            screen.blit(text_surf, (rect.x + 10, rect.y + 5))
        pygame.display.flip()
        clock.tick(30)

    from league import Team, Player
    for t_data in teams_data:
        if t_data["name"] == selected:
            team = Team(t_data["name"], t_data["budget"])
            for p_data in t_data["players"]:
                team.add_player(Player(p_data["name"], p_data["position"], p_data["skill"], p_data["price"]))
            return team
    return None