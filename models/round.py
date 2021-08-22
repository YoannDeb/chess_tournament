"""
Module for class Round.
"""
from datetime import datetime


class Round:
    """
    Class representing a Round.
    """
    def __init__(self, name):
        """
        Init method of a round.
        Matches are stored as a list of tuples :
        - Each tuple is a match composed of two lists.
        - Each list contains two elements: A players' ID and it's score.
        begin_time is the date and time at the first instantiation of the round.
        :param name: Name of the round.
        """
        self.name = name
        self.matches = []
        self.begin_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.end_time = ""

    @staticmethod
    def check_if_previous_encounter(player1_id, player2_id, rounds):
        """
        Check in passed rounds if a match between player1 and player2 already occurred.
        :param player1_id: One player's id.
        :param player2_id: Another player's id.
        :param rounds: List of instances of rounds.
        :return: True if a match occurred, False if not.
        """
        for previous_round in rounds[:-1]:
            for match in previous_round.matches:
                if player1_id == match[0][0] and player2_id == match[1][0]:
                    return True
                elif player2_id == match[0][0] and player1_id == match[1][0]:
                    return True
        return False

    def pair_by_elo(self, players_ids):
        """
        Match making for the first round of a swiss tournament, using elo ranking:
        - Order players by ascending elo ranking.
        - Separate in two lists from the middle.
        - Zip the two lists.
        - Finally creates the matches corresponding to the pairs.
        :param players_ids: List of players' id in the tournament.
        """

        list_middle = int(len(players_ids) / 2)
        first_half_players = players_ids[:list_middle]
        second_half_players = players_ids[list_middle:]

        pairs = zip(first_half_players, second_half_players)

        for pair in pairs:
            self.matches.append(([pair[0], None], [pair[1], None]))

    def pair_by_score(self, players_ids, rounds):
        """
        Match making for the second and following rounds, using current tournament score and then elo ranking:
        - For each odd players, check if he has encountered the following (pair) player in a previous match.
        If so invert position of the following player and the next, recheck and invert with the following,
        until the original odd player hasn't already played with his follower in the list.
        - If one player has already played with all remaining players in the list, reverses the list and
        repeat the process until the list is valid (no match have been already played).
        If the list is in reversed status, inverses it one last time.
        - Finally create a match with each pair of player (the odd and the following player) in the list.
        :param players_ids: A copy of the list of instances of players' IDs in the tournament, already sorted
         by tournament's rank.
        :param rounds: A list of instances of rounds in the tournament.
        """

        print(players_ids)
        reversed_order = False
        one_of_last_matches_impossible = True
        while one_of_last_matches_impossible:
            one_of_last_matches_impossible = False
            for index in range(0, len(players_ids), 2):
                if one_of_last_matches_impossible:
                    break
                # input()
                index_of_player_to_switch_with = 2
                print(f"checking player in position {index} id = {players_ids[index]} with player in position {index + 1} id = {players_ids[index + 1]}")
                while self.check_if_previous_encounter(players_ids[index], players_ids[index + 1], rounds):
                    print(f"existing match detected between those two players")
                    if index + index_of_player_to_switch_with != len(players_ids):
                        players_ids[index + 1], players_ids[index + index_of_player_to_switch_with] = players_ids[index + index_of_player_to_switch_with], players_ids[index + 1]
                        print(f"nouvelle liste réarrangée : {players_ids}")
                        index_of_player_to_switch_with += 1
                        print(index_of_player_to_switch_with)
                    else:
                        print("no more players to pair with")
                        if index <= len(players_ids) - 4:
                            players_ids[index + 1], players_ids[index + index_of_player_to_switch_with - 1] = players_ids[index + index_of_player_to_switch_with - 1], players_ids[index + 1]
                        print(f"players before reversing {players_ids}")
                        players_ids.reverse()
                        print(f"players after reversing {players_ids}")
                        reversed_order = not reversed_order
                        one_of_last_matches_impossible = True
                        break
                print("match ok")
        if reversed_order:
            players_ids.reverse()
        print(f"final sorting {players_ids}")
        # input()

        for index in range(0, len(players_ids), 2):
            self.matches.append(([players_ids[index], None], [players_ids[index + 1], None]))

    def register_end_time(self):
        """
        Change the end time for the actual date and time
        :return:
        """
        self.end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def normalize_score_signifiance(self):
        """
        All score will be the same signifiance. (ex : 2.5, 3.0, 1.0 etc.)
        """
        for match in self.matches:
            match[0][1] += 0.0
            match[1][1] += 0.0

    def serialize(self):
        """
        Serialize a round in a manageable form for TinyDb.
        :return: A dictionary with round information serialized.
        """
        serialized_round = {
            'name': self.name,
            'matches': self.matches,
            'begin_time': self.begin_time,
            'end_time': self.end_time,
        }
        return serialized_round

    @classmethod
    def deserialize(cls, serialized_round):
        """
        Take a serialized round and deserialize it.
        :param serialized_round: A dictionary with round information serialized.
        :return: An instance of Round class.
        """
        deserialized_matches = [(match[0], match[1]) for match in serialized_round['matches']]
        chess_round = cls(serialized_round['name'])
        chess_round.matches = deserialized_matches
        chess_round.begin_time = serialized_round['begin_time']
        chess_round.end_time = serialized_round['end_time']

        return chess_round
