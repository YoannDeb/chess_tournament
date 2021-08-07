from datetime import datetime

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
        players = [Player.get(player_id) for player_id in players_id]
        players.sort(key=lambda player: player.elo_ranking)
        players.reverse()

        list_middle = int(len(players) / 2)
        first_half_players = players[:list_middle]
        second_half_players = players[list_middle:]

        pairs = zip(first_half_players, second_half_players)

        for pair in pairs:
            self.matches.append(([pair[0].id, None], [pair[1].id, None]))

    def pair_by_score(self, players_id, players_score, rounds):
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
        :param players_score: list of players' score in tournament
        :param rounds: list of rounds in the tournament.
        """
        players = [Player.get(player_id) for player_id in players_id]
        for item in players:
            item.tournament_score = players_score.pop(0)
        players.sort(key=lambda player: player.elo_ranking)
        players.sort(key=lambda player: player.tournament_score)
        players.reverse()
        sorted_players_id = [player.id for player in players]

        print(sorted_players_id)
        last_players_not_pairable = False
        for index in range(0, len(sorted_players_id), 2):
            if last_players_not_pairable:
                break
            index_of_player_to_switch_with = 2
            print(f"checking player in position {index} id = {sorted_players_id[index]} with player in position {index + 1} id = {sorted_players_id[index + 1]}")
            while self.check_if_previous_encounter(sorted_players_id[index], sorted_players_id[index + 1], rounds):
                print(f"existing match detected between those two players")
                if index + index_of_player_to_switch_with == len(sorted_players_id):
                    print("no more players to pair with")
                    if index <= len(sorted_players_id) - 4:
                        sorted_players_id[index + 1], sorted_players_id[index + index_of_player_to_switch_with - 1] = sorted_players_id[index + index_of_player_to_switch_with - 1], sorted_players_id[index + 1]
                    last_players_not_pairable = True
                    print(f"players before rearangement {sorted_players_id}")
                    break
                sorted_players_id[index + 1], sorted_players_id[index + index_of_player_to_switch_with] = sorted_players_id[index + index_of_player_to_switch_with], sorted_players_id[index + 1]
                print(f"nouvelle liste réarrangée : {sorted_players_id}")
                index_of_player_to_switch_with += 1
                print(index_of_player_to_switch_with)
            print("match ok")
        print(f"final sorting {sorted_players_id}")

        if last_players_not_pairable:
            print("reversing list for last players")
            sorted_players_id.reverse()
            for index in range(0, len(sorted_players_id), 2):
                index_of_player_to_switch_with = 2
                print(f"checking player in position {index} id = {sorted_players_id[index]} with player in position {index + 1} id = {sorted_players_id[index + 1]}")
                while self.check_if_previous_encounter(sorted_players_id[index], sorted_players_id[index + 1], rounds):
                    print(f"existing match detected between those two players")
                    sorted_players_id[index + 1], sorted_players_id[index + index_of_player_to_switch_with] = sorted_players_id[index + index_of_player_to_switch_with], sorted_players_id[index + 1]
                    print(f"nouvelle liste réarrangée : {sorted_players_id}")
                    index_of_player_to_switch_with += 1
                    print(index_of_player_to_switch_with)
                print("match ok")
            print(f"final reverse sorting {sorted_players_id}")
            sorted_players_id.reverse()
            print(f"final in order sorting {sorted_players_id}")

        for index in range(0, len(sorted_players_id), 2):
            self.matches.append(([sorted_players_id[index], None], [sorted_players_id[index + 1], None]))

    def input_round_result(self):
        """ à modifier quand plus d'input dans le test"""
        for match in self.matches:
            player1_name = Player.get(match[0][0]).name
            player2_name = Player.get(match[1][0]).name
            print(f"Match {player1_name} vs {player2_name}")
            match[0][1] = float(input(f"result of {player1_name}"))
            match[1][1] = float(input(f"result of {player2_name}"))
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
