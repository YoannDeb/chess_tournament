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
        # self.players_elo_ranking = []
        self.time_control = time_control
        self.description = description
        self.id = None

    def __repr__(self):
        return repr(
            f"Nom : {self.name} | "
            f"Lieu : {self.location} | "
            f"Date de début : {self.begin_date} | "
            f"Date de fin : {self.end_date} |"
            f"Nombre de Rounds : {self.total_round_number} | "
            f"Contrôle du temps : {self.time_control} | "
            f"Description : {self.description}"
        )

    def get_players(self, database_file):
        return [Player.get(player_id, database_file) for player_id in self.players_id]

    # def get_players_elo_ranking(self):
    #     return [player.elo_ranking for player in self.get_players()]

    def players_tournament_score(self):
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

    def generate_first_round(self, database_file):
        self.rounds.append(Round("Round 1"))
        self.rounds[0].pair_by_elo(self.players_id, database_file)
        self.save(database_file)
        self.rounds[0].input_round_results(database_file)
        self.save(database_file)

    def generate_following_round(self, database_file):
        self.rounds.append(Round(f"Round {len(self.rounds) + 1}"))
        print(self.rounds[-1].name)
        self.rounds[-1].pair_by_score(self.players_id, self.players_tournament_score(), self.rounds, database_file)
        self.save(database_file)
        self.rounds[-1].input_round_results(database_file)
        self.save(database_file)

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
    def get(cls, tournament_id, database_file):
        """
        Take id and return instance of tournamnent from the tournaments table in database file.
        update the tournament id attribute
        :param tournament_id: id of the tournament in the database
        :param database_file: database file in json format
        :return: instance of tournament as in database
        """
        tournament = cls.deserialize(TinyDB(database_file).table('tournaments').get(doc_id=tournament_id))
        tournament.id = tournament_id
        return tournament

    @classmethod
    def get_all(cls, database_file):
        tournaments = []
        print("TinyDB(database_file).table('tournaments').all()", TinyDB(database_file).table('tournaments').all())
        for tournament in TinyDB(database_file).table('tournaments').all():
            tournament_id = tournament.doc_id
            tournaments.append(cls.get(tournament_id, database_file))
            print(f"get_all{tournaments}")
        return tournaments

    def store_in_database(self, database_file):
        return TinyDB(database_file).table('tournaments').insert(self.serialize())

    def update_in_database(self, database_file):
        TinyDB(database_file).table('tournaments').update(self.serialize(), doc_ids=[self.id])

    def save(self, database_file):
        if self.id is None:
            self.id = self.store_in_database(database_file)
        else:
            self.update_in_database(database_file)
