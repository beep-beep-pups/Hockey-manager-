import pygame
import random
import numpy as np

# ---------- КЛАССЫ ИГРОКОВ И КОМАНД ----------
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

# ---------- ФУНКЦИЯ СИМУЛЯЦИИ МАТЧА (С ПОДДЕРЖКОЙ ОВЕРТАЙМА) ----------
def simulate_match(team1, team2, home_team=None, home_advantage=1.1, is_playoff=False):
    def team_attack_strength(team):
        field_players = [p for p in team.players if p.position != "Goalkeeper"]
        if not field_players:
            return 52
        return sum(p.skill for p in field_players) / len(field_players)

    def save_probability(goalie_skill):
        return 0.80 + (goalie_skill / 100) * 0.1

    def get_tactic_coeffs(team):
        tactic = team.tactic
        if tactic == "aggressive":
            return 1.1, 1.1
        elif tactic == "defensive":
            return 0.9, 0.9
        return 1.0, 1.0

    base_attack1 = team_attack_strength(team1)
    base_attack2 = team_attack_strength(team2)

    attack_coeff1, defence_coeff1 = get_tactic_coeffs(team1)
    attack_coeff2, defence_coeff2 = get_tactic_coeffs(team2)

    attack1 = base_attack1 * attack_coeff1 * (home_advantage if home_team == team1 else 1.0)
    attack2 = base_attack2 * attack_coeff2 * (home_advantage if home_team == team2 else 1.0)

    attack1 *= random.uniform(0.9, 1.1)
    attack2 *= random.uniform(0.9, 1.1)

    def select_goalie(team):
        goalies = [p for p in team.players if p.position == "Goalkeeper"]
        if not goalies:
            return None
        if len(goalies) == 1:
            return goalies[0]
        best = max(goalies, key=lambda g: g.skill)
        return best if random.random() < 0.8 else random.choice(goalies)

    goalie1 = select_goalie(team1)
    goalie2 = select_goalie(team2)

    total_goals1 = total_goals2 = 0
    goal_events = []  # (abs_time, team_name, player_name)
    PERIOD_LEN_SEC = 20 * 60

    # Три периода
    for period in range(1, 4):
        exp_shots1 = 7 + (attack1 - 70) * 0.03
        exp_shots2 = 7 + (attack2 - 70) * 0.03
        exp_shots1 = max(5, min(15, exp_shots1)) * defence_coeff2
        exp_shots2 = max(5, min(15, exp_shots2)) * defence_coeff1

        shots1 = int(np.random.poisson(exp_shots1))
        shots2 = int(np.random.poisson(exp_shots2))

        if goalie2:
            goals1 = int(shots1 * (1 - save_probability(goalie2.skill)) + random.gauss(0, 0.5))
            goals1 = max(0, min(shots1, goals1))
            goalie2.saves += shots1 - goals1
            goalie2.goals_against += goals1
        else:
            goals1 = shots1

        if goalie1:
            goals2 = int(shots2 * (1 - save_probability(goalie1.skill)) + random.gauss(0, 0.5))
            goals2 = max(0, min(shots2, goals2))
            goalie1.saves += shots2 - goals2
            goalie1.goals_against += goals2
        else:
            goals2 = shots2

        scorer_names1 = [p.name for p in team1.players if p.position != "Goalkeeper"] or [team1.name]
        for _ in range(goals1):
            scorer = random.choice(scorer_names1)
            t_in_period = random.uniform(0, PERIOD_LEN_SEC)
            abs_time = (period - 1) * PERIOD_LEN_SEC + t_in_period
            goal_events.append((abs_time, team1.name, scorer))

        scorer_names2 = [p.name for p in team2.players if p.position != "Goalkeeper"] or [team2.name]
        for _ in range(goals2):
            scorer = random.choice(scorer_names2)
            t_in_period = random.uniform(0, PERIOD_LEN_SEC)
            abs_time = (period - 1) * PERIOD_LEN_SEC + t_in_period
            goal_events.append((abs_time, team2.name, scorer))

        total_goals1 += goals1
        total_goals2 += goals2

    # Овертайм (если ничья)
    winner = None
    base_time = 3 * PERIOD_LEN_SEC

    if total_goals1 == total_goals2:
        if is_playoff:
            ot_len = 20 * 60
            while True:
                expected_goal_time = 1 / ((attack1 + attack2) / 200 / ot_len) if (attack1+attack2) > 0 else ot_len+1
                time_to_goal = random.expovariate(1 / expected_goal_time) if expected_goal_time > 0 else ot_len+1
                if time_to_goal <= ot_len:
                    scorer_team = team1 if random.random() < attack1/(attack1+attack2) else team2
                    abs_time = base_time + time_to_goal
                    goal_events.append((abs_time, scorer_team.name, "Овертайм"))
                    if scorer_team == team1:
                        total_goals1 += 1
                        winner = team1
                    else:
                        total_goals2 += 1
                        winner = team2
                    break
                else:
                    base_time += ot_len
        else:
            ot_len = 5 * 60
            expected_goal_time = 1 / ((attack1 + attack2) / 200 / ot_len) if (attack1+attack2) > 0 else ot_len+1
            time_to_goal = random.expovariate(1 / expected_goal_time) if expected_goal_time > 0 else ot_len+1
            if time_to_goal <= ot_len:
                scorer_team = team1 if random.random() < attack1/(attack1+attack2) else team2
                abs_time = base_time + time_to_goal
                goal_events.append((abs_time, scorer_team.name, "Овертайм"))
                if scorer_team == team1:
                    total_goals1 += 1
                    winner = team1
                else:
                    total_goals2 += 1
                    winner = team2
            else:
                # Буллиты
                shootout_score1 = 0
                shootout_score2 = 0
                skaters1 = [p for p in team1.players if p.position != "Goalkeeper"] or [Player("Unknown", "Forward", 50)]
                skaters2 = [p for p in team2.players if p.position != "Goalkeeper"] or [Player("Unknown", "Forward", 50)]

                def shootout_prob(shooter, goalie):
                    prob = 0.3 + (shooter.skill - (goalie.skill if goalie else 50)) / 200
                    return max(0.05, min(0.7, prob))

                base_time += ot_len
                for r in range(1, 6):
                    s1 = random.choice(skaters1)
                    s2 = random.choice(skaters2)
                    g1 = random.random() < shootout_prob(s1, goalie2)
                    g2 = random.random() < shootout_prob(s2, goalie1)
                    if g1:
                        shootout_score1 += 1
                    if g2:
                        shootout_score2 += 1
                    goal_events.append((base_time + r * 0.1, team1.name, f"Буллит: {s1.name} {'забил' if g1 else 'не забил'}"))
                    goal_events.append((base_time + r * 0.1, team2.name, f"Буллит: {s2.name} {'забил' if g2 else 'не забил'}"))
                r = 6
                while shootout_score1 == shootout_score2:
                    s1 = random.choice(skaters1)
                    s2 = random.choice(skaters2)
                    g1 = random.random() < shootout_prob(s1, goalie2)
                    g2 = random.random() < shootout_prob(s2, goalie1)
                    if g1:
                        shootout_score1 += 1
                    if g2:
                        shootout_score2 += 1
                    goal_events.append((base_time + r * 0.1, team1.name, f"Буллит: {s1.name} {'забил' if g1 else 'не забил'}"))
                    goal_events.append((base_time + r * 0.1, team2.name, f"Буллит: {s2.name} {'забил' if g2 else 'не забил'}"))
                    r += 1
                    if g1 != g2:
                        break
                winner = team1 if shootout_score1 > shootout_score2 else team2
                if winner == team1:
                    total_goals1 += 1
                else:
                    total_goals2 += 1
                goal_events.append((base_time + r * 0.1, winner.name, "Победа в буллитах"))
    else:
        winner = team1 if total_goals1 > total_goals2 else team2

    goal_events.sort(key=lambda x: x[0])
    return {
        "total_score": (total_goals1, total_goals2),
        "goal_events": goal_events,
        "winner": winner.name
    }

