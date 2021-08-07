from datetime import datetime

from tinydb import TinyDB

from models.round import Round
from models.player import Player


class Tournament:
    def __init__(
            self,
            name,
            location,
            tournament_players_id,
            time_control,
            description,
            total_round_number=4):
        self.name = name
        self.location = location
        self.begin_date = datetime.now().strftime("%d/%m/%Y")
        self.end_date = None
        self.rounds = []
        self.total_round_number = total_round_number
        self.players_id = tournament_players_id
        # self.players_ranking = []
        self.time_control = time_control
        self.description = description
        self.id = None

    def __repr__(self):
        return repr(
            f"name : {self.name} | "
            f"location : {self.location} | "
            f"total round number : {self.total_round_number} | "
            f"tournament players : {self.get_players()}"
        )

    def get_players(self):
        return [Player.get(player_id) for player_id in self.players_id]

    # def get_players_ranking(self):
    #     return [player.elo_ranking for player in self.get_players()]

    def players_score(self):
        players_score = []
        for player_id in self.players_id:
            score = 0.0
            for chess_round in self.rounds:
                for match in chess_round.matches:
                    if None not in match:
                        if player_id == match[0][0]:
                            score += match[0][1]
                        elif player_id == match[1][0]:
                            score += match[1][1]
            players_score.append(score)
        return players_score

    def generate_first_round(self):
        self.rounds.append(Round("Round 1"))
        self.rounds[0].pair_by_elo(self.players_id)
        self.save()
        self.rounds[0].input_round_result()
        self.save()

    def generate_following_round(self):
        self.rounds.append(Round(f"Round {len(self.rounds) + 1}"))
        print(self.rounds[-1].name)
        self.rounds[-1].pair_by_score(self.players_id, self.players_score(), self.rounds)
        self.save()
        self.rounds[-1].input_round_result()
        self.save()

    def end_tournament(self):
        self.end_date = datetime.now().strftime("%d/%m/%Y")
        self.save()

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
            'players_id': self.players_id,
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
            serialized_tournament['players_id'],
            serialized_tournament['time_control'],
            serialized_tournament['description'],
            serialized_tournament['total_round_number']
        )
        tournament.begin_date = serialized_tournament['begin_date']
        tournament.end_date = serialized_tournament['end_date']
        tournament.rounds = deserialized_rounds
        return tournament

    @classmethod
    def get(cls, tournament_id):
        """
        Take id and return instance of tournament from the tournaments table in db.json.
        update the tournament id parameter
        :param tournament_id:
        :return:
        """
        tournament = cls.deserialize(TinyDB('db.json').table('tournaments').get(doc_id=tournament_id))
        tournament.id = tournament_id
        return tournament

    def store_in_database(self):
        return TinyDB('db.json').table('tournaments').insert(self.serialize())

    def update_in_database(self):
        TinyDB('db.json').table('tournaments').update(self.serialize(), doc_ids=[self.id])

    def save(self):
        if self.id is None:
            self.id = self.store_in_database()
        else:
            self.update_in_database()
