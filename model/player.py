from tinydb import TinyDB


class Player:
    def __init__(self, name, surname, birth_date, sex, elo_ranking):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.sex = sex
        self.elo_ranking = elo_ranking
        self.tournament_score = None
        self.id = None

    def __repr__(self):
        return repr(
            f"id: {self.id}, "
            f"nom : {self.name} {self.surname}, "
            f"né le {self.birth_date}, "
            f"sexe : {self.sex}, "
            f"classement Elo : {self.elo_ranking}"
        )

    def modify_elo(self, new_elo):
        self.elo_ranking = new_elo
        self.save()

    def serialize(self):
        serialized_player = {
            'name': self.name,
            'surname': self.surname,
            'birth_date': self.birth_date,
            'sex': self.sex,
            'elo_ranking': self.elo_ranking,
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
        )
        return player

    @classmethod
    def get(cls, player_id):
        """
        Take id and return instance of player from the players table in db.json.
        update the player id parameter
        :param player_id:
        :return:
        """
        player = cls.deserialize(TinyDB('db.json').table('players').get(doc_id=player_id))
        player.id = player_id
        return player

    def store_in_database(self):
        return TinyDB('db.json').table('players').insert(self.serialize())

    def update_in_database(self):
        TinyDB('db.json').table('players').update(self.serialize(), doc_ids=[self.id])

    def save(self):
        if self.id is None:
            self.id = self.store_in_database()
        else:
            self.update_in_database()
