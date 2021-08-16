import argparse

from controllers.main import MainController
from models.storage import change_database_file


def main():
    database_file = set_database_arg()
    if database_file:
        change_database_file(database_file)
    controller = MainController()
    controller.run()


def set_database_arg():
    parser = argparse.ArgumentParser(description="Utiliser un fichier de base de donnée différent de celui par défaut (db.json).")
    parser.add_argument("-d", "--databasefile", help="nom du fichier de base de donnée à utiliser")
    args = parser.parse_args()
    return args.databasefile


if __name__ == "__main__":
    main()
