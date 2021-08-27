"""
All storage related stuff.
"""
import os
import pathlib

from tinydb import TinyDB

DATABASE_FILE = pathlib.Path.cwd() / 'database' / 'db.json'
os.makedirs(pathlib.Path.cwd() / 'database', exist_ok=True)


class Model:
    """
    Parent class for Player and Tournament.
    Implementing all storage and recall functions from database.
    """
    def __init__(self):
        """
        Defined in each subclass.
        """
        self.id = None

    _table = None

    def serialize(self):
        """
        Defined in each subclass.
        """
        pass

    @classmethod
    def deserialize(cls, serialized_item):
        """
        Defined in each subclass.
        """
        pass

    @classmethod
    def get(cls, subclass_instance_id):
        """
        Takes id and return instance of subclass from the subclass _table in database file.
        Updates the subclass id attribute.
        :param subclass_instance_id: ID of the subclass instance.
        :return: subclass instance
        """
        subclass_instance = cls.deserialize(TinyDB(DATABASE_FILE).table(cls._table).get(doc_id=subclass_instance_id))
        subclass_instance.id = subclass_instance_id
        return subclass_instance

    @classmethod
    def get_all(cls):
        """
        Takes all items in the subclass _table, instantiate and append it to a list of all instances stored.
        :return: A list of all instances stored in database.
        """
        subclass_instances = []
        for item in TinyDB(DATABASE_FILE).table(cls._table).all():
            subclass_instance_id = item.doc_id
            subclass_instances.append(cls.get(subclass_instance_id))
        return subclass_instances

    def store_in_database(self):
        """
        Will store the instance in DATABASE_FILE.
        :return: The ID assigned by TinyDB.
        """
        return TinyDB(DATABASE_FILE).table(self._table).insert(self.serialize())

    def update_in_database(self):
        """
        Replace the data of an instance in DATABASE_FILE by the actual data of the instance.
        Localized in database with self.id.
        """
        TinyDB(DATABASE_FILE).table(self._table).update(self.serialize(), doc_ids=[self.id])

    def save(self):
        """
        Checks if an ID exists, which in fact checks if it already been stored at least once.
        Store it if no, update it if yes.
        """
        if self.id is None:
            self.id = self.store_in_database()
        else:
            self.update_in_database()


def change_database_file(database_file):
    """
    Change the DATABASE_FILE constant for the one in parameters.
    :param database_file: A new database filename.
    """
    global DATABASE_FILE
    DATABASE_FILE = pathlib.Path.cwd() / 'database' / database_file


def check_database_exists():
    """
    Checks if database_file already exists.
    :return: True if so, False if not.
    """
    try:
        with open(DATABASE_FILE):
            pass
    except IOError:
        return False
    return True
