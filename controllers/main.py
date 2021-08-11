from controllers.menu import HomeMenuController
from controllers.tournament import TournamentController
from models.tournament import Tournament
from models.player import Player

DATABASE_FILE = 'db.json'


class MainController:
    def __init__(self, database_file=DATABASE_FILE):
        self.players = []
        self.tournaments = []
        self.ongoing_tournament = None
        self.database_file = database_file
        self.controller = None

    def check_database_existence(self):
        if self.database_file:  # todo really check file
            return True
        return False

    def load_database(self):
        self.players = Player.get_all(self.database_file)
        self.tournaments = Tournament.get_all(self.database_file)

    def check_ongoing_tournament(self):
        for tournament in self.tournaments:
            if tournament.end_date is None:
                return tournament
        return None

    def run(self):
        if self.check_database_existence():
            self.load_database()

        self.ongoing_tournament = self.check_ongoing_tournament()
        if self.ongoing_tournament is not None:
            self.controller = TournamentController(self.players, self.tournaments, self.ongoing_tournament)
        else:
            self.controller = HomeMenuController(self.players, self.tournaments)

        while self.controller:
            self.controller = self.controller()

