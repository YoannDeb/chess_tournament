from models.storage import Model


class Player(Model):
    def __init__(self, surname, name, birth_date, sex, elo_ranking):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.sex = sex
        self.elo_ranking = int(elo_ranking)
        self.tournament_score = None
        self.id = None

    _table = 'players'

    def __repr__(self):
        return str(
            f"|{self.surname.center(30)}|"
            f"{self.name.center(30)}|"
            f"{self.birth_date.center(15)}|"
            f"{self.sex.center(9)}|"
            f"{str(self.elo_ranking).center(10)}|"
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

    # @classmethod
    # def get(cls, player_id):
    #     """
    #     Take id and return instance of player from the players table in database file.
    #     update the player id attribute
    #     :param player_id:
    #     :return:
    #     """
    #     player = cls.deserialize(TinyDB(DATABASE_FILE).table(cls._table).get(doc_id=player_id))
    #     player.id = player_id
    #     return player
    #
    # @classmethod
    # def get_all(cls):
    #     players = []
    #     for player in TinyDB(DATABASE_FILE).table(cls._table).all():
    #         player_id = player.doc_id
    #         players.append(cls.get(player_id))
    #     return players
    #
    # def store_in_database(self):
    #     return TinyDB(DATABASE_FILE).table(self._table).insert(self.serialize())
    #
    # def update_in_database(self):
    #     TinyDB(DATABASE_FILE).table(self._table).update(self.serialize(), doc_ids=[self.id])
    #
    # def save(self):
    #     if self.id is None:
    #         self.id = self.store_in_database()
    #     else:
    #         self.update_in_database()
