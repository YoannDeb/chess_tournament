from datetime import datetime

from model.match import Match


class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.begin_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.end_time = ""

    @staticmethod
    def check_if_already_unpaired(player, rounds):
        """
        Check in passed rounds if the player has already been unpaired
        :param player: player to check
        :param rounds: list of instances of rounds
        :return: True if the player has already been unpaired, False if not
        """
        for index in range(0, (len(rounds) - 1)):
            if rounds[index].matches[-1].match_data[0][0] == player:
                return True
        return False

    @staticmethod
    def check_if_previous_encounter(player1, player2, rounds):
        """
        Check in passed rounds if a match between player1 and player2 already occurred
        :param player1: one player
        :param player2: another player
        :param rounds: list of instances of rounds
        :return: True if a match occurred, False if not
        """
        for index in range(0, (len(rounds) - 1)):
            for match in rounds[index].matches:
                if player1 == match.match_data[0][0] and player2 == match.match_data[1][0]:
                    return True
                elif player2 == match.match_data[0][0] and player1 == match.match_data[1][0]:
                    return True
        return False

    def pair_by_elo(self, players):
        """
        Matching for the first round of a swiss tournament, using elo ranking:
        - Order players by decreasing elo ranking, then reverse list.
        - Separate in two lists from the middle.
        - Zip the two lists.
        - Finally create the matches corresponding to the pairs.
        If the number of players is odd, the last one will be in an unpaired solo match.
        :param players: List of instances of players in the tournament.
        """
        players.sort(key=lambda player: player.elo_ranking)
        players.reverse()

        list_middle = int(len(players) / 2)
        first_half_players = players[:list_middle]
        second_half_players = players[list_middle:]

        pairs = zip(first_half_players, second_half_players)

        for pair in pairs:
            self.matches.append(Match(pair[0], pair[1]))
        if (len(players) % 2) == 1:
            self.matches.append(Match(players[-1]))

    def pair_by_score(self, players, rounds):
        """
        Matching for the second and following rounds, using current tournament score and then elo ranking:
        - Order players by decreasing elo, then order players by decreased elo ranking,
        so the equals score get classed by elo ranking , then reverse list.
        - If the number of players is odd, check if the last player has already been unpaired,
        and if so invert with the penultimate in the list,
        and repeat the process if the penultimate has also been unpaired in a previous round
        until the last player of the list has effectively not been unpaired in a previous round.
        - For each odd players, check if he has encountered the following (pair) player in a previous match.
        If so invert position of the following player and the next,
        recheck and invert with the following,
        until the original odd player hasn't already played with his follower in the list.
        - Finally create a match with each pair of player (the odd and the following player) in the list.
        If the number of players is odd, the last one will be in an unpaired solo match.
        :param players: list of instances of players in the tournament.
        :param rounds: list of rounds in the tournament.
        """
        players.sort(key=lambda player: player.elo_ranking)
        players.sort(key=lambda player: player.tournament_score)
        players.reverse()
        # todo the last player shall not be replaced by another but just not be rewarded a point if he already received a pairing-allocated bye or has already scored a forfeit win according to FIDE reglement
        if (len(players) % 2) == 1:
            index_of_player_to_switch_with = -2
            while self.check_if_already_unpaired(players[-1], rounds):
                players[-1], players[index_of_player_to_switch_with] = players[index_of_player_to_switch_with], players[-1]
                index_of_player_to_switch_with -= 1

        for index in range(0, len(players), 2):
            index_of_player_to_switch_with = 2
            if players[index] != players[-1]:
                while self.check_if_previous_encounter(players[index], players[index + 1], rounds):
                    players[index + 1], players[index + index_of_player_to_switch_with] = players[index + index_of_player_to_switch_with], players[index + 1]
                    if players[index + index_of_player_to_switch_with] == players[-1]:
                        print("no more players to pair with")
                        break
                    index_of_player_to_switch_with += 1

        for index in range(0, len(players), 2):
            if players[index] != players[-1]:
                self.matches.append(Match(players[index], players[index + 1]))
            else:
                self.matches.append(Match(players[index]))

    def input_round_result(self):
        for match in self.matches:
            match.input_scores()
        self.end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def serialize(self):
        pass

    def deserialize(self):
        pass
