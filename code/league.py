import json
import random
from typing import List, Tuple, Optional

class Player:
    def __init__(self, name: str, position: str, skill: int, price: int):
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
        return {
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
        p = Player(data["name"], data["position"], data["skill"], data["price"])
        p.games_played = data.get("games_played", 0)
        p.goals = data.get("goals", 0)
        p.assists = data.get("assists", 0)
        p.points = data.get("points", 0)
        p.saves = data.get("saves", 0)
        p.goals_against = data.get("goals_against", 0)
        p.plus_minus = data.get("plus_minus", 0)
        return p


class Team:
    def __init__(self, name: str, budget: int, tactic: str = "neutral"):
        self.name = name
        self.budget = budget
        self.tactic = tactic
        self.players: List[Player] = []
        self.wins = 0
        self.wins_ot = 0
        self.loses = 0
        self.loses_ot = 0
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0

    def add_player(self, player: Player):
        self.players.append(player)

    def to_dict(self):
        return {
            "name": self.name,
            "budget": self.budget,
            "tactic": self.tactic,
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
        team = Team(data["name"], data["budget"], data.get("tactic", "neutral"))
        for p_data in data["players"]:
            team.add_player(Player.from_dict(p_data))
        team.wins = data.get("wins", 0)
        team.wins_ot = data.get("wins_ot", 0)
        team.loses = data.get("loses", 0)
        team.loses_ot = data.get("loses_ot", 0)
        team.points = data.get("points", 0)
        team.goals_scored = data.get("goals_scored", 0)
        team.goals_conceded = data.get("goals_conceded", 0)
        return team


class League:
    def __init__(self, teams: List[Team]):
        self.teams = teams
        self.schedule_rounds: List[List[Tuple[Team, Team]]] = []
        self.current_round = 0
        self.current_match_in_round = 0
        self.user_team: Optional[Team] = None

        self.playoff_active = False
        self.playoff_rounds = []   # список раундов, каждый раунд - список [team1, team2, wins1, wins2]
        self.current_playoff_round = 0
        self.current_playoff_pair = 0
        self.regular_season_over = False

    def generate_schedule_by_rounds(self, rounds_per_pair: int = 2):
        all_matches = []
        n = len(self.teams)
        for _ in range(rounds_per_pair):
            for i in range(n):
                for j in range(n):
                    if i != j:
                        all_matches.append((self.teams[i], self.teams[j]))
        random.shuffle(all_matches)
        matches_per_round = n // 2 if n // 2 > 0 else 1
        self.schedule_rounds = [all_matches[i:i+matches_per_round] for i in range(0, len(all_matches), matches_per_round)]
        self.current_round = 0
        self.current_match_in_round = 0

    def simulate_next_user_match_and_round(self):
        from simulate_match import simulate_match_dry
        while self.current_round < len(self.schedule_rounds):
            round_matches = self.schedule_rounds[self.current_round]
            user_idx = None
            for idx, (t1, t2) in enumerate(round_matches):
                if t1.name == self.user_team.name or t2.name == self.user_team.name:
                    user_idx = idx
                    break
            if user_idx is not None:
                self.current_match_in_round = user_idx
                return round_matches[user_idx]
            else:
                for (t1, t2) in round_matches:
                    res = simulate_match_dry(t1, t2, home_team=t1)
                    g1, g2 = res["score"]
                    win_type = res["win_type"]
                    self.record_match_result(t1, t2, g1, g2, win_type)
                self.current_round += 1
        return None

    def simulate_remaining_matches_in_current_round(self):
        from simulate_match import simulate_match_dry
        if self.current_round >= len(self.schedule_rounds):
            return []
        round_matches = self.schedule_rounds[self.current_round]
        results = []
        for idx, (t1, t2) in enumerate(round_matches):
            if idx == self.current_match_in_round:
                continue
            res = simulate_match_dry(t1, t2, home_team=t1)
            g1, g2 = res["score"]
            win_type = res["win_type"]
            self.record_match_result(t1, t2, g1, g2, win_type)
            results.append((t1, t2, g1, g2, win_type))
        self.current_round += 1
        self.current_match_in_round = 0
        return results

    def record_match_result(self, team1: Team, team2: Team, goals1: int, goals2: int, win_type: str):
        if win_type == "regulation":
            if goals1 > goals2:
                team1.wins += 1
                team2.loses += 1
            else:
                team2.wins += 1
                team1.loses += 1
        elif win_type in ("ot", "shootout"):
            if goals1 > goals2:
                team1.wins_ot += 1
                team2.loses_ot += 1
            else:
                team2.wins_ot += 1
                team1.loses_ot += 1
        team1.goals_scored += goals1
        team1.goals_conceded += goals2
        team2.goals_scored += goals2
        team2.goals_conceded += goals1
        team1.points = team1.wins * 2 + team1.wins_ot
        team2.points = team2.wins * 2 + team2.wins_ot

    def get_standings(self) -> List[Team]:
        return sorted(self.teams, key=lambda t: (-t.points, t.goals_scored - t.goals_conceded))

    def generate_playoff(self):
        west_names = ["Metalurg","Avangard","Ak Bars","Avtomobilist","Salavat Yulayev",
                      "Traktor","Nephtehimik","Sibir","Admiral","Barys","Amur"]
        east_names = ["Lokomotiv","Dinamo Minsk","Dinamo Moscow","Severstal","Torpedo",
                      "Spartak","SKA","CSKA","Dragons","Lada","Sochi"]
        west_teams = [t for t in self.teams if t.name in west_names]
        east_teams = [t for t in self.teams if t.name in east_names]
        west_standings = sorted(west_teams, key=lambda t: (-t.points, t.goals_scored - t.goals_conceded))
        east_standings = sorted(east_teams, key=lambda t: (-t.points, t.goals_scored - t.goals_conceded))
        west_top8 = west_standings[:8]
        east_top8 = east_standings[:8]
        if len(west_top8) < 8 or len(east_top8) < 8:
            print("Ошибка: недостаточно команд для плей-офф")
            return
        west_quarter = [(west_top8[i], west_top8[7-i]) for i in range(4)]
        east_quarter = [(east_top8[i], east_top8[7-i]) for i in range(4)]
        # Четвертьфиналы
        quarter_pairs = []
        for pair in west_quarter + east_quarter:
            quarter_pairs.append([pair[0], pair[1], 0, 0])
        self.playoff_rounds = [quarter_pairs]
        self.current_playoff_round = 0
        self.current_playoff_pair = 0
        self.playoff_active = True
        self.regular_season_over = True

    def get_next_playoff_match(self):
        if not self.playoff_active:
            return None
        from simulate_match import simulate_match_dry

        current_round_pairs = self.playoff_rounds[self.current_playoff_round]

        # Симулируем все пары без пользователя в текущем раунде
        for idx, pair in enumerate(current_round_pairs):
            t1, t2, w1, w2 = pair
            if t1 is None or t2 is None:
                continue
            if w1 < 4 and w2 < 4 and t1.name != self.user_team.name and t2.name != self.user_team.name:
                while w1 < 4 and w2 < 4:
                    res = simulate_match_dry(t1, t2, home_team=t1)
                    g1, g2 = res["score"]
                    if g1 > g2:
                        w1 += 1
                    else:
                        w2 += 1
                current_round_pairs[idx][2] = w1
                current_round_pairs[idx][3] = w2

        # Ищем пару с пользователем
        while self.current_playoff_pair < len(current_round_pairs):
            t1, t2, w1, w2 = current_round_pairs[self.current_playoff_pair]
            if t1 is None or t2 is None:
                self.current_playoff_pair += 1
                continue
            if (t1.name == self.user_team.name or t2.name == self.user_team.name) and w1 < 4 and w2 < 4:
                return (t1, t2)
            self.current_playoff_pair += 1

        # Текущий раунд завершён – строим следующий
        winners = []
        for t1, t2, w1, w2 in current_round_pairs:
            if w1 == 4:
                winners.append(t1)
            elif w2 == 4:
                winners.append(t2)
        if len(winners) >= 2:
            next_pairs = []
            for i in range(0, len(winners), 2):
                if i+1 < len(winners):
                    next_pairs.append([winners[i], winners[i+1], 0, 0])
                else:
                    next_pairs.append([winners[i], None, 0, 0])
            self.playoff_rounds.append(next_pairs)
            self.current_playoff_round += 1
            self.current_playoff_pair = 0
            return self.get_next_playoff_match()
        else:
            self.playoff_active = False
            return None

    def record_playoff_match_result(self, team1: Team, team2: Team, goals1: int, goals2: int):
        current_round_pairs = self.playoff_rounds[self.current_playoff_round]
        for pair in current_round_pairs:
            t1, t2, w1, w2 = pair
            if (t1.name == team1.name and t2.name == team2.name) or (t1.name == team2.name and t2.name == team1.name):
                if goals1 > goals2:
                    if team1.name == t1.name:
                        pair[2] += 1
                    else:
                        pair[3] += 1
                else:
                    if team1.name == t1.name:
                        pair[3] += 1
                    else:
                        pair[2] += 1
                return
        raise ValueError("Match not found")

    def simulate_remaining_playoff_matches(self):
        from simulate_match import simulate_match_dry
        while self.playoff_active:
            match = self.get_next_playoff_match()
            if match is None:
                break
            t1, t2 = match
            w1, w2 = 0, 0
            while w1 < 4 and w2 < 4:
                res = simulate_match_dry(t1, t2, home_team=t1)
                g1, g2 = res["score"]
                if g1 > g2:
                    w1 += 1
                else:
                    w2 += 1
            # Записываем результат
            current_round_pairs = self.playoff_rounds[self.current_playoff_round]
            for pair in current_round_pairs:
                if (pair[0].name == t1.name and pair[1].name == t2.name) or (pair[0].name == t2.name and pair[1].name == t1.name):
                    pair[2] = w1
                    pair[3] = w2
                    break
            self.current_playoff_pair += 1
        self.playoff_active = False

    def start_new_season(self):
        # Сброс статистики всех команд
        for team in self.teams:
            team.wins = 0
            team.wins_ot = 0
            team.loses = 0
            team.loses_ot = 0
            team.points = 0
            team.goals_scored = 0
            team.goals_conceded = 0
        # Генерация нового расписания
        self.generate_schedule_by_rounds(rounds_per_pair=2)
        self.playoff_active = False
        self.playoff_rounds = []
        self.current_playoff_round = 0
        self.current_playoff_pair = 0
        self.regular_season_over = False

    def to_dict(self):
        return {
            "teams": [t.to_dict() for t in self.teams],
            "schedule_rounds": [[(t1.name, t2.name) for (t1, t2) in round] for round in self.schedule_rounds],
            "current_round": self.current_round,
            "current_match_in_round": self.current_match_in_round,
            "user_team_name": self.user_team.name if self.user_team else None,
            "playoff_active": self.playoff_active,
            "playoff_rounds": [[[t1.name if t1 else None, t2.name if t2 else None, w1, w2] for (t1, t2, w1, w2) in round] for round in self.playoff_rounds],
            "current_playoff_round": self.current_playoff_round,
            "current_playoff_pair": self.current_playoff_pair,
            "regular_season_over": self.regular_season_over
        }

    @staticmethod
    def from_dict(data, teams_dict: dict):
        schedule_rounds = []
        for round_data in data["schedule_rounds"]:
            round_matches = [(teams_dict[t1], teams_dict[t2]) for (t1, t2) in round_data]
            schedule_rounds.append(round_matches)
        all_teams = set()
        for r in schedule_rounds:
            for t1, t2 in r:
                all_teams.add(t1); all_teams.add(t2)
        league = League(list(all_teams))
        league.schedule_rounds = schedule_rounds
        league.current_round = data["current_round"]
        league.current_match_in_round = data["current_match_in_round"]
        if data["user_team_name"]:
            league.user_team = teams_dict[data["user_team_name"]]
        for saved_team in data["teams"]:
            team = teams_dict[saved_team["name"]]
            team.wins = saved_team["wins"]
            team.wins_ot = saved_team["wins_ot"]
            team.loses = saved_team["loses"]
            team.loses_ot = saved_team["loses_ot"]
            team.points = saved_team["points"]
            team.goals_scored = saved_team["goals_scored"]
            team.goals_conceded = saved_team["goals_conceded"]
        league.playoff_active = data.get("playoff_active", False)
        playoff_rounds = data.get("playoff_rounds", [])
        league.playoff_rounds = []
        for round_data in playoff_rounds:
            round_list = []
            for (t1_name, t2_name, w1, w2) in round_data:
                t1 = teams_dict[t1_name] if t1_name else None
                t2 = teams_dict[t2_name] if t2_name else None
                round_list.append([t1, t2, w1, w2])
            league.playoff_rounds.append(round_list)
        league.current_playoff_round = data.get("current_playoff_round", 0)
        league.current_playoff_pair = data.get("current_playoff_pair", 0)
        league.regular_season_over = data.get("regular_season_over", False)
        return league