from model.round import Round


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

    def __repr__(self):
        return repr(f"name : {self.name} | location : {self.location} | total round number : {self.total_round_number} | tournament players : {self.tournament_players}")

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
