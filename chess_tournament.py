class Tournament:
    def __init__(self, name, location, tournament_players, time_control, description, total_round_number=4):
        self.name = name
        self.location = location
        self.begin_date = "le 12/12/12"  # current_date
        self.end_date = None  # obligé de renseigner dans init ???
        self.rounds = []
        self.total_round_number = total_round_number
        self.round_count = 0
        self.tournament_players = tournament_players
        self.time_control = time_control
        self.description = description
        for player in self.tournament_players:
            player.tournament_score = 0

    def generate_rounds(self):
        if self.round_count == 0:
            round1 = Round("round1")
            round1.pair_by_elo(self.tournament_players)
        elif self.round_count == 2:
            round2 = Round("round2")
            round2.pair_by_score(self.rounds[self.round_count], self.tournament_players)
        self.round_count += 1

    def end_tournament(self):
        self.end_date = "le 12/12/12"  #current_date

    def serialize(self):
        pass

    @classmethod
    def deserialize(cls, dictionary):
        # return Tournament(dictionary[2][2])
        pass



class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.begin_time = "le 12/12/12 a 12:12:12"  #current_time
        self.end_time = ""

    def pair_by_elo(self, players):
        pass
        # order players by elo
        # split in two lists
        match1 = Match(players[0], players[1])
        match2 = Match(players[2], players[3])
        self.matches = [match1, match2]  # make matches with the two lists

    def pair_by_score(self, players):
        pass
        # associate with swiss tournament algorithm
        # make matches

    def input_round_result(self):
        for match in self.matches:
            match.input_result()
        self.end_time = "le 12/12/12 a 12:12:12"  #current_time

    def serialize:
        pass

    def deserialize:
        pass

class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = 0  #obligé de déclarer dans init ???
        self.score_player2 = 0

    def input_scores(self):
        while self.score_player1 + self.score_player2 != 1:
            print(f"Match {self.player1.name} vs {self.player2.name}")
            self.score_player1 = input(f"result of {self.player1.name}")
            self.score_player2 = input(f"result of {self.player2.name}")
        self.player1.modify_score(self.score_player1)
        self.player2.modify_score(self.score_player2)


class Player:
    def __init__(self, surname, name, birth_date, sex, elo_ranking):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.sex = sex
        self.elo_ranking = elo_ranking
        self.tournament_score = 0

    def modify_elo(self, new_elo):
        self.elo_ranking = new_elo

    def modify_score(self, last_match_score):
        self.tournament_score += last_match_score


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
        # input scores
        for match in tournament.rounds[tournament.round_count].matches:
            match.input_scores()

    tournament.end_tournament()


if __name__ == "__main__":
    main()
