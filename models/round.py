"""
Module for class Round.
"""
from datetime import datetime
from itertools import combinations

from models.player import Player


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

        # # make list with all (players, elo)
        # players_ids_elos = [(player_id, Player.get(player_id).elo_ranking) for player_id in players_ids]
        #
        # # make a list with all possible matches [((player1, elo), (player2, elo)), ((player1, elo), (player3, elo)),...]
        # all_possible_matches = []
        # while len(players_ids_elos) > 1:
        #     player_to_pair = players_ids_elos.pop(0)
        #     for player in players_ids_elos:
        #         all_possible_matches.append((player_to_pair, player))

        all_possible_matches = list(combinations(players_ids, 2))

        print(all_possible_matches)
        print(len(all_possible_matches))

        # remove all already played matches:
        all_possible_matches_not_played = [match for match in all_possible_matches if not self.check_if_previous_encounter(match[0], match[1], rounds)]
        # for match in all_possible_matches:
        #     if not self.check_if_previous_encounter(match[0], match[1], rounds):
        #         all_possible_matches_not_played.append(match)

        print(len(all_possible_matches_not_played))
        print(len(rounds[0].matches))
        print(len(rounds))
        print((len(rounds)-1)*(len(rounds[0].matches)))
        print(all_possible_matches_not_played)

        # trouver toutes les combinaisons de matchs possibles
        all_matches_combinations = list(combinations(all_possible_matches_not_played, int(len(players_ids)/2)))
        print(len(all_matches_combinations))

        # Sélectionner celles qui n'ont pas de doublons de joueurs:
        valid_matches_combinations = []
        for matches in all_matches_combinations:
            deserialized_matches = []
            for match in matches:
                deserialized_matches.append(match[0])
                deserialized_matches.append(match[1])
            doubles = False
            for player in players_ids:
                if not deserialized_matches.count(player) == 1:
                    doubles = True
            if not doubles:
                valid_matches_combinations.append(matches)

        print(valid_matches_combinations)

        # Ordonner les combinaisons par différence de score croissante et prendre la plus basse:

        def player_tournament_score(player_id):
            score = 0
            for chess_round in rounds:
                for match in chess_round.matches:
                    if match[0][1] is not None:
                        if player_id == match[0][0]:
                            score += match[0][1]
                        elif player_id == match[1][0]:
                            score += match[1][1]
            return score

        def match_score_diff(match):
            print(f"player1 score {player_tournament_score(match[0])}")
            print(f"player2 score {player_tournament_score(match[1])}")
            print(f"scorediff {abs(player_tournament_score(match[0]) - player_tournament_score(match[1]))}")
            print()
            return abs(player_tournament_score(match[0]) - player_tournament_score(match[1]))

        def match_score_sum(match):
            return player_tournament_score(match[0]) + player_tournament_score(match[1])

        def matches_total_score_diff(matches_list):
            return sum([match_score_diff(match) for match in matches_list])

        def match_elo_diff(match):
            return abs(Player.get(match[0]).elo_ranking - Player.get(match[1]).elo_ranking)

        def match_elo_sum(match):
            return Player.get(match[0]).elo_ranking + Player.get(match[1]).elo_ranking

        def matches_total_elo_diff(matches_list):
            return sum([match_elo_diff(match) for match in matches_list])

        print(matches_total_score_diff(valid_matches_combinations[0]))
        print(valid_matches_combinations[0])
        input()

        for n in range(0, 10):
            print(matches_total_score_diff(valid_matches_combinations[n]))
            print(valid_matches_combinations[n])

        print()

        for n in range(-10, -1):
            print(matches_total_score_diff(valid_matches_combinations[n]))
            print(valid_matches_combinations[n])

        input()
        valid_matches_combinations.sort(key=lambda x: matches_total_elo_diff(x))
        valid_matches_combinations.sort(key=lambda x: matches_total_score_diff(x))

        for n in range(0, 10):
            print(matches_total_score_diff(valid_matches_combinations[n]))
            print(matches_total_elo_diff(valid_matches_combinations[n]))
            print(valid_matches_combinations[n])

        print()

        for n in range(-10, -1):
            print(matches_total_score_diff(valid_matches_combinations[n]))
            print(matches_total_elo_diff(valid_matches_combinations[n]))
            print(valid_matches_combinations[n])

        print()
        input()

        print(valid_matches_combinations[0])

        best_combination = list(valid_matches_combinations[0])
        best_combination.sort(key=lambda x: match_elo_sum(x), reverse=True)
        best_combination.sort(key=lambda x: match_score_sum(x), reverse=True)
        for match in best_combination:
            print(match)
            print(match_score_sum(match))
            print(match_score_sum(match))
            self.matches.append(([match[0], None], [match[1], None]))

        print(self.matches)
        print(players_ids)

        # self.matches = best_combination.sort(key=lambda x: match_sum(x))
        # self.matches.sort(key=lambda x: match_sum(x))


        input()








        # print(players_ids)
        # reversed_order = False
        # one_of_last_matches_impossible = True
        # while one_of_last_matches_impossible:
        #     one_of_last_matches_impossible = False
        #     for index_of_player_to_check in range(0, len(players_ids), 2):
        #         if one_of_last_matches_impossible:
        #             break
        #         # input()
        #         relative_index_of_player_to_switch_with = 2
        #         print(f"checking {players_ids[index_of_player_to_check]} and {players_ids[index_of_player_to_check + 1]}")
        #         print(players_ids)
        #         print()
        #         # Tries to do one inversion if the match exists.
        #         while self.check_if_previous_encounter(players_ids[index_of_player_to_check], players_ids[index_of_player_to_check + 1], rounds):
        #             print(f"existing match detected between those two players {players_ids[index_of_player_to_check]} and {players_ids[index_of_player_to_check + 1]} NOK!!!")
        #             index_of_player_to_switch_with = index_of_player_to_check + relative_index_of_player_to_switch_with
        #             # Checks if the player to switch with is not the last player.
        #             if index_of_player_to_switch_with != len(players_ids):
        #                 # process with inversion
        #                 players_ids[index_of_player_to_check + 1], players_ids[index_of_player_to_switch_with] = \
        #                     players_ids[index_of_player_to_switch_with], players_ids[index_of_player_to_check + 1]
        #                 print(f"nouvelle liste réarrangée : {players_ids}")
        #                 relative_index_of_player_to_switch_with += 1
        #                 print(relative_index_of_player_to_switch_with)
        #             # The player to check is the last player, there is no player after him.
        #             else:
        #                 print("no more players to pair with")
        #                 # if index_of_player_to_check <= len(players_ids) - 4:
        #                     # replace players after in original order before reversing
        #                 players_ids.append(players_ids.pop(index_of_player_to_check + 1))
        #                     # , players_ids[-1] = players_ids[-1], players_ids[index_of_player_to_check + 1]
        #                 print(f"players before reversing {players_ids}")
        #                 players_ids.reverse()
        #                 print(f"players after reversing {players_ids}")
        #                 answer = input("test match by id ? y N >> ")
        #                 while answer == "y":
        #                     player1 = input("id 1 >> ")
        #                     player2 = input("id 2 >> ")
        #                     print(f"{self.check_if_previous_encounter(int(player1), int(player2), rounds)}")
        #                     answer = input("test another match existence? y N >> ")
        #                 reversed_order = not reversed_order
        #                 one_of_last_matches_impossible = True
        #                 break
        #
        #         print(f"match {players_ids[index_of_player_to_check]} and {players_ids[index_of_player_to_check + 1]} OK!!!")
        #         print(players_ids)
        #         print()
        # if reversed_order:
        #     players_ids.reverse()
        # print(f"final sorting {players_ids}")
        # input()
        #
        # for index_of_player_to_check in range(0, len(players_ids), 2):
        #     self.matches.append(([players_ids[index_of_player_to_check], None], [players_ids[index_of_player_to_check + 1], None]))

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
