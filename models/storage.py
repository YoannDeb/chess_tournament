from tinydb import TinyDB
from abc import ABC, abstractmethod


class Storage:
    @classmethod
    def get(cls, player_id, database_file):
        """
        Take id and return instance of player from the players table in database file.
        update the player id parameter
        :param player_id:
        :param database_file:
        :return:
        """
        player = cls.deserialize(TinyDB(database_file).table('players').get(doc_id=player_id))
        player.id = player_id
        return player

    @classmethod
    def get_all(cls, database_file):
        players = []
        for player in TinyDB(database_file).table('players').all():
            player_id = player.doc_id
            players.append(cls.get(player_id, database_file))
        return players

    def store_in_database(self, database_file):
        return TinyDB(database_file).table('players').insert(self.serialize())

    def update_in_database(self, database_file):
        TinyDB(database_file).table('players').update(self.serialize(), doc_ids=[self.id])

    def save(self, database_file):
        if self.id is None:
            self.id = self.store_in_database(database_file)
        else:
            self.update_in_database(database_file)