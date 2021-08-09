from ..models.tournament import Tournament
from ..models.player import Player

DATABASE_FILE = 'db.json'


class MainController:
    def __init__(self, database_file=DATABASE_FILE):
        self.players = []
        self.tournaments = []
        self.ongoing_tournament = None
        self.database_file = database_file
        self.controller = None

    def check_database_existence(self):
        if self.database_file:  # todo realy check file
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
            self.controller = HomeMenuController()

        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Consulter, modifier et renseigner les joueurs", PlayersMenuController())
        self.menu.add("auto", "Consulter et créer un ou des tournois", TournamentMenuController())
        self.menu.add("q", "Quitter le programme (tous les changements sont automatiquement enregistrés au fur et à mesure)", EndScreenController())

        user_choice = self.view.get_user_choice()

        return user_choice.manager


class PlayersMenuController:
    def __init__(self, sorting="surname"):
        self.menu = Menu()
        self.view = PlayerMenuView(self.menu)
        self.sorting = sorting
        self.parent_menu = HomeMenuController()

    def __call__(self):
        self.players.sort(key=lambda player: player.str(self.sorting))
        self.menu.add_header("Nom", "Prénom", "Classement Elo", "Date de naissance")  # todo adjust headers or decide not to show them or make a real table !
        for chess_player in self.players:
            self.menu.add("auto", chess_player, ModifyPlayerEloMenuController(chess_player))

        self.menu.add_bottom("c", "Ajouter un joueur", AddPlayerMenuController())
        self.menu.addbottom(None, "Saisissez le numéro du joueur pour le modifier", None)
        if self.sorting == "surname":
            self.menu.add_bottom("e", "Classement par Elo", PlayersMenuController("elo_ranking"))
        elif self.sorting == "elo_ranking":
            self.menu.add_bottom("a", "Classement par ordre alphabétique", PlayersMenuController("surname"))

        self.menu.add_bottom("r", "retourner au menu précédent", self.parent_menu)

        user_choice = self.view.get_user_choice()

        return user_choice.manager


class ModifyPlayerEloMenuController:
    def __init__(self, player):
        self.menu = Menu()
        self.view = ModifyPlayerEloView(self.menu)
        self.player = player

    def __call__(self):
        self.menu.show(f"Nom : {self.player.surname}, {self.player.name} | Elo actuel {self.player.elo_ranking}")
        self.menu.query("Veuillez renseigner le nouveau classement Elo du joueur")

        while True:
            new_elo = self.view.get_user_choice()
            if self.check_elo_format(new_elo):
                break
            else:
                self.menu.query("Classement Elo invalide, merci de renseigner un nombre entre 0 et 9999")

        self.player.modify_elo(new_elo)

        return PlayersMenuController()

    @staticmethod
    def check_elo_format(self, elo):
        try:
            elo = int(elo)
        except ValueError:
            return False
        else:
            return True


class TournamentMenuController:
    pass


class EndScreenController:
    pass
