from datetime import datetime

from tinydb import TinyDB, Query

from model.round import Round


class Tournament:
    def __init__(
            self,
            name,
            location,
            tournament_players,
            time_control,
            description,
            total_round_number=4):
        self.name = name
        self.location = location
        self.begin_date = datetime.now().strftime("%d/%m/%Y")
        self.end_date = None
        self.rounds = []
        self.total_round_number = total_round_number
        self.round_count = 0
        self.tournament_players = tournament_players  # todo à supprimer
        self.time_control = time_control
        self.description = description
        for player in self.tournament_players:
            player.tournament_score = 0
        #  todo check if the tournament has enough players/enough rounds at creation

    def __repr__(self):
        return repr(
            f"name : {self.name} | "
            f"location : {self.location} | "
            f"total round number : {self.total_round_number} | "
            f"tournament players : {self.tournament_players}"
        )

    def generate_rounds(self):
        if self.round_count == 0:
            self.rounds.append(Round("Round 1"))
            self.rounds[0].pair_by_elo(self.tournament_players)
        else:
            self.rounds.append(Round(f"Round {self.round_count + 1}"))
            self.rounds[self.round_count].pair_by_score(self.tournament_players, self.rounds)
        self.round_count += 1

    def end_tournament(self):
        self.end_date = datetime.now().strftime("%d/%m/%Y")

    def serialize(self):
        serialized_rounds = []
        for chess_round in self.rounds:
            serialized_rounds.append(chess_round.serialize())

        serialized_tournament = {
            'name': self.name,
            'location': self.location,
            'begin_date': self.begin_date,
            'end_date': self.end_date,
            'rounds': serialized_rounds,
            'total_round_number': self.total_round_number,
            'round_count': self.round_count,
            'tournament_players': self.tournament_players,  # todo à changer quand les joueurs ne seront plus un attribut
            'time_control': self.time_control,
            'description': self.description
        }
        return serialized_tournament

    @classmethod
    def deserialize(cls, serialized_tournament):
        deserialized_rounds = []
        for chess_round in serialized_tournament['rounds']:
            deserialized_rounds.append(Round.deserialize(chess_round))

        tournament = cls(
            serialized_tournament['name'],
            serialized_tournament['location'],
            serialized_tournament['tournament_players'],
            serialized_tournament['time_control'],
            serialized_tournament['description'],
            serialized_tournament['total_round_number']
        )
        tournament.begin_date = serialized_tournament['begin_date']
        tournament.end_date = serialized_tournament['end_date']
        tournament.rounds = deserialized_rounds
        tournament.round_count = serialized_tournament['round_count']
        return tournament
