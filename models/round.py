from datetime import datetime


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
        for previous_round in rounds[:-1]:
            for match in previous_round.matches:
                if player1_id == match[0][0] and player2_id == match[1][0]:
                    return True
                elif player2_id == match[0][0] and player1_id == match[1][0]:
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

        list_middle = int(len(players_id) / 2)
        first_half_players = players_id[:list_middle]
        second_half_players = players_id[list_middle:]

        pairs = zip(first_half_players, second_half_players)

        for pair in pairs:
            self.matches.append(([pair[0], None], [pair[1], None]))

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
        :param players_id: copy of the list of instances of players' id in the tournament, already sorted by tournament's rank tournament.
        :param rounds: list of rounds in the tournament.
        """

        print(players_id)
        reversed_order = False
        one_of_last_matches_impossible = True
        while one_of_last_matches_impossible:
            one_of_last_matches_impossible = False
            for index in range(0, len(players_id), 2):
                if one_of_last_matches_impossible:
                    break
                input()
                index_of_player_to_switch_with = 2
                print(f"checking player in position {index} id = {players_id[index]} with player in position {index + 1} id = {players_id[index + 1]}")
                while self.check_if_previous_encounter(players_id[index], players_id[index + 1], rounds):
                    print(f"existing match detected between those two players")
                    if index + index_of_player_to_switch_with != len(players_id):
                        players_id[index + 1], players_id[index + index_of_player_to_switch_with] = players_id[index + index_of_player_to_switch_with], players_id[index + 1]
                        print(f"nouvelle liste réarrangée : {players_id}")
                        index_of_player_to_switch_with += 1
                        print(index_of_player_to_switch_with)
                    else:
                        print("no more players to pair with")
                        if index <= len(players_id) - 4:
                            players_id[index + 1], players_id[index + index_of_player_to_switch_with - 1] = players_id[index + index_of_player_to_switch_with - 1], players_id[index + 1]
                        print(f"players before reversing {players_id}")
                        players_id.reverse()
                        print(f"players after reversing {players_id}")
                        reversed_order = not reversed_order
                        one_of_last_matches_impossible = True
                        break
                print("match ok")
        if reversed_order:
            players_id.reverse
        print(f"final sorting {players_id}")
        input()

        for index in range(0, len(players_id), 2):
            self.matches.append(([players_id[index], None], [players_id[index + 1], None]))

    def register_end_time(self):
        self.end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def serialize(self):
        serialized_round = {
            'name': self.name,
            'matches': self.matches,
            'begin_time': self.begin_time,
            'end_time': self.end_time,
        }
        return serialized_round

    @classmethod
    def deserialize(cls, serialized_round):
        deserialized_matches = [(match[0], match[1]) for match in serialized_round['matches']]
        chess_round = cls(serialized_round['name'])
        chess_round.matches = deserialized_matches
        chess_round.begin_time = serialized_round['begin_time']
        chess_round.end_time = serialized_round['end_time']

        return chess_round
