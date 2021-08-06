from datetime import datetime

from model.match import Match
from model.player import Player


class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.begin_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.end_time = ""

    @staticmethod
    def check_if_previous_encounter(player1_id, player2_id, rounds):
        """
        Check in passed rounds if a match between player1 and player2 already occurred
        :param player1_id: one player
        :param player2_id: another player
        :param rounds: list of instances of rounds
        :return: True if a match occurred, False if not
        """
        for index in range(0, (len(rounds) - 1)):
            for match in rounds[index].matches:
                if player1_id == match.match_data[0][0] and player2_id == match.match_data[1][0]:
                    return True
                elif player2_id == match.match_data[0][0] and player1_id == match.match_data[1][0]:
                    return True
        return False

    def pair_by_elo(self, players_id):
        """
        Matching for the first round of a swiss tournament, using elo ranking:
        - Order players by decreasing elo ranking, then reverse list.
        - Separate in two lists from the middle.
        - Zip the two lists.
        - Finally create the matches corresponding to the pairs.
        If the number of players is odd, the last one will be in an unpaired solo match.
        :param players_id: List of players' id in the tournament.
        """
        players = [Player.get(player_id) for player_id in players_id]
        players.sort(key=lambda player: player.elo_ranking)
        players.reverse()

        list_middle = int(len(players) / 2)
        first_half_players = players[:list_middle]
        second_half_players = players[list_middle:]

        pairs = zip(first_half_players, second_half_players)

        for pair in pairs:
            self.matches.append(Match(pair[0].id, pair[1].id))

    def pair_by_score(self, players_id, rounds):
        """
        Matching for the second and following rounds, using current tournament score and then elo ranking:
        - Order players by decreasing elo, then order players by decreased elo ranking,
        so the equals score get classed by elo ranking , then reverse list.
        - For each odd players, check if he has encountered the following (pair) player in a previous match.
        If so invert position of the following player and the next,
        recheck and invert with the following,
        until the original odd player hasn't already played with his follower in the list.
        - Finally create a match with each pair of player (the odd and the following player) in the list.
        If the number of players is odd, the last one will be in an unpaired solo match.
        :param players_id: list of instances of players' id in the tournament.
        :param rounds: list of rounds in the tournament.
        """
        players = [Player.get(player_id) for player_id in players_id]
        players.sort(key=lambda player: player.elo_ranking)
        players.sort(key=lambda player: player.tournament_score)
        players.reverse()

        for index in range(0, len(players), 2):
            index_of_player_to_switch_with = 2
            while self.check_if_previous_encounter(players[index], players[index + 1], rounds):
                players[index + 1], players[index + index_of_player_to_switch_with] = players[index + index_of_player_to_switch_with], players[index + 1]
                # todo manage if no match possible with all the following players
                if players[index + index_of_player_to_switch_with] == players[-1]:
                    print("no more players to pair with")
                    break
                index_of_player_to_switch_with += 1

        for index in range(0, len(players), 2):
            self.matches.append(Match(players[index].id, players[index + 1].id))

    def input_round_result(self):
        for match in self.matches:
            match.input_scores()
        self.end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def serialize(self):
        serialized_matches = []
        for match in self.matches:
            serialized_matches.append(match.serialize())

        serialized_round = {
            'name': self.name,
            'matches': serialized_matches,
            'begin_time': self.begin_time,
            'end_time': self.end_time,
        }
        return serialized_round

    @classmethod
    def deserialize(cls, serialized_round):
        deserialized_matches = []
        for match in serialized_round['matches']:
            deserialized_matches.append(Match.deserialize(match))

        chess_round = cls(serialized_round['name'])
        chess_round.matches = deserialized_matches
        chess_round.begin_time = serialized_round['begin_time']
        chess_round.end_time = serialized_round['end_time']

        return chess_round
