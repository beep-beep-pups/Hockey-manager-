import pygame
import random
import numpy as np
import math
from typing import Optional, Tuple
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Hockey Manager')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

myfont = pygame.font.Font('fonts/f.ttf', 100)
font = pygame.font.Font('fonts/f.ttf', 42)

button_exit = myfont.render('Exit', True, 'Black')
button_play_exit = font.render('Back', True, 'White')
button_play = myfont.render('Play', True, 'Black')

exit_rect = pygame.Rect(1000, 125, 135, 110)
exit_play_rect = pygame.Rect(1530, 0, 60, 50)
play_rect = pygame.Rect(1000, 240, 135, 110)

menu_image = pygame.image.load('images/m.jpg')

class player:
    def __init__(self, name: str , position: str , skill: int, price: int):
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

    def to_dict(self):
        return{
            "name": self.name,
            "position": self.position,
            "skill": self.skill,
            "price": self.price,
            "games_played": self.games_played,
            "goals": self.goals,
            "assists": self.assists,
            "points": self.points,
            "saves": self.saves,
            "goals_against": self.goals_against,
            "plus_minus": self.plus_minus
        }

    @staticmethod
    def from_dict(data):
        p = player(data["name"], data["position"], data["skill"], data.get("price"))
        p.games_played = data.get("games_played", 0)
        p.goals = data.get("goals", 0)
        p.assists = data.get("assists", 0)
        p.points = data.get("points", 0)
        p.saves = data.get("saves", 0)
        p.goals_against = data.get("goals_against", 0)
        return p

class Team:
    def __init__(self, name, budget):
        self.name = name
        self.players = []
        self.budget = budget
        self.wins = 0
        self.wins_ot = 0
        self.loses = 0
        self.loses_ot = 0
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.playoff_wins = 0
        self.tactic = "neutral"

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def to_dict(self):
        return {
            "name": self.name,
            "budget": self.budget,
            "players": [p.to_dict() for p in self.players],
            "wins": self.wins,
            "wins_ot": self.wins_ot,
            "loses": self.loses,
            "loses_ot": self.loses_ot,
            "points": self.points,
            "goals_scored": self.goals_scored,
            "goals_conceded": self.goals_conceded
        }

    @staticmethod
    def from_dict(data):
        team = Team(data["name"], data.get("budget"))
        for p_data in data["players"]:
            team.add_player(player.from_dict(p_data))
        team.wins = data.get("wins", 0)
        team.wins_ot = data.get("wins_ot", 0)
        team.loses = data.get("loses", 0)
        team.loses_ot = data.get("loses_ot", 0)
        team.points = data.get("points", 0)
        team.goals_scored = data.get("goals_scored", 0)
        team.goals_conceded = data.get("goals_conceded", 0)
        return team

