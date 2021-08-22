"""
Module for Tournament class.
"""
from datetime import datetime

from models.round import Round
from models.player import Player
from models.storage import Model


class Tournament(Model):
    """
    Class representing a tournament.
    """
    def __init__(
            self,
            name,
            location,
            tournament_players_ids,
            time_control,
            description,
            total_round_number=4):
        """
        Init method of a tournament.
        self.begin_date is the date when the tournament is instantiated for the first time.
        :param name: Name of the tournament.
        :param location: Location of the tournament.
        :param tournament_players_ids: List of all  IDs of the players of the tournament.
        :param time_control: Time control type of the tournament.
        :param description: Descritpion of the tournament.
        :param total_round_number: Total round number of the tournament.
        """
        self.name = name
        self.location = location
        self.begin_date = datetime.now().strftime("%d/%m/%Y")
        self.end_date = None
        self.rounds = []
        self.total_round_number = total_round_number
        self.players_ids = tournament_players_ids
        self.time_control = time_control
        self.description = description
        self.id = None

    _table = 'tournaments'

    def __repr__(self):
        """
        Repr method for easier printing of a tournament informations.
        """
        if self.end_date is None:
            end_date = "En cours"
        else:
            end_date = self.end_date

        return str(
            f"|{self.name.center(35)}|"
            f"{self.location.center(15)}|"
            f"{self.begin_date.center(10)}|"
            f"{end_date.center(10)}|"
            f"{str(self.total_round_number).center(6)}|"
            f"{self.time_control.center(13)}|"
            f"{self.description.center(50)}|"
        )

    def sort_players_ids_by_rank(self):
        """
        Sort tournament players IDs list by rank in the tournament.
        If they have the same rank they will be sorted by Elo ranking.
        The ranking sorting is conserved in self.players_id list.
        """
        players = [Player.get(player_id) for player_id in self.players_ids]
        players_score = self.players_tournament_score()
        for player in players:
            player.tournament_score = players_score.pop(0)
        players.sort(key=lambda chess_player: chess_player.elo_ranking, reverse=True)
        players.sort(key=lambda chess_player: chess_player.tournament_score, reverse=True)
        self.players_ids = [player.id for player in players]

    def players_tournament_score(self):
        """
        Calculate scores of each player in the tournament.
        :return: A list with all scores in the same order than the list self.players_ids.
        """
        players_score = []
        for player_id in self.players_ids:
            score = 0
            for chess_round in self.rounds:
                for match in chess_round.matches:
                    if match[0][1] is not None:
                        if player_id == match[0][0]:
                            score += match[0][1]
                        elif player_id == match[1][0]:
                            score += match[1][1]
            players_score.append(score)
        return players_score

    def generate_first_round(self):
        """
        Creates the first Round of a tournament using pair_by_elo for the pairing.
        """
        self.rounds.append(Round("Round 1"))
        self.rounds[0].pair_by_elo(self.players_ids)

    def generate_following_round(self):
        """
        Creates a round in the tournaments which is not the first one.
        Uses pair_by_score() to pair players, on a copy of players_id
        (We don't want to mess with ordered self.players_ids).
        """
        self.rounds.append(Round(f"Round {len(self.rounds) + 1}"))
        self.rounds[-1].pair_by_score(self.players_ids.copy(), self.rounds)

    def end_tournament(self):
        """
        Change the end date for the actual date.
        """
        self.end_date = datetime.now().strftime("%d/%m/%Y")

    def serialize(self):
        """
        Serialize a tournament in a manageable form for TinyDb.
        :return: A dictionary with tournament information serialized.
        """
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
            'players_id': self.players_ids,
            'time_control': self.time_control,
            'description': self.description
        }
        return serialized_tournament

    @classmethod
    def deserialize(cls, serialized_tournament):
        """
        Take a serialized tournament and deserialize it.
        :param serialized_tournament: A dictionary with tournament information serialized.
        :return: An instance of Tournament class.
        """
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
