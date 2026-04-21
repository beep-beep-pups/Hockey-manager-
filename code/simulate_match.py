import pygame
import random
import numpy as np

class Player:
    def __init__(self, name, position, skill, price=0):
        self.name = name
        self.position = position
        self.skill = skill
        self.price = price
        self.games_played = 0
        self.goals = 0
        self.assists = 0
        self.points = 0
        self.saves = 0
        self.goals_against = 0
        self.plus_minus = 0

class Team:
    def __init__(self, name, tactic="neutral"):
        self.name = name
        self.players = []
        self.tactic = tactic
        self.wins = 0
        self.wins_ot = 0
        self.loses = 0
        self.loses_ot = 0
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0

    def add_player(self, player):
        self.players.append(player)

def simulate_match_dry(team1, team2, home_team=None, home_advantage=1.1, is_playoff=False):
    def team_attack_strength(team):
        field = [p for p in team.players if p.position != "Goalkeeper"]
        if not field:
            return 52
        return sum(p.skill for p in field) / len(field)

    def save_prob(goalie_skill):
        return 0.80 + (goalie_skill / 100) * 0.1

    def get_tactic_coeffs(team):
        t = team.tactic
        if t == "aggressive":
            return 1.1, 1.1
        elif t == "defensive":
            return 0.9, 0.9
        return 1.0, 1.0

    base1 = team_attack_strength(team1)
    base2 = team_attack_strength(team2)
    ac1, dc1 = get_tactic_coeffs(team1)
    ac2, dc2 = get_tactic_coeffs(team2)
    attack1 = base1 * ac1 * (home_advantage if home_team == team1 else 1.0) * random.uniform(0.9,1.1)
    attack2 = base2 * ac2 * (home_advantage if home_team == team2 else 1.0) * random.uniform(0.9,1.1)

    def select_goalie(team):
        goalies = [p for p in team.players if p.position == "Goalkeeper"]
        if not goalies:
            return None
        if len(goalies) == 1:
            return goalies[0]
        best = max(goalies, key=lambda g: g.skill)
        return best if random.random() < 0.8 else random.choice(goalies)

    g1 = select_goalie(team1)
    g2 = select_goalie(team2)

    total1 = total2 = 0
    PERIOD_LEN = 20*60
    for period in range(1,4):
        exp_shots1 = max(5, min(15, 7 + (attack1-70)*0.03)) * dc2
        exp_shots2 = max(5, min(15, 7 + (attack2-70)*0.03)) * dc1
        shots1 = int(np.random.poisson(exp_shots1))
        shots2 = int(np.random.poisson(exp_shots2))
        if g2:
            goals1 = int((shots1 * (1 - save_prob(g2.skill)) + random.gauss(0,0.5)) * 1.3)
            goals1 = max(0, min(shots1, goals1))
            g2.saves += shots1 - goals1
            g2.goals_against += goals1
        else:
            goals1 = shots1
        if g1:
            goals2 = int((shots2 * (1 - save_prob(g1.skill)) + random.gauss(0,0.5)) * 1.3)
            goals2 = max(0, min(shots2, goals2))
            g1.saves += shots2 - goals2
            g1.goals_against += goals2
        else:
            goals2 = shots2
        total1 += goals1
        total2 += goals2

    winner = None
    win_type = "regulation"
    if total1 == total2:
        if is_playoff:
            if random.random() < 0.5:
                total1 += 1
                winner = team1
            else:
                total2 += 1
                winner = team2
            win_type = "ot"
        else:
            if random.random() < 0.5:
                total1 += 1
                winner = team1
                win_type = "ot"
            else:
                s1 = s2 = 0
                for _ in range(5):
                    if random.random() < 0.5:
                        s1 += 1
                    if random.random() < 0.5:
                        s2 += 1
                if s1 == s2:
                    s1 += 1 if random.random() < 0.5 else 0
                    s2 += 1 if random.random() < 0.5 else 0
                winner = team1 if s1 > s2 else team2
                win_type = "shootout"
                if winner == team1:
                    total1 += 1
                else:
                    total2 += 1
    else:
        winner = team1 if total1 > total2 else team2

    return {"score": (total1, total2), "win_type": win_type, "winner": winner}