# ---------- ГРАФИЧЕСКАЯ СИМУЛЯЦИЯ ----------
pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
ICE = (200, 220, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Хоккейный менеджер - Симуляция матча")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
event_font = pygame.font.Font(None, 28)

rink_bg = None

# Загрузка изображений игроков (маленькие, 64x64)
try:
    player_left_img = pygame.image.load('images/player_left.png')
    player_left_img = pygame.transform.scale(player_left_img, (64, 64))
except:
    player_left_img = None
try:
    player_right_img = pygame.image.load('images/player_right.png')
    player_right_img = pygame.transform.scale(player_right_img, (64, 64))
except:
    player_right_img = None

def create_test_team(name, strength_level=75):
    team = Team(name)
    for i in range(3):
        skill = random.randint(strength_level-10, strength_level+10)
        team.add_player(Player(f"F{i+1}", "Forward", skill))
    for i in range(2):
        skill = random.randint(strength_level-10, strength_level+10)
        team.add_player(Player(f"D{i+1}", "Defenseman", skill))
    goalie_skill = random.randint(strength_level-5, strength_level+15)
    team.add_player(Player("G1", "Goalkeeper", goalie_skill))
    return team

is_playoff = False
team1 = create_test_team("Динамо", 80)
team2 = create_test_team("ЦСКА", 75)

match_data = simulate_match(team1, team2, home_team=team1, is_playoff=is_playoff)
goal_events = match_data["goal_events"]

PERIOD_LEN_SEC = 20 * 60
current_abs_time = 0.0
goals1, goals2 = 0, 0
paused = False
match_over = False
events = []
next_event_idx = 0
TIME_FACTOR = 60

PAUSE_AFTER_GOAL = 2.0
freeze_until = 0.0
freeze_message = ""

def get_current_period(abs_time):
    if abs_time < PERIOD_LEN_SEC:
        return 1
    elif abs_time < 2 * PERIOD_LEN_SEC:
        return 2
    elif abs_time < 3 * PERIOD_LEN_SEC:
        return 3
    else:
        return 4

def format_abs_time(abs_seconds):
    minutes = int(abs_seconds // 60)
    seconds = int(abs_seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def format_remaining_time(abs_time):
    period = get_current_period(abs_time)
    if period <= 3:
        period_start = (period - 1) * PERIOD_LEN_SEC
        elapsed = abs_time - period_start
        remaining = PERIOD_LEN_SEC - elapsed
        if remaining < 0:
            remaining = 0
        return format_abs_time(remaining)
    else:
        ot_len = 5 * 60 if not is_playoff else 20 * 60
        elapsed = abs_time - 3 * PERIOD_LEN_SEC
        remaining = ot_len - elapsed
        if remaining < 0:
            remaining = 0
        return format_abs_time(remaining)

def add_event(text):
    events.insert(0, text)
    if len(events) > 6:
        events.pop()

def draw_background():
    if rink_bg:
        screen.blit(rink_bg, (0, 0))
    else:
        screen.fill(ICE)

def draw_players():
    # Рисуем изображения хоккеистов по бокам
    if player_left_img:
        screen.blit(player_left_img, (50, HEIGHT // 2 - 32))
    else:
        pygame.draw.circle(screen, BLACK, (82, HEIGHT // 2), 32, 2)
    if player_right_img:
        screen.blit(player_right_img, (WIDTH - 114, HEIGHT // 2 - 32))
    else:
        pygame.draw.circle(screen, BLACK, (WIDTH - 82, HEIGHT // 2), 32, 2)

def draw_scoreboard():
    # Счёт
    score_text = font.render(f"{goals1} : {goals2}", True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 40))
    screen.blit(score_text, score_rect)
    # Названия команд
    team1_text = font.render(team1.name, True, BLACK)
    team2_text = font.render(team2.name, True, BLACK)
    screen.blit(team1_text, (WIDTH // 2 - 150, 10))
    screen.blit(team2_text, (WIDTH // 2 + 50, 10))
    # Период и время
    period_num = get_current_period(current_abs_time)
    if period_num == 4:
        period_str = "ОВЕРТАЙМ"
    else:
        period_str = f"{period_num} ПЕРИОД"
    period_surf = font.render(period_str, True, BLACK)
    time_surf = font.render(format_remaining_time(current_abs_time), True, BLACK)
    screen.blit(period_surf, (20, 20))
    screen.blit(time_surf, (20, 60))

def draw_events():
    start_y = HEIGHT - 100
    step = 30
    for i, ev in enumerate(events[:6]):
        surf = event_font.render(ev, True, BLACK)
        rect = surf.get_rect(center=(WIDTH // 2, start_y - i * step))
        screen.blit(surf, rect)

def draw_freeze_message():
    if freeze_until > pygame.time.get_ticks() / 1000.0 and freeze_message:
        surf = font.render(freeze_message, True, BLACK)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(surf, rect)

def check_period_end():
    global match_over, current_abs_time
    # Если время перевалило за 3 периода и матч ещё не окончен
    if current_abs_time >= 3 * PERIOD_LEN_SEC and not match_over:
        # Если счёт не равный, матч окончен
        if goals1 != goals2:
            match_over = True
            return
        # Если равный, овертайм уже должен был начаться, но возможно время ушло вперёд – ничего не делаем
    # Добавляем события конца периода только в ленту, без заморозки
    for border in [PERIOD_LEN_SEC, 2 * PERIOD_LEN_SEC]:
        if abs(current_abs_time - border) < 0.1 and border < 3 * PERIOD_LEN_SEC:
            period = int(border / PERIOD_LEN_SEC)
            add_event(f"Конец {period} периода. Счёт {goals1}:{goals2}")
            # Не ставим freeze_until, только событие
            break

running = True
while running:
    clock.tick(FPS)
    current_real_time = pygame.time.get_ticks() / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused and not match_over and current_real_time >= freeze_until:
        dt = TIME_FACTOR / FPS
        old_time = current_abs_time
        current_abs_time += dt

        # Проверка окончания периодов (добавление событий в ленту)
        check_period_end()

        # Обработка голов
        while next_event_idx < len(goal_events):
            ev_time, ev_team, ev_text = goal_events[next_event_idx]
            if ev_time <= current_abs_time:
                # Гол или событие
                if "Буллит" not in ev_text and "Победа" not in ev_text:
                    if ev_team == team1.name:
                        goals1 += 1
                    else:
                        goals2 += 1
                    time_str = format_abs_time(ev_time)
                    add_event(f"ГОЛ! {ev_team}: {ev_text} на {time_str}")
                else:
                    add_event(f"{ev_team}: {ev_text}")
                next_event_idx += 1
                # Заморозка после гола (только короткое сообщение)
                if "Буллит" not in ev_text:
                    freeze_until = current_real_time + PAUSE_AFTER_GOAL
                    freeze_message = "ГОЛ!"
                # Если это гол в овертайме или победа в буллитах, завершаем матч
                if "Овертайм" in ev_text or "Победа" in ev_text:
                    match_over = True
                # Если время перевалило за 3 периода и счёт не равный, завершаем
                if current_abs_time >= 3 * PERIOD_LEN_SEC and goals1 != goals2:
                    match_over = True
                break
            else:
                break

        # Если время закончилось и ничья, овертайм уже должен быть обработан через goal_events
        # Если овертайм есть, гол будет добавлен из goal_events

    # Отрисовка
    draw_background()
    draw_players()
    draw_scoreboard()
    draw_events()
    draw_freeze_message()

    if paused:
        pause_surf = font.render("ПАУЗА (ПРОБЕЛ)", True, BLACK)
        screen.blit(pause_surf, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
