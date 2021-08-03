from model.match import Match


class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.begin_time = "le 12/12/12 a 12:12:12"  #current_time
        self.end_time = ""

    def pair_by_elo(self, players):
        """
        Orders players by elo, separate in two lists from the middle, zip the two lists
        Finally create the matches corresponding to the pairs.
        :param players: instances of players
        :return:
        """
        players.sort(key=lambda player: player.elo_ranking)
        players.reverse()
        list_middle = int(len(players) / 2)
        first_half_players = players[:list_middle]
        # if (len(players) % 2) == 0:
        second_half_players = players[list_middle:]
        # else:
        #     second_half_players = players[list_middle:-1]
        #     players[-1].modify_tournament_score(1)
        #     print(players[-1])
        print(first_half_players)
        print(second_half_players)
        pairs = zip(first_half_players, second_half_players)
        # print(list(pairs))
        for pair in pairs:
            print(pair)
            self.matches.append(Match(pair[0], pair[1]))
        if (len(players) % 2) == 1:
            self.matches.append(Match(players[-1]))

    def pair_by_score(self, players):
        players.sort(key=lambda player: player.elo_ranking)
        players.sort(key=lambda player: player.tournament_score)
        players.reverse()  # todo check if match already exists and handle odd players number
        for index in range(0, len(players), 2):
            if players[index] != players[-1]:
                self.matches.append(Match(players[index], players[index + 1]))
            else:
                self.matches.append(Match(players[index]))
        # todo verifier que le match n'existe pas déjà
        # todo corriger la liste si c'est le cas
        # associate with swiss tournament algorithm :
        # associer 1 et 2, 2 et 3
        # vérifier si match a déjà existé
        # réassocier joueurs ayant déjà joué ensemble
        # make matches

    def input_round_result(self):
        for match in self.matches:
            match.input_scores()
        self.end_time = "le 12/12/12 a 12:12:12"  #current_time

    def serialize(self):
        pass

    def deserialize(self):
        pass