def simulating_match(team1, team2, home_team=None, home_advantage=1.1, is_playoff=False):
    def team_attack_strength(team):
        field_players = [p for p in team.players if p.position != "Goalkeeper"]
        if not field_players:
            return 52
        strength = sum(p.skill for p in field_players) / len(field_players)
        return strength

    def save_probability(goalkeeper_skill):
        return 0.80 + (goalkeeper_skill / 100) * 0.1

    base_attack1 = team_attack_strength(team1)
    base_attack2 = team_attack_strength(team2)

    def get_tactic_coeffs(team):
        tactic = getattr(team, 'tactic', 'neutral')
        if tactic == "aggressive":
            return 1.1, 1.1
        elif tactic == "defensive":
            return 0.9, 0.9
        else:
            return 1.0, 1.0

    attack_coeff1, defence_coeff1 = get_tactic_coeffs(team1)
    attack_coeff2, defence_coeff2 = get_tactic_coeffs(team2)

    attack1_final = base_attack1 * attack_coeff1
    attack1_final *= (home_advantage if home_team == team1 else 1.0)
    attack2_final = base_attack2 * attack_coeff2
    attack2_final *= (home_advantage if home_team == team2 else 1.0)

    factor1 = random.uniform(0.9, 1.1)
    factor2 = random.uniform(0.9, 1.1)
    attack1 = attack1_final * factor1
    attack2 = attack2_final * factor2

    def select_goalie(team):
        goalies = [p for p in team.players if p.position == "Goalkeeper"]
        if len(goalies) == 1:
            return goalies[0]
        goalies_sorted = sorted(goalies, key=lambda g: g.skill, reverse=True)
        best = goalies_sorted[0]
        if random.random() < 0.8:
            return best
        else:
            return random.choice(goalies_sorted[1:])

    goalie1 = select_goalie(team1)
    goalie2 = select_goalie(team2)

    total_goals1 = 0
    total_goals2 = 0
    period_reports = []
    base_shots_per_period = 7
    shots_factor = 0.03
    winner = None

    for period in range(1, 4):

        exp_shots1 = base_shots_per_period + (attack1 - 70) * shots_factor
        exp_shots2 = base_shots_per_period + (attack2 - 70) * shots_factor
        exp_shots1 = int(exp_shots1)
        exp_shots2 = int(exp_shots2)
        exp_shots1 = max(5, min(15, exp_shots1))
        exp_shots2 = max(5, min(15, exp_shots2))

        exp_shots1 *= defence_coeff2
        exp_shots2 *= defence_coeff1

        shots1 = int(np.random.poisson(exp_shots1))
        shots2 = int(np.random.poisson(exp_shots2))

        if goalie2:
            save_pct2 = save_probability(goalie2.skill)
            goals1 = int(shots1 * (1 - save_pct2) + random.gauss(0, 0.5))
            goals1 = max(0, min(shots1, goals1))
            goalie2.saves += (shots1 - goals1)
            goalie2.against_goals += goals1
        else:
            goals1 = shots1

        if goalie1:
            save_pct1 = save_probability(goalie1.skill)
            goals2 = int(shots2 * (1 - save_pct1) + random.gauss(0, 0.5))
            goals2 = max(0, min(shots2, goals2))
            goalie1.saves += (shots2 - goals2)
            goalie1.against_goals += goals2
        else:
            goals2 = shots2

        for _ in range(goals1):
            field = [p for p in team1.players if p.position != "Goalkeeper"]

            if field:
                scorer = random.choice(field)
                scorer.goals += 1
                scorer.points += 1

                if random.random() < 0.8:
                    possible_assistant = [p for p in field if p != scorer and p.position != "Goalkeeper"]
                    if possible_assistant:
                        assistant = random.choice(possible_assistant)
                        assistant.assists += 1
                        assistant.points += 1
                for i in range(5):
                    for p in team1.players:
                        if p.position != "Goalkeeper":
                            p.plus_minus += 1
                for j in range(5):
                    for p in team2.players:
                        if p.position != "Goalkeeper":
                            p.plus_minus -= 1

        for _ in range(goals2):
            field = [p for p in team2.players if p.position != "Goalkeeper"]

            if field:
                scorer = random.choice(field)
                scorer.goals += 1
                scorer.points += 1

                if random.random() < 0.8:
                    possible_assistant = [p for p in field if p != scorer and p.position != "Goalkeeper"]
                    if possible_assistant:
                        assistant = random.choice(possible_assistant)
                        assistant.assists += 1
                        assistant.points += 1
                for i in range(5):
                    for p in team2.players:
                        if p.position != "Goalkeeper":
                            p.plus_minus += 1
                for j in range(5):
                    for p in team1.players:
                        if p.position != "Goalkeeper":
                            p.plus_minus -= 1

        total_goals1 += goals1
        total_goals2 += goals2
        period_reports.append(
            f"{period} Period: \n"
            f"Team {team1.name}: {shots1} shots, {goals1} goals\n"
            f"Team {team2.name}: {shots2} shots, {goals2} goals"
        )

    ot_goals1 = 0
    ot_goals2 = 0
    shootout_score1 = 0
    shootout_score2 = 0
    win_type = None
    ot_winner = None

    if total_goals1 == total_goals2:
        if is_playoff:
            while True:
                expected_ot_goals1 = attack1 / 400
                expected_ot_goals2 = attack2 / 400
                if expected_ot_goals1 > 0 or expected_ot_goals2 > 0:
                    u1 = random.random()
                    u2 = random.random()
                    if u1 == 0: u1 = 1e-10
                    if u2 == 0: u2 = 1e-10

                    time1 = -math.log(1 - u1) / expected_ot_goals1 if expected_ot_goals1 > 0 else float('inf')
                    time2 = -math.log(1 - u2) / expected_ot_goals2 if expected_ot_goals2 > 0 else float('inf')

                    if time1 < time2:
                        ot_winner = team1
                        ot_goals1 = 1
                        win_type = "ot_playoff"
                        break
                    elif time2 < time1:
                        ot_winner = team2
                        ot_goals2 = 1
                        win_type = "ot_playoff"
                        break
                    else:
                        continue
                else:
                    if random.random() < 0.5:
                        ot_winner = team1
                        ot_goals1 = 1
                    else:
                        ot_winner = team2
                        ot_goals2 = 1
                    win_type = "ot_playoff"
                    break
            total_goals1 += ot_goals1
            total_goals2 += ot_goals2
            period_reports.append(f"Overtime: {ot_winner.name} score and win!")

        else:
            expected_ot_goals1 = attack1 / 240
            expected_ot_goals2 = attack2 / 240
            if expected_ot_goals1 > 0 or expected_ot_goals2 > 0:
                u1 = random.random()
                u2 = random.random()
                if u1 == 0: u1 = 1e-10
                if u2 == 0: u2 = 1e-10

                time1 = -math.log(1 - u1) / expected_ot_goals1 if expected_ot_goals1 > 0 else float('inf')
                time2 = -math.log(1 - u2) / expected_ot_goals2 if expected_ot_goals2 > 0 else float('inf')

                if time1 < time2:
                    ot_winner = team1
                    ot_goals1 = 1
                elif time2 < time1:
                    ot_winner = team2
                    ot_goals2 = 1
                else:
                    ot_winner = None
            if ot_winner is not None:
                total_goals1 += ot_goals1
                total_goals2 += ot_goals2
                if ot_winner == team1:
                    field = [p for p in team1.players if p.position != "Goalkeeper"]
                    if field:
                        scorer = random.choice(field)
                        scorer.goals += 1
                        scorer.points += 1
                    win_type = "ot"
                    ot_winner = team1
                    period_reports.append(f"Overtime: {team1.name} score goal and win")
                else:
                    field = [p for p in team2.players if p.position != "Goalkeeper"]
                    if field:
                        scorer = random.choice(field)
                        scorer.goals += 1
                        scorer.points += 1
                    win_type = "ot"
                    ot_winner = team2
                    period_reports.append(f"Overtime: {team2.name} score goal and win")
            else:
                win_type = "shootout"
                period_reports.append(f"The overtime ended with no goals. Shootout series")

            skaters1 = [p for p in team1.players if p.position != "Goalkeeper"]
            skaters2 = [p for p in team2.players if p.position != "Goalkeeper"]

            available1 = skaters1.copy()
            available2 = skaters2.copy()
            attempt = 0
            shootout_report = []

            def shootout_prob(shooter, goalie):
                prob = 0.3 + (shooter.skill - (goalie.skill if goalie else 50)) / 200
                return max(0.05, min(0.7, prob))

            for _ in range(5):
                if not available1:
                    available1 = skaters1.copy()
                if not available2:
                    available2 = skaters2.copy()

                shooter1 = random.choice(available1)
                shooter2 = random.choice(available2)
                available1.remove(shooter1)
                available2.remove(shooter2)

                goal1 = random.random() < shootout_prob(shooter1, goalie2)
                goal2 = random.random() < shootout_prob(shooter2, goalie1)

                if goal1:
                    shootout_score1 += 1
                if goal2:
                    shootout_score2 += 1

                shootout_report.append(
                    f"(shooter1.name) - {'score' if goal1 else 'not score'}"
                    f"(shooter2.name) - {'score' if goal2 else 'not score'}"
                )
                attempt += 1
            while shootout_score1 == shootout_score2:
                if not available1:
                    available1 = skaters1.copy()
                if not available2:
                    available2 = skaters2.copy()
                shooter1 = random.choice(available1)
                shooter2 = random.choice(available2)
                available1.remove(shooter1)
                available2.remove(shooter2)

                goal1 = random.random() < shootout_prob(shooter1, goalie2)
                goal2 = random.random() < shootout_prob(shooter2, goalie1)
                if goal1:
                    shootout_score1 += 1
                if goal2:
                    shootout_score2 += 1
                attempt += 1
                shootout_report.append(
                    f"{attempt}: {shooter1.name} – {'score' if goal1 else 'not score'}, "
                    f"{shooter2.name} – {'score' if goal2 else 'not score'}"
                )
                if goal1 != goal2:
                    break

            winner = team1 if shootout_score1 > shootout_score2 else team2
            period_reports.append("Shootout:")
            period_reports.extend(shootout_report)
            period_reports.append(
                f"The result of the shootout series: {shootout_score1}:{shootout_score2} - {winner.name} win")

    if win_type is None:
        if total_goals1 > total_goals2:
            winner = team1
            win_type = "regulation"
        else:
            winner = team2
            win_type = "regulation"

    if not is_playoff:
        if win_type == "regulation":
            if winner == team1:
                team1.wins += 1
                team2.loses += 1
            else:
                team2.wins += 1
                team1.loses += 1
        elif win_type == "ot":
            if winner == team1:
                team1.wins_ot += 1
                team2.loses_ot += 1
            else:
                team2.wins_ot += 1
                team1.loses_ot += 1
        elif win_type == "shootout":
            if winner == team1:
                team1.wins_ot += 1
                team2.loses_ot += 1
            else:
                team2.wins_ot += 1
                team1.loses_ot += 1

    for p in team1.players:
        p.games_played += 1
    for p in team2.players:
        p.games_played += 1

    team1.goals_scored += total_goals1
    team1.goals_conceded += total_goals2
    team2.goals_scored += total_goals2
    team2.goals_conceded += total_goals1

    if win_type == "regulation":
        result_text = f"{winner.name} win"
    elif win_type == "ot":
        result_text = f"{winner.name} win in overtime"
    elif win_type == "ot_playoff":
        result_text = f"{winner.name} win in playoff overtime"
    else:
        result_text = f"{winner.name} win in shootout series"

    full_report = f"{team1.name} {total_goals1} : {total_goals2} {team2.name} – {result_text}\n"
    full_report += "\n".join(period_reports)

    return {
        "winner": winner,
        "win_type": win_type,
        "score": (total_goals1, total_goals2),
        "ot_goals": (ot_goals1, ot_goals2),
        "shootout_score": (shootout_score1, shootout_score2),
        "report": full_report
    }

