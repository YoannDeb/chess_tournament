class Match:
    def __init__(self, player1, player2="Unpaired"):
        self.match_data = ([player1, 0], [player2, 0])

    def __repr__(self):
        if self.match_data[1][0] != "Unpaired":
            return repr(f"{self.match_data[0][0].name} {self.match_data[0][0].surname}; score : {self.match_data[0][1]} | "
                        f"{self.match_data[1][0].name} {self.match_data[1][0].surname}; score : {self.match_data[1][1]}"
                        )
        else:
            return repr(f"{self.match_data[0][0].name} {self.match_data[0][0].surname}; score : {self.match_data[0][1]} was unpaired for this round")

    def input_scores(self):
        """
        prototype input_score menu, should just become score modification
        match_data[0] = (first player, first player's score)
        :return:
        """
        if self.match_data[1][0] != "Unpaired":
            print(f"Match {self.match_data[0][0].name} vs {self.match_data[1][0].name}")
            self.match_data[0][1] = float(input(f"result of {self.match_data[0][0].name}"))
            self.match_data[1][1] = float(input(f"result of {self.match_data[1][0].name}"))
            self.match_data[0][0].modify_tournament_score(self.match_data[0][1])
            self.match_data[1][0].modify_tournament_score(self.match_data[1][1])
        else:
            print(f"Player {self.match_data[0][0].name} {self.match_data[0][0].surname} is unpaired for this round")
            print("He will receive 1 point")
            self.match_data[0][1] = float(1)
            self.match_data[0][0].modify_tournament_score(1)

    def serialize(self):
        pass

    def deserialize(self):
        pass
