from models.tournament import Tournament

class TournamentController:
    def __init__(self, players, tournaments, tournament=None):
        self.players = players
        self.tournament = tournament
        self.tournament = tournament

    def __call__(self):
        if self.tournament is None:
            self.tournament = Tournament()




