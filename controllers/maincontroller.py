from models.tournament import Tournament
from models.player import Player
from views.views import MenuData, HomeMenuView, PlayerMenuView, ModifyPlayerMenuView, PlayerCreationMenuView, PlayerCreationConfirmationMenuView


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
        self.menu_data.add_entry("auto", "MENU JOUEURS : Consulter, modifier et créer les joueurs", PlayersMenuController(self.players, self.tournament))
        self.menu_data.add_entry("auto", "MENU TOURNOIS : Consulter les tournois passés, en créer un nouveau", TournamentMenuController(self.players, self.tournament))
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
        self.menu_data.add_header("Index, Nom, Prénom, Date de naissance, Sexe, Classement Elo")  # todo adjust headers or decide not to show them or make a real table !
        for chess_player in self.players:
            self.menu_data.add_entry("auto", chess_player, ModifyPlayerEloMenuController(self.players, self.tournaments, chess_player))

        self.menu_data.add_entry("c", "Créer un joueur", PlayerCreationMenuController(self.players, self.tournaments, self.sorting))
        if self.sorting == "surname":
            self.menu_data.add_entry("e", "Classer par Elo", PlayersMenuController(self.players, self.tournaments, "elo_ranking"))
        elif self.sorting == "elo_ranking":
            self.menu_data.add_entry("a", "Classer par ordre alphabétique", PlayersMenuController(self.players, self.tournaments, "surname"))

        self.menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", self.parent_menu)

        return self.view.get_user_choice()


class PlayerCreationMenuController:
    def __init__(self, players, tournaments, sorting):
        print("debut du constructeur")
        self.players = players
        self.tournaments = tournaments
        self.sorting = sorting
        self.main_menu_data = MenuData()
        self.confirmation_menu_data = MenuData()
        self.main_view = PlayerCreationMenuView(self.main_menu_data)
        self.confirmation_view = PlayerCreationConfirmationMenuView(self.confirmation_menu_data)

    def __call__(self):
        print("debut du call")
        self.main_menu_data.add_query("Nom de famille")
        self.main_menu_data.add_query("Prénom")
        self.main_menu_data.add_query("Date de naissance")
        self.main_menu_data.add_query("Sexe")
        self.main_menu_data.add_query("Classement Elo")

        players_attributes = self.main_view.get_user_choice()

        # todo create data verification before player creation
        player = Player(
            players_attributes[0].capitalize(),
            players_attributes[1].capitalize(),
            players_attributes[2],
            players_attributes[3],
            int(players_attributes[4]),
        )
        print("after player creation")
        player.save(DATABASE_FILE)
        self.players.append(player)
        print("after player save in database")
        self.confirmation_menu_data.add_header(f"Création du joueur")
        self.confirmation_menu_data.add_header(player)
        self.confirmation_menu_data.add_header("réalisée avec succès")
        self.confirmation_menu_data.add_entry("c", "Créer un autre joueur", PlayerCreationMenuController(self.players, self.tournaments, self.sorting))
        self.confirmation_menu_data.add_entry("j", "MENU JOUEURS : Consulter, modifier et créer les joueurs", PlayersMenuController(self.players, self.tournaments, self.sorting))
        self.confirmation_menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", HomeMenuController(self.players, self.tournaments))

        return self.confirmation_view.get_user_choice()


class ModifyPlayerEloMenuController:
    def __init__(self, players, tournaments, player):
        self.players = players
        self.tournaments = tournaments
        self.player = player
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
        return HomeMenuController(self.players, self.tournaments)


class EndScreenController:
    def __call__(self):
        print("Fermeture du programme")
    pass


class TournamentController:
    def __init__(self, tournament=None):
        self.tournament = tournament
