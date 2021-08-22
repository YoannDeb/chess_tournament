from models.storage import Model


class Player(Model):
    def __init__(self, surname, name, birth_date, sex, elo_ranking):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.sex = sex
        self.elo_ranking = elo_ranking
        self.tournament_score = None
        self.id = None

    _table = 'players'

    def __repr__(self):
        str_elo = str(self.elo_ranking)
        if len(str_elo) < 4:
            zeros = 4 - len(str_elo)
        else:
            zeros = 0
        return str(
            f"|{self.surname.center(30)}|"
            f"{self.name.center(30)}|"
            f"{self.birth_date.center(15)}|"
            f"{self.sex.center(9)}|"
            f"{(('0' * zeros) + str_elo).center(10)}|"
        )

    def modify_elo(self, new_elo):
        self.elo_ranking = new_elo

    def serialize(self):
        serialized_player = {
            'surname': self.surname,
            'name': self.name,
            'birth_date': self.birth_date,
            'sex': self.sex,
            'elo_ranking': self.elo_ranking,
        }
        return serialized_player

    @classmethod
    def deserialize(cls, serialized_player):
        player = cls(
            serialized_player['surname'],
            serialized_player['name'],
            serialized_player['birth_date'],
            serialized_player['sex'],
            serialized_player['elo_ranking'],
        )
        return player

