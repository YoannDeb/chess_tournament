from models.tournament import Tournament
from models.player import Player
from views.views import MenuData, HomeMenuView, PlayerMenuView, ModifyPlayerMenuView


DATABASE_FILE = 'db.json'
# players = []
# tournaments = []


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
            self.controller = TournamentController(self.ongoing_tournament)
        else:
            self.controller = HomeMenuController(self.players, self.tournaments)

        while self.controller:
            self.controller = self.controller()
            # next_menu = self.controller()
            # if next_menu == "PlayersMenuController":
            #     next_menu = PlayersMenuController(self.players)
            # self.controller = next_menu


class HomeMenuController:
    def __init__(self, players, tournament):
        self.players = players
        self.tournament = tournament
        self.menu_data = MenuData()
        self.view = HomeMenuView(self.menu_data)

    def __call__(self):
        self.menu_data.add_entry("auto", "Consulter modifier et renseigner les joueurs", PlayersMenuController(self.players, self.tournament))
        self.menu_data.add_entry("auto", "Consulter les tournois passés, en créer un nouveau", TournamentMenuController(self.players, self.tournament))
        self.menu_data.add_entry("q", "Quitter le programme (tous les changements sont automatiquement enregistrés au fur et à mesure)", EndScreenController())

        return self.view.get_user_choice()


class PlayersMenuController:
    def __init__(self, players, tournaments, sorting="surname"):
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.view = PlayerMenuView(self.menu_data)
        self.sorting = sorting
        self.parent_menu = HomeMenuController(self.players, self.tournaments)

    def __call__(self):
        if self.sorting == "surname":
            self.players.sort(key=lambda player: player.surname)
        elif self.sorting == "elo_ranking":
            self.players.sort(key=lambda player: player.elo_ranking)
            self.players.reverse()
#        self.menu.add_header("Nom", "Prénom", "Classement Elo", "Date de naissance")  # todo adjust headers or decide not to show them or make a real table !
        for chess_player in self.players:
            self.menu_data.add_entry("auto", chess_player, ModifyPlayerEloMenuController(self.players, self.tournaments, chess_player))

        self.menu_data.add_entry("c", "Ajouter un joueur", CreatePlayerMenuController(self.players, self.tournaments))
        self.menu_data.add_entry(None, "Saisissez le numéro du joueur pour le modifier", None)
        if self.sorting == "surname":
            self.menu_data.add_entry("e", "Classement par Elo", PlayersMenuController(self.players, self.tournaments, "elo_ranking"))
        elif self.sorting == "elo_ranking":
            self.menu_data.add_entry("a", "Classement par ordre alphabétique", PlayersMenuController(self.players, self.tournaments, "surname"))

        self.menu_data.add_entry("r", "retourner au menu précédent", self.parent_menu)

        return self.view.get_user_choice()


class CreatePlayerMenuController:
    def __init__(self, players, tournaments):
        self.players = players
        self.tournaments = tournaments

    def __call__(self):
        print("dans le menu création joueur")
        return HomeMenuController()


class ModifyPlayerEloMenuController:
    def __init__(self, players, tournaments, player):
        self.players = players
        self.tournaments = tournaments
        self.player = player
        print(player)
        self.menu_data = MenuData()
        self.view = ModifyPlayerMenuView(self.menu_data)

    def __call__(self):
        self.menu_data.add_header(f"Nom : {self.player.surname}, {self.player.name} | Elo actuel {self.player.elo_ranking}")
        self.menu_data.add_query("Veuillez renseigner le nouveau classement Elo du joueur")

        while True:
            new_elo = self.view.get_user_choice()
            if self.check_elo_format(new_elo):
                break
            else:
                self.menu_data.queries[0] = "Classement Elo invalide. Merci de renseigner un nombre entier positif"

        self.player.modify_elo(int(new_elo))
        self.player.save(DATABASE_FILE)

        return PlayersMenuController(self.players, self.tournaments)

    @staticmethod
    def check_elo_format(elo):
        try:
            elo = int(elo)
        except ValueError:
            return False
        if elo < 0:
            return False
        else:
            return True


class TournamentMenuController:
    def __init__(self, players, tournaments):
        self.players = players
        self.tournaments = tournaments

    def __call__(self):
        print("dans le tournoi")
        return HomeMenuController()


class EndScreenController:
    def __call__(self):
        print("Fermeture du programme")
    pass


class TournamentController:
    def __init__(self, tournament=None):
        self.tournament = tournament
