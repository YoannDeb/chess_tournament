class Tournament:
    def __index__(
            self,
            name,
            location,
            tournament_players,
            time_control,
            description,
            total_round_number=4
    ):
        self.name = name
        self.location = location
        self.begin_date = "le 12/12/12"  #current_date
        self.end_date = ""  # obligé de renseigner dans init ???
        self.rounds = []
        self.total_round_number = total_round_number
        self.round_count = 0
        self.tournament_players = tournament_players
        self.time_control = time_control
        self.description = description

    def generate_rounds(self):
        if self.round_count == 0:
            round.pair_by_elo()

            self.round_count += 1
        elif self.round_count < 4:
            Round.pair_by_score()
            self.round_number += 1

    def end_tournament(self):
        self.end_date = "le 12/12/12"  #current_date


class Round:
    def __init__(self, name, matches):
        self.name = name
        self.matches = matches
        self.begin_time = "le 12/12/12 a 12:12:12"  #current_time
        self.end_time = ""

    def pair_by_elo(self, players):
        pass
        # order players by elo
        # split in two lists
        match1 = Match(players[0], players[1])
        match2 = Match(players[2], players[3])
        self.matches = [match1, match2]  # make matches with the two lists

    def pair_by_ranking(self):
        pass
        # associate with swiss tournament algorithm
        # make matches

    def input_round_result(self):
        for match in self.matches:
            match.input_result()
        self.end_time = "le 12/12/12 a 12:12:12"  #current_time


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.result_player1 = None  #obligé de déclarer dans init ???
        self.result_player2 = None

    def input_result_player1(self):
        print(f"Match {self.player1.name} vs {self.player2.name}")
        self.result_player1 = input(f"result of {self.player1.name}")
        self.result_player2 = input(f"result of {self.player2.name}")


class Player:
    def __init__(self, surname, name, birth_date, sex, elo_ranking):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.sex = sex
        self.elo_ranking = elo_ranking

    def modify_elo(self, new_elo):
        self.elo_ranking = new_elo


def main():
    # normalement players généré par le menu
    player1 = Player("Vachier-Lagrave", "Maxime", "12/12/12", "M", "2653")
    player2 = Player("Bacrot", "Etienne", "12/12/12", "M", "2452")
    player3 = Player("Mazetovich", "Sebastien", "12/12/12", "M", "1645")
    player4 = Player("Libizeswski", "Fabien", "12/12/12", "M", "2224")
    players = [player1, player2, player3, player4]

    tournament = Tournament("tournament1", "place1", players, "Bullet", "this is the description of tournament")

    while tournament.round_count < 4:
        tournament.generate_rounds()

    tournament.end_tournament()
