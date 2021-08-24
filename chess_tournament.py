import argparse

from controllers.main import MainController
from models.storage import change_database_file


def main():
    """
    Main function.
    Checks if database argument was given.
    If so changes database file in models.storage.
    Finally instantiate a MainController object and launches run method.
    """
    database_file = set_database_arg()
    if database_file:
        change_database_file(database_file)

    controller = MainController()
    controller.run()


def set_database_arg():
    """
    Initiate argparser argument "--databasefile" to change database file name.
    :return: The new database's filename, or None if no argument were given.
    """
    parser = argparse.ArgumentParser(
        description="Utiliser un fichier de base de donnée différent de celui par défaut (db.json)."
    )
    parser.add_argument("-d", "--databasefile", help="nom du fichier de base de donnée à utiliser")
    args = parser.parse_args()
    return args.databasefile


if __name__ == "__main__":
    main()
