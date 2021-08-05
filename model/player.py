class Player:
    def __init__(self, name, surname, birth_date, sex, elo_ranking):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.sex = sex
        self.elo_ranking = elo_ranking
        self.tournament_score = 0

    def __repr__(self):
        return repr(
            f"{self.name} {self.surname}, "
            f"né le {self.birth_date}, "
            f"sexe : {self.sex}, "
            f"classement Elo : {self.elo_ranking}, "
            f"score dans le tournoi : {self.tournament_score}"
        )

    def modify_elo(self, new_elo):
        self.elo_ranking = new_elo

    def modify_tournament_score(self, last_match_score):
        self.tournament_score += last_match_score

    def serialize(self):
        serialized_player = {
            'name': self.name,
            'surname': self.surname,
            'birth_date': self.birth_date,
            'sex': self.sex,
            'elo_ranking': self.elo_ranking,
            'tournament_score': self.tournament_score
        }
        return serialized_player

    @classmethod
    def deserialize(cls, serialized_player):
        player = cls(
            serialized_player['name'],
            serialized_player['surname'],
            serialized_player['birth_date'],
            serialized_player['sex'],
            serialized_player['elo_ranking'],
            serialized_player['tournament_score']
        )
        return player