def run_match_with_result(screen, team1, team2, is_playoff=False):
    WIDTH, HEIGHT = screen.get_size()
    BLACK = (0,0,0)
    ICE = (200,220,255)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    event_font = pygame.font.Font(None, 28)

    try:
        player_left = pygame.image.load('images/player1.jpg')
        player_left = pygame.transform.scale(player_left, (500,500))
    except:
        player_left = None
    try:
        player_right = pygame.image.load('images/player2.jpg')
        player_right = pygame.transform.scale(player_right, (500,500))
    except:
        player_right = None

    dry = simulate_match_dry(team1, team2, home_team=team1, is_playoff=is_playoff)
    goals1_final, goals2_final = dry["score"]
    win_type_final = dry["win_type"]

    goal_events = []
    PERIOD_LEN = 20*60
    for _ in range(goals1_final):
        period = random.randint(1,3)
        t = random.uniform(0, PERIOD_LEN)
        abs_time = (period-1)*PERIOD_LEN + t
        scorer = random.choice([p.name for p in team1.players if p.position!="Goalkeeper"] or [team1.name])
        goal_events.append((abs_time, team1.name, scorer))
    for _ in range(goals2_final):
        period = random.randint(1,3)
        t = random.uniform(0, PERIOD_LEN)
        abs_time = (period-1)*PERIOD_LEN + t
        scorer = random.choice([p.name for p in team2.players if p.position!="Goalkeeper"] or [team2.name])
        goal_events.append((abs_time, team2.name, scorer))
    goal_events.sort(key=lambda x: x[0])

    current_abs_time = 0.0
    goals1, goals2 = 0, 0
    paused = False
    match_over = False
    events = []
    next_ev_idx = 0
    TIME_FACTOR = 60
    PAUSE_GOAL = 2.0
    PAUSE_PERIOD = 2.5
    freeze_until = 0.0
    freeze_msg = ""
    ot_pause_flag = False

    def get_period(abs_time):
        if abs_time < PERIOD_LEN: return 1
        if abs_time < 2*PERIOD_LEN: return 2
        if abs_time < 3*PERIOD_LEN: return 3
        return 4

    def format_abs_time(sec):
        m = int(sec//60)
        s = int(sec%60)
        return f"{m:02d}:{s:02d}"

    def format_remaining_time(abs_time):
        period = get_period(abs_time)
        if period <= 3:
            period_start = (period-1)*PERIOD_LEN
            elapsed = abs_time - period_start
            remaining = PERIOD_LEN - elapsed
            return format_abs_time(max(0, remaining))
        else:
            ot_len = 5*60 if not is_playoff else 20*60
            elapsed = abs_time - 3*PERIOD_LEN
            remaining = ot_len - elapsed
            return format_abs_time(max(0, remaining))

    def add_event(text):
        events.append(text)
        if len(events) > 8:
            events.pop(0)

    def draw_bg():
        screen.fill(ICE)

    def draw_players():
        if player_left:
            screen.blit(player_left, (20, HEIGHT//2 - 50))
        else:
            pygame.draw.circle(screen, BLACK, (70, HEIGHT//2), 40, 2)
        if player_right:
            screen.blit(player_right, (WIDTH - 500, HEIGHT//2 - 50))
        else:
            pygame.draw.circle(screen, BLACK, (WIDTH - 70, HEIGHT//2), 40, 2)

    def draw_scoreboard():
        score_surf = font.render(f"{goals1} : {goals2}", True, BLACK)
        screen.blit(score_surf, (WIDTH//2 - 30, 40))
        t1_surf = font.render(team1.name, True, BLACK)
        t2_surf = font.render(team2.name, True, BLACK)
        screen.blit(t1_surf, (WIDTH//2 - 150, 10))
        screen.blit(t2_surf, (WIDTH//2 + 50, 10))
        period_num = get_period(current_abs_time)
        period_str = f"{period_num} PERIOD" if period_num <= 3 else "OVERTIME"
        period_surf = font.render(period_str, True, BLACK)
        time_surf = font.render(format_remaining_time(current_abs_time), True, BLACK)
        screen.blit(period_surf, (20, 20))
        screen.blit(time_surf, (20, 60))

    def draw_events():
        y = 100
        step = 30
        for i, ev in enumerate(events[-6:]):
            surf = event_font.render(ev, True, BLACK)
            rect = surf.get_rect(center=(WIDTH//2, y + i*step))
            screen.blit(surf, rect)

    def draw_freeze():
        if freeze_until > pygame.time.get_ticks()/1000 and freeze_msg:
            surf = font.render(freeze_msg, True, BLACK)
            rect = surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
            screen.blit(surf, rect)

    def check_period_end():
        nonlocal match_over, freeze_until, freeze_msg, ot_pause_flag
        for border in [PERIOD_LEN, 2*PERIOD_LEN]:
            if abs(current_abs_time - border) < 0.1 and border < 3*PERIOD_LEN:
                period = int(border / PERIOD_LEN)
                add_event(f"{period} period over: {goals1}:{goals2}")
                freeze_until = pygame.time.get_ticks()/1000 + PAUSE_PERIOD
                freeze_msg = f"{period} period over"
                return
        if current_abs_time >= 3*PERIOD_LEN and not match_over:
            if goals1 != goals2:
                match_over = True
                add_event(f"Match over! {goals1}:{goals2}")
            else:
                if not ot_pause_flag:
                    freeze_until = pygame.time.get_ticks()/1000 + PAUSE_PERIOD
                    freeze_msg = "OVERTIME"
                    ot_pause_flag = True
                    return

    running = True
    while running:
        now = pygame.time.get_ticks() / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    paused = not paused
                if e.key == pygame.K_q:
                    goals1, goals2 = goals1_final, goals2_final
                    match_over = True
                    add_event(f"Match over! {goals1}:{goals2}")
                    draw_bg()
                    draw_players()
                    draw_scoreboard()
                    draw_events()
                    draw_freeze()
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    running = False
                    break

        if not paused and not match_over and now >= freeze_until:
            dt = TIME_FACTOR / 60.0
            current_abs_time += dt
            check_period_end()

            while next_ev_idx < len(goal_events):
                ev_time, team_name, scorer = goal_events[next_ev_idx]
                if ev_time <= current_abs_time:
                    if team_name == team1.name:
                        goals1 += 1
                    else:
                        goals2 += 1
                    add_event(f"Goal! {scorer} {format_abs_time(ev_time)}")
                    next_ev_idx += 1
                    freeze_until = now + PAUSE_GOAL
                    freeze_msg = "Goal!"
                    if ev_time >= 3*PERIOD_LEN:
                        match_over = True
                    break
                else:
                    break

            if current_abs_time >= 3*PERIOD_LEN and goals1 != goals2 and not match_over:
                match_over = True
                add_event(f"Match over! {goals1}:{goals2}")

        draw_bg()
        draw_players()
        draw_scoreboard()
        draw_events()
        draw_freeze()
        if paused:
            pause_surf = font.render("PAUSE", True, BLACK)
            screen.blit(pause_surf, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        clock.tick(60)

    return goals1, goals2, win_type_final