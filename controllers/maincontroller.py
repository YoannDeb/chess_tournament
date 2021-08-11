from models.tournament import Tournament
from models.player import Player
from views.views import MenuData, HomeMenuView, PlayerMenuView, ModifyPlayerMenuView, PlayerCreationMenuView, PlayerCreationConfirmationMenuView, TournamentMenuView

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
            # next_menu = self.controller()
            # if next_menu == "PlayersMenuController":
            #     next_menu = PlayersMenuController(self.players)
            # self.controller = next_menu


class HomeMenuController:
    def __init__(self, players, tournaments):
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.view = HomeMenuView(self.menu_data)

    def __call__(self):
        self.menu_data.add_entry("auto", "MENU JOUEURS : Consulter, modifier et créer les joueurs", PlayersMenuController(self.players, self.tournaments))
        self.menu_data.add_entry("auto", "MENU TOURNOIS : Consulter les tournois passés, en créer un nouveau", TournamentMenuController(self.players, self.tournaments))
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
            self.players.sort(key=lambda chess_player: chess_player.surname)
        elif self.sorting == "elo_ranking":
            self.players.sort(key=lambda player: player.elo_ranking)
            self.players.reverse()
        self.menu_data.add_header("Index, Nom, Prénom, Date de naissance, Sexe, Classement Elo")  # todo adjust headers or decide not to show them or make a real table !
        for player in self.players:
            self.menu_data.add_entry("auto", player, ModifyPlayerEloMenuController(self.players, self.tournaments, player))

        self.menu_data.add_entry("c", "Créer un joueur", PlayerCreationMenuController(self.players, self.tournaments, self.sorting))
        if self.sorting == "surname":
            self.menu_data.add_entry("e", "Classer par Elo", PlayersMenuController(self.players, self.tournaments, "elo_ranking"))
        elif self.sorting == "elo_ranking":
            self.menu_data.add_entry("a", "Classer par ordre alphabétique", PlayersMenuController(self.players, self.tournaments, "surname"))

        self.menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", self.parent_menu)

        return self.view.get_user_choice()


class PlayerCreationMenuController:
    def __init__(self, players, tournaments, sorting):
        self.players = players
        self.tournaments = tournaments
        self.sorting = sorting
        self.main_menu_data = MenuData()
        self.confirmation_menu_data = MenuData()
        self.main_view = PlayerCreationMenuView(self.main_menu_data)
        self.confirmation_view = PlayerCreationConfirmationMenuView(self.confirmation_menu_data)

    def __call__(self):
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

        player.save(DATABASE_FILE)
        self.players.append(player)

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
        self.menu_data = MenuData()
        self.view = TournamentMenuView(self.menu_data)

    def __call__(self):
        self.tournaments.sort(key=lambda chess_tournament: chess_tournament.begin_date[:2])
        self.tournaments.sort(key=lambda chess_tournament: chess_tournament.begin_date[3:5])
        self.tournaments.sort(key=lambda chess_tournament: chess_tournament.begin_date[6:])

        self.menu_data.add_header(
            "Index, Nom | Lieu | Date de début | Date de fin | Nombre de tours | "
            "Contrôle du temps | Description"
        )
        for tournament in self.tournaments:
            self.menu_data.add_entry("auto", tournament, TournamentInfoMenuController(self.players, self.tournaments, tournament))

        self.menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", HomeMenuController(self.players, self.tournaments))

        return self.view.get_user_choice()


class TournamentInfoMenuController:
    def __init__(self, players, tournaments, tournament):
        self.players = players
        self.tournaments = tournaments
        self.tournament = tournament
        self.menu_data = MenuData()

    def __call__(self):
        self.menu_data.add_header(self.tournament)
        self.menu_data.add_header("tableau des scores")
        self.menu_data.add_header("ligne 1")
        self.menu_data.add_header("ligne 2")
        self.menu_data.add_header("ligne 3")
        self.menu_data.add_header("ligne 4")
        self.menu_data.add_header("ligne 5")
        self.menu_data.add_header("ligne 6")
        self.menu_data.add_header("ligne 7")
        self.menu_data.add_header("ligne 8")

        self.menu_data.add_entry("auto", "rapport des rondes et matchs du tournoi", TournamentRoundsMenuController(self.players, self.tournaments))
        # self.menu_data.add_entry("auto", "liste des joueurs du tournoi", TournamentPlayersMenuController(self.player, self.tournaments))
        self.menu_data.add_entry("auto", "Création d'un nouveau tournoi", TournamentController(self.players, self.tournaments))
        self.menu_data.add_entry("auto", "retour au menu des tournois", TournamentMenuController(self.players, self.tournaments))


class TournamentRoundsMenuController:
    def __init__(self, players, tournaments, tournament):
        self.players = players
        self.tournaments = tournaments
        self.tournament = tournament

    def __call__(self):
        return TournamentInfoMenuController(self.players, self.tournaments, self.tournament)


class TournamentController:
    def __init__(self, players, tournaments, tournament=None):
        self.tournament = tournament

class EndScreenController:
    def __call__(self):
        print("Fermeture du programme") # déléguer à la vue
    pass