from model.player import Player


class Match:
    def __init__(self, player1_id, player2_id):
        self.match_data = ([player1_id, None], [player2_id, None])
        self.player1 = Player.get(player1_id)
        self.player2 = Player.get(player2_id)

    def __repr__(self):
        return repr(f"player 1: {self.player1.name} {self.player1.surname} ; "
                    f"score: {self.match_data[0][1]} | "
                    f"player 2: {self.player2.name} {self.player2.surname} ; "
                    f"score: {self.match_data[1][1]}"
                    )

    def input_scores(self):
        """
        prototype input_score menu, should just become score modification
        match_data[0] = [player1_id, player1 score]
        :return:
        """
        print(f"Match {self.player1.name} vs {self.player2.name}")
        self.match_data[0][1] = float(input(f"result of {self.player1.name}"))
        self.match_data[1][1] = float(input(f"result of {self.player2.name}"))
        self.player1.modify_tournament_score(self.match_data[0][1])
        self.player2.modify_tournament_score(self.match_data[1][1])

    def serialize(self):
        print(self.match_data)
        return {'match_data': self.match_data}

    @classmethod
    def deserialize(cls, serialized_match):
        print(serialized_match)
        print(serialized_match['match_data'])
        match = cls(
            serialized_match['match_data'][0][0],
            serialized_match['match_data'][1][0],
        )
        match.match_data[0][1] = serialized_match['match_data'][0][1]
        match.match_data[1][1] = serialized_match['match_data'][1][1]
