"""
Main controller module.
"""
from controllers.menus import HomeMenuController
from controllers.tournament import TournamentController
from models.tournament import Tournament
from models.storage import check_database_exists
from models.player import Player


class MainController:
    """
    Main loop controller.
    - Checks database existence.
    - Load data if exists.
    - Check if there is an unfinished tournament.
    - Launch TournamentController if so.
    - Launch HomeMenuController if not.
    """
    def __init__(self):
        """
        Init method of the main controller.
        - self.players: A list of instances of all players from the database.
        - self.tournaments: A list of instances of all tournaments from the database.
        - self.ongoing_tournament: An instance of unfinished tournament if found at the start in database.
        - self.controller: the controller "loaded" in the loop.
        """
        self.players = []
        self.tournaments = []
        self.ongoing_tournament = None
        self.controller = None

    def load_database(self):
        """
        Retrieve all datas in database file and write them in self.players and self.tournaments
        """
        self.players = Player.get_all()
        self.tournaments = Tournament.get_all()

    def retrieve_ongoing_tournament(self):
        """
        Checks if there is an unfinished tournament in self.tournaments.
        :return The unfinished tournament if found, else None.
        """
        for tournament in self.tournaments:
            if tournament.end_date is None:
                return tournament
        return None

    def run(self):
        """
        - Checks database existence.
        - Load data if exists.
        - Check if there is an unfinished tournament.
        - "Loads" TournamentController if so.
        - "Loads" HomeMenuController if not.
        - Launch the loop with "loaded" controller.
        """
        if check_database_exists():
            self.load_database()
            self.ongoing_tournament = self.retrieve_ongoing_tournament()
        if self.ongoing_tournament is not None:
            self.controller = TournamentController(
                self.players, self.tournaments,
                HomeMenuController, self.ongoing_tournament
            )
        else:
            self.controller = HomeMenuController(self.players, self.tournaments)

        while self.controller:
            self.controller = self.controller()
