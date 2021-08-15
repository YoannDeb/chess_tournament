from tinydb import TinyDB

DATABASE_FILE = 'db.json'


class Model:
    def __init__(self):
        self.id = None

    _table = None

    def serialize(self):
        pass

    @classmethod
    def deserialize(cls, serialized_item):
        pass

    @classmethod
    def get(cls, player_id):
        """
        Take id and return instance of player from the players table in database file.
        update the player id attribute
        :param player_id:
        :return:
        """
        player = cls.deserialize(TinyDB(DATABASE_FILE).table(cls._table).get(doc_id=player_id))
        player.id = player_id
        return player

    @classmethod
    def get_all(cls):
        players = []
        for player in TinyDB(DATABASE_FILE).table(cls._table).all():
            player_id = player.doc_id
            players.append(cls.get(player_id))
        return players

    def store_in_database(self):
        return TinyDB(DATABASE_FILE).table(self._table).insert(self.serialize())

    def update_in_database(self):
        TinyDB(DATABASE_FILE).table(self._table).update(self.serialize(), doc_ids=[self.id])

    def save(self):
        if self.id is None:
            self.id = self.store_in_database()
        else:
            self.update_in_database()


def check_database_exists():
    try:
        with open(DATABASE_FILE):
            pass
    except IOError:
        print("no database file")
        return False
    print("database_file exists")
    return True