class League:
    def __init__(self, teams: list[Team]):
        self.teams = teams
        self.schedule = []
        self.current_match = 0

    def generate_schedule(self, rounds=4):
        self.schedule = []
        for i in range(len(self.teams)):
            for j in range(len(self.teams)):
                if i != j:
                    for _ in range(rounds):
                        self.schedule.append((self.teams[i], self.teams[j]))
        random.shuffle(self.schedule)
        self.current_match = 0

    def next_match(self) -> Optional[Tuple[Team, Team]]:
        if self.current_match < len(self.schedule):
            match = self.schedule[self.current_match]
            self.current_match += 1
            return match
        return None

    def get_standings(self):
        return sorted(self.teams, key=lambda t: (t.points, t.goals_scored - t.goals_conceded), reverse=True)

    def print_standings(self):
        lines = ["=== ТУРНИРНАЯ ТАБЛИЦА ==="]
        lines.append(f"{'Команда':<15} {'И':<3} {'В':<3} {'ВО':<3} {'П':<3} {'ПО':<3} {'О':<3} {'Ш':<5}")
        for team in self.get_standings():
            games = team.wins + team.wins_ot + team.loses + team.loses_ot
            lines.append(f"{team.name:<15} {games:<3} {team.wins:<3} {team.wins_ot:<3} {team.loses:<3} {team.loses_ot:<3} {team.points:<3} {team.goals_scored}-{team.goals_conceded}")
        return "\n".join(lines)

game_state = "menu"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if exit_rect.collidepoint(event.pos):
                    running = False
                elif play_rect.collidepoint(event.pos):
                    game_state = "game"
            elif game_state == "game":
                if exit_play_rect.collidepoint(event.pos):
                    game_state = "menu"
    if game_state == "menu":
        screen.fill((255, 255, 255))
        screen.blit(menu_image, (100, 150))
        screen.blit(button_play, (1000, 240))
        screen.blit(button_exit, (1000, 125))
    elif game_state == "game":
        screen.fill((0, 0, 0))
        screen.blit(button_play_exit, (1530, 0))

    pygame.display.update()
pygame.quit()
