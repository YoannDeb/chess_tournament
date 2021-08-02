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
            self.rounds.append(Round("Round 1"))
            self.rounds[0].pair_by_elo(self.tournament_players)
        else:
            self.rounds.append(Round(f"Round {self.round_count + 1}"))
            self.rounds[self.round_count].pair_by_score(self.tournament_players)
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
        # order players by elo
        # split in two lists
        for player in players[::2]:
            self.matches.append(Match(player, player))
 # make matches with the two lists

    def pair_by_score(self, players):
        pass
        # associate with swiss tournament algorithm :
        # trier par score
        # associer 1 et 2, 2 et 3
        # vérifier si match a déjà existé
        # réassocier joueurs ayant déjà joué ensemble
        # make matches


    def input_round_result(self):
        for match in self.matches:
            match.input_result()
        self.end_time = "le 12/12/12 a 12:12:12"  #current_time

    def serialize(self):
        pass

    def deserialize(self):
        pass


class Match:
    def __init__(self, player1, player2):
        self.match_data = ([player1, 0], [player2, 0])

    def __repr__(self):
        return repr(f"{self.match_data[0][0].name} {self.match_data[0][0].surname}; score : {self.match_data[0][1]} | "
                    f"{self.match_data[1][0].name} {self.match_data[1][0].surname}; score : {self.match_data[1][1]}"
                    )

    def input_scores(self):
        print(f"Match {self.match_data[0][0].name} vs {self.match_data[1][0].name}")
        self.match_data[0][1] = float(input(f"result of {self.match_data[0][0].name}"))
        self.match_data[1][1] = float(input(f"result of {self.match_data[1][0].name}"))
        self.match_data[0][0].modify_tournament_score(self.match_data[0][1])
        self.match_data[1][0].modify_tournament_score(self.match_data[1][1])


class Player:
    def __init__(self, surname, name, birth_date, sex, elo_ranking):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.sex = sex
        self.elo_ranking = elo_ranking
        self.tournament_score = 0

    def __repr__(self):
        return repr(f"{self.name} {self.surname}, né le {self.birth_date}, sexe : {self.sex}, classement Elo : {self.elo_ranking}, score dans le tournoi : {self.tournament_score}")

    def modify_elo(self, new_elo):
        self.elo_ranking = new_elo

    def modify_tournament_score(self, last_match_score):
        self.tournament_score += last_match_score


def main():
    # normalement players généré par le menu
    player1 = Player("Vachier-Lagrave", "Maxime", "12/12/12", "M", "2653")
    player2 = Player("Bacrot", "Etienne", "12/12/12", "M", "2452")
    player3 = Player("Mazetovich", "Sebastien", "12/12/12", "M", "1645")
    player4 = Player("Libizeswski", "Fabien", "12/12/12", "M", "2224")
    players = [player1, player2, player3, player4]


    tournament = Tournament("tournament1", "place1", players, "Bullet", "this is the description of tournament")

    while tournament.round_count < tournament.total_round_number:
        tournament.generate_rounds()
        print(tournament.rounds[tournament.round_count - 1].name)
        print(tournament.rounds[tournament.round_count - 1].matches[0].match_data)
        print(tournament.rounds[tournament.round_count - 1].matches[1].match_data)
        # input scores, -1 because round_count already increase in, generate rounds
        for match in tournament.rounds[tournament.round_count - 1].matches:
            match.input_scores()
            print(match)

    tournament.end_tournament()


if __name__ == "__main__":
    main()
