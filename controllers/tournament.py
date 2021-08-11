from models.player import Player
from views.views import MenuData, CreateTournamentView, TournamentView, PlayersMenuView


DATABASE_FILE = 'db.json'

name,
            location,
            tournament_players_id,
            time_control,
            description,
            total_round_number=4):

class CreateTournament:
    def __init__(self):
        self.menu_data = MenuData()
        self.view_players = PlayersMenuView(self.menu_data)
        self.view_time_control = Time_Control_Menu_View(self.menu_data)
        self.view = CreateTournamentView(self.menu_data)

    def __call__(self):



        self.menu_data.add_query("Nom du tournoi")
        self.menu_data.add_query("Lieu")
        self.menu_data.add_query("Descritpion")
        self.menu_data.add_query("Nombre de tours")




class TournamentController:
    def __init__(self, players, tournaments, tournament=None):
        self.players = players
        self.tournaments = tournaments
        self.tournament = tournament

    def __call__(self):
        if self.tournament is None:
            self.tournament = CreateTournament()
            self.tournament.save(DATABASE_FILE)
            self.tournaments.append(self.tournament)

        self.tournament.sort_players_id_by_rank(DATABASE_FILE)
        self.tournament.generate_first_round()
        self.tournament.save(DATABASE_FILE)
        print(f"{self.tournament.rounds[-1].name} generated with following pairs :")
        for match in self.tournament.rounds[-1].matches:
            print(f"{Player.get(match[0][0], DATABASE_FILE).name} vs {Player.get(match[1][0], DATABASE_FILE).name}")
        input("press enter to input scores")
        self.tournament.rounds[-1].input_scores(DATABASE_FILE)
        self.tournament.sort_players_id_by_rank(DATABASE_FILE)
        self.tournament.save(DATABASE_FILE)

        while len(self.tournament.rounds) < self.tournament.total_round_number:
            self.tournament.generate_following_round(DATABASE_FILE)
            self.tournament.save(DATABASE_FILE)
            print(f"{self.tournament.rounds[-1].name} generated with following pairs :")
            for match in self.tournament.rounds[-1].matches:
                print(
                    f"{Player.get(match[0][0], DATABASE_FILE).name} vs {Player.get(match[1][0], DATABASE_FILE).name}")
            input("press enter to input scores")
            self.tournament.rounds[-1].input_scores(DATABASE_FILE)
            self.tournament.sort_players_id_by_rank(DATABASE_FILE)
            self.tournament.save(DATABASE_FILE)
            print("end of ", self.tournament.rounds[-1].name)
            print(self.tournament.rounds[-1].matches)
            print(self.tournament)

        self.tournament.end_tournament()
        self.tournament.save(DATABASE_FILE)

        print("tournament", self.tournament)





