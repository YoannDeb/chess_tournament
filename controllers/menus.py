"""
Controllers classes for menus.
"""
from controllers.tournament import TournamentController
from models.player import Player
from views.menus import (
    HomeMenuView, PlayersMenuView, PlayerCreationMenuView, ModifyPlayerEloMenuView,
    TournamentsMenuView, TournamentInfoMenuView, RoundsInfoMenuView, EndScreenView
)
from core.utils import MenuData
from controllers.utils import check_elo_format, check_name_format, check_date_format, get_player_tournament_scores


class HomeMenuController:
    """
    Controller for home menu, interacting particularly with HomeMenuView.
    A MenuData instance is used to transmit informations to the view.
    """
    def __init__(self, players, tournaments):
        """
        Init method.
        self.menu_data is an instance of MenuData
        self.view is an instance of HomeMenuView taking self.menu_data as parameter.
        :param players: A list of instances of all players registered in database.
        :param tournaments: A list of instances of all tournaments registered in database.
        """
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.view = HomeMenuView(self.menu_data)

    def __call__(self):
        """
        Defines informations in self.menu_data
        :return: An instance of the next controller, depending on the choice gathered by the view.
        """
        self.menu_data.add_entry("j", "MENU JOUEURS : Consulter, modifier et créer les joueurs", PlayersMenuController(self.players, self.tournaments))
        self.menu_data.add_entry("t", "MENU TOURNOIS : Consulter les tournois passés, en créer un nouveau", TournamentsMenuController(self.players, self.tournaments))
        self.menu_data.add_entry("q", "Quitter le programme (tous les changements sont automatiquement enregistrés au fur et à mesure)", EndScreenController())
        self.menu_data.add_input_message("Saisissez votre choix")

        return self.view.get_user_choice()


class PlayersMenuController:
    """
    Controller for players menu, interacting particularly with PlayersMenuView.
    A MenuData instance is used to transmit informations to the view.
    """
    def __init__(self, players, tournaments, sorting="surname"):
        """
        Init method.
        self.menu_data is an instance of MenuData
        self.view is an instance of PlayersMenuView taking self.menu_data as parameter.
        self.parent_menu is used to recall HomeMenuController.
        :param players: A list of instances of all players registered in database.
        :param tournaments: A list of instances of all tournaments registered in database.
        :param sorting: Stores the choice of sorting type of the user. Default is sorting by surname.
        """
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.view = PlayersMenuView(self.menu_data)
        self.sorting = sorting
        self.parent_menu = HomeMenuController(self.players, self.tournaments)

    def __call__(self):
        """
        Defines informations in self.menu_data.
        Sorts the players depending of the type of sorting in self.sorting.
        :return: An instance of the next controller, depending on the choice gathered by the view.
        """
        self.menu_data.add_line(f"{'################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU JOUEURS #'.center(105)}")
        self.menu_data.add_line(f"{'################'.center(105)}")
        self.menu_data.add_line("")

        if self.sorting == "surname":
            self.players.sort(key=lambda chess_player: chess_player.surname)
        elif self.sorting == "elo_ranking":
            self.players.sort(key=lambda chess_player: chess_player.elo_ranking, reverse=True)

        if len(self.players) != 0:
            self.menu_data.add_line(
                f"    |{'Nom'.center(30)}|"
                f"{'Prénom'.center(30)}|"
                f"{'Né le'.center(15)}|"
                f"{'Sexe'.center(9)}|"
                f"{'Elo'.center(10)}|"
            )
            self.menu_data.add_line(
                f"----|{'-' * 30}|"
                f"{'-' * 30}|"
                f"{'-' * 15}|"
                f"{'-' * 9}|"
                f"{'-' * 10}|"
            )
            for player in self.players:
                self.menu_data.add_entry("auto", player, ModifyPlayerEloMenuController(self.players, self.tournaments, player, self.sorting))
        else:
            self.menu_data.add_line("Pas de joueur dans la base")
        self.menu_data.add_entry("c", "Créer un joueur", PlayerCreationMenuController(self.players, self.tournaments, self.sorting))
        if self.sorting == "surname":
            self.menu_data.add_entry("e", "Classer par Elo", PlayersMenuController(self.players, self.tournaments, "elo_ranking"))
        elif self.sorting == "elo_ranking":
            self.menu_data.add_entry("a", "Classer par ordre alphabétique", PlayersMenuController(self.players, self.tournaments, "surname"))

        self.menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", self.parent_menu)
        self.menu_data.add_input_message("Saisissez le numéro d'un joueur pour modifier son Elo, "
                                         "ou choisissez une autre option")

        return self.view.get_user_choice()


class PlayerCreationMenuController:
    """
    Controller for player creation menu, interacting particularly with PlayersCreationMenuView.
    A MenuData instance is used to transmit informations to the view.
    """
    def __init__(self, players, tournaments, sorting):
        """
        Init method.
        self.menu_data is an instance of MenuData
        self.view is an instance of PlayersMenuView taking self.menu_data as parameter.
        :param players: A list of instances of all players registered in database.
        :param tournaments: A list of instances of all tournaments registered in database.
        :param sorting: Stores the choice of sorting type of the user.
                        Transmitted by PlayersMenuController.
                        Allows persistance of the choice when user goes back to players menu.
        """
        self.players = players
        self.tournaments = tournaments
        self.sorting = sorting
        self.menu_data = MenuData()
        self.view = PlayerCreationMenuView(self.menu_data)

    def __call__(self):
        """
        Defines informations in self.menu_data (lines and one query for one field).
        Inside a validation loop, stores information gathered by the view in a variable associated the the field.
        Clears data in self.menu_data.
        Repeats this for each field.
        Creates an instance of Player with informations gathered
        Saves the instance in database
        Displays a final menu where user can choose to create another player or return to players menu.
        :return: An instance of the next controller, depending on the choice gathered by the view.
        """

        # Surname query
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION JOUEUR #'.center(105)}")
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez entrer le nom de famille")
        while True:
            surname = self.view.get_user_choice()
            if check_name_format(surname):
                surname = surname.strip().capitalize()
                break
            else:
                self.menu_data.add_line(
                    f"/!\\ Nom de famille '{surname}' invalide, le nom de famille ne peut pas"
                    f" être vide et doit commencer par une lettre /!\\"
                )

        # Name query
        self.menu_data.clear_data()
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION JOUEUR #'.center(105)}")
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez entrer le prénom")
        while True:
            name = self.view.get_user_choice()
            if check_name_format(name):
                name = name.strip().capitalize()
                break
            else:
                self.menu_data.add_line(
                    f"/!\\ Prénom '{name}' invalide, le prénom ne peut pas"
                    f" être vide et doit commencer par une lettre /!\\"
                )

        # Birth date query
        self.menu_data.clear_data()
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION JOUEUR #'.center(105)}")
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez entrer la date de naissance au format JJ/MM/AAAA")
        while True:
            birth_date = self.view.get_user_choice()
            if check_date_format(birth_date):
                break
            else:
                self.menu_data.add_line(f"/!\\ Date '{birth_date}' invalide /!\\")

        # Sex query
        self.menu_data.clear_data()
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION JOUEUR #'.center(105)}")
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_entry("m", "Masculin", "M")
        self.menu_data.add_entry("f", "Féminin", "F")
        self.menu_data.add_input_message("Saisissez votre choix")
        sex = self.view.get_user_choice()

        # Elo ranking query
        self.menu_data.clear_data()
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION JOUEUR #'.center(105)}")
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez renseigner le classement Elo du joueur")
        while True:
            elo = self.view.get_user_choice()
            if check_elo_format(elo):
                break
            else:
                self.menu_data.add_line(f"/!\\ Classement Elo '{elo}' invalide /!\\")

        # Instantiation and storage
        player = Player(
            surname.capitalize(),
            name.capitalize(),
            birth_date,
            sex,
            elo,
        )
        player.save()
        self.players.append(player)

        # Final menu
        self.menu_data.clear_data()
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION JOUEUR #'.center(105)}")
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_line(player)
        self.menu_data.add_line("")
        self.menu_data.add_line("Ajouté à la base de donnée")
        self.menu_data.add_line("")
        self.menu_data.add_entry("c", "Créer un autre joueur", PlayerCreationMenuController(self.players, self.tournaments, self.sorting))
        self.menu_data.add_entry("j", "MENU JOUEURS : Consulter, modifier et créer les joueurs", PlayersMenuController(self.players, self.tournaments, self.sorting))
        self.menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", HomeMenuController(self.players, self.tournaments))
        self.menu_data.add_input_message("Saisissez votre choix")

        return self.view.get_user_choice()


class ModifyPlayerEloMenuController:
    """
    Controller for player Elo modification menu, interacting particularly with ModifyPlayerEloMenuView.
    A MenuData instance is used to transmit informations to the view.
    """
    def __init__(self, players, tournaments, player, sorting):
        """
        Init method.
        self.menu_data is an instance of MenuData
        self.view is an instance of PlayersMenuView taking self.menu_data as parameter.
        :param players: A list of instances of all players registered in database.
        :param tournaments: A list of instances of all tournaments registered in database.
        :param sorting: Stores the choice of sorting type of the user.
                Transmitted by PlayersMenuController.
                Allows persistance of the choice when user goes back to players menu.
        """
        self.players = players
        self.tournaments = tournaments
        self.player = player
        self.menu_data = MenuData()
        self.view = ModifyPlayerEloMenuView(self.menu_data)
        self.sorting = sorting

    def __call__(self):
        """
        Defines informations in self.menu_data (lines and one query for Elo field).
        Inside a validation loop, stores Elo ranking gathered by the view.
        Updates Elo ranking in the instance of the player.
        Saves the instance in database.
        :return: An instance of PlayersMenuController.
        """

        self.menu_data.add_line(f"{'##################################'.center(105)}")
        self.menu_data.add_line(f"{'# MODIFICATION DU CLASSEMENT ELO #'.center(105)}")
        self.menu_data.add_line(f"{'##################################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_line(f"{self.player.surname}, {self.player.name} | Elo actuel : {self.player.elo_ranking}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez renseigner le nouveau classement Elo du joueur")

        while True:
            new_elo = self.view.get_user_choice()
            if check_elo_format(new_elo):
                break
            else:
                self.menu_data.add_line(
                    f"/!\\ Classement Elo '{new_elo}' invalide. Merci de "
                    f"renseigner un nombre entier positif /!\\"
                )

        self.player.modify_elo(int(new_elo))
        self.player.save()

        return PlayersMenuController(self.players, self.tournaments, self.sorting)


class TournamentsMenuController:
    """
    Controller for tournaments menu, interacting particularly with TournamentsMenuView.
    A MenuData instance is used to transmit informations to the view.
    """
    def __init__(self, players, tournaments):
        """
        Init method.
        self.menu_data is an instance of MenuData
        self.view is an instance of TournamentsMenuView taking self.menu_data as parameter.
        :param players: A list of instances of all players registered in database.
        :param tournaments: A list of instances of all tournaments registered in database.
        """
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.view = TournamentsMenuView(self.menu_data)

    def __call__(self):
        """
        Sorts tournaments by ascending begin date.
        Defines informations in self.menu_data :
            - Lines of title frame and legend for the table.
            - Menu entries for each tournament.
            - Menu entries for the bottom menu (tournament creation and return to home menu).
        :return: An instance of the next controller, depending on the choice gathered by the view.
        """
        self.tournaments.sort(key=lambda chess_tournament: chess_tournament.begin_date[:2])
        self.tournaments.sort(key=lambda chess_tournament: chess_tournament.begin_date[3:5])
        self.tournaments.sort(key=lambda chess_tournament: chess_tournament.begin_date[6:])

        self.menu_data.add_line(f"{'#################'.center(150)}")
        self.menu_data.add_line(f"{'# MENU TOURNOIS #'.center(150)}")
        self.menu_data.add_line(f"{'#################'.center(150)}")
        self.menu_data.add_line("")
        if len(self.tournaments) != 0:
            self.menu_data.add_line(
                f"    |{'Nom'.center(35)}|{'Lieu'.center(15)}|{'Début'.center(10)}|"
                f"{'Fin'.center(10)}|{'Rondes'.center(6)}|"
                f"{'Cadence'.center(13)}|{'Description'.center(50)}|"
            )
            self.menu_data.add_line(
                f"----|{'-' * 35}|{'-' * 15}|{'-' * 10}|"
                f"{'-' * 10}|{'-' * 6}|"
                f"{'-' * 13}|{'-' * 50}|"
            )
            for tournament in self.tournaments:
                self.menu_data.add_entry("auto", tournament, TournamentInfoMenuController(self.players, self.tournaments, tournament))
        else:
            self.menu_data.add_line("Pas de tournoi dans la base")

        self.menu_data.add_entry("c", "Création d'un nouveau tournoi", TournamentController(self.players, self.tournaments, HomeMenuController))
        self.menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", HomeMenuController(self.players, self.tournaments))
        self.menu_data.add_input_message("Saisissez le numéro d'un tournoi pour plus d'informations sur celui-ci, ou choisissez une autre option")

        return self.view.get_user_choice()


class TournamentInfoMenuController:
    """
    Controller for tournaments info menu, interacting particularly with TournamentsInfoMenuView.
    Essentially shows a scores table.
    A MenuData instance is used to transmit informations to the view.
    """
    def __init__(self, players, tournaments, tournament, sorting="score"):
        """
        Init method.
        self.menu_data is an instance of MenuData
        self.view is an instance of PlayersMenuView taking self.menu_data as parameter.
        :param players: A list of instances of all players registered in database.
        :param tournaments: A list of instances of all tournaments registered in database.
        :param tournament: the instance of tournament detailed in this menu.
        :param sorting: Stores the choice of sorting type of the user. Default is sorting by score.
        """
        self.players = players
        self.tournaments = tournaments
        self.tournament = tournament
        self.menu_data = MenuData()
        self.view = TournamentInfoMenuView(self.menu_data)
        self.sorting = sorting

    def __call__(self):
        """
        Sorts tournaments by ascending begin date.
        Defines informations in self.menu_data :
            - Lines of title frame and legend for the table.
            - After correct sorting, lines for players in the tournament.
            - Menu entries for the bottom menu (more details, changing sorting type, menu navigation).
        :return: An instance of the next controller, depending on the choice gathered by the view.
        """
        self.menu_data.add_line(f"{'######################'.center(147)}")
        self.menu_data.add_line(f"{'# TABLEAU DES SCORES #'.center(147)}")
        self.menu_data.add_line(f"{'######################'.center(147)}")
        self.menu_data.add_line("")
        self.menu_data.add_line(
            f"|{'Nom'.center(35)}|{'Lieu'.center(15)}|{'Début'.center(10)}|"
            f"{'Fin'.center(10)}|{'Rondes'.center(6)}|"
            f"{'Cadence'.center(13)}|{'Description'.center(50)}|"
        )
        self.menu_data.add_line(
            f"|{'-' * 35}|{'-' * 15}|{'-' * 10}|"
            f"{'-' * 10}|{'-' * 6}|"
            f"{'-' * 13}|{'-' * 50}|"
        )
        self.menu_data.add_line(self.tournament)
        self.menu_data.add_line("")
        self.menu_data.add_line(f"{'*' * 147}")
        self.menu_data.add_line("")

        self.menu_data.add_line(
            f"|{'Classement'.center(12)}|"
            f"{'Nom'.center(30)}|"
            f"{'Prénom'.center(30)}|"
            f"{'Scores des matchs'.center(54)}|"
            f"{'Total'.center(15)}|"
        )
        self.menu_data.add_line(
            f"|{'-' * 12}|"
            f"{'-' * 30}|"
            f"{'-' * 30}|"
            f"{'-' * 54}|"
            f"{'-' * 15}|"
        )

        if self.sorting == "score":
            position = 0
            for player_id in self.tournament.players_ids:
                position += 1
                player = Player.get(player_id)
                player_scores = get_player_tournament_scores(player_id, self.tournament)
                self.menu_data.add_line(f"|{str(position).center(12)}|{player.surname.center(30)}|{player.name.center(30)}|{str(player_scores).center(54)}|{str(sum(player_scores)).center(15)}|")

        if self.sorting == "name":
            name_sorted_players_id = sorted(self.tournament.players_ids, key=lambda chess_player_id: Player.get(chess_player_id).surname)
            for player_id in name_sorted_players_id:
                player = Player.get(player_id)
                player_scores = get_player_tournament_scores(player_id, self.tournament)
                position = self.tournament.players_ids.index(player_id) + 1
                self.menu_data.add_line(f"|{str(position).center(12)}|{player.surname.center(30)}|{player.name.center(30)}|{str(player_scores).center(54)}|{str(sum(player_scores)).center(15)}|")

        self.menu_data.add_entry("c", "Consulter le rapport des rondes et matchs du tournoi", RoundsInfoMenuController(self.players, self.tournaments, self.tournament, self.sorting))
        if self.sorting == "score":
            self.menu_data.add_entry("a", "Classer les joueurs par ordre alphabétique", TournamentInfoMenuController(self.players, self.tournaments, self.tournament, "name"))
        elif self.sorting == "name":
            self.menu_data.add_entry("s", "Classer les joueurs par score du tournoi", TournamentInfoMenuController(self.players, self.tournaments, self.tournament, "score"))
        self.menu_data.add_entry("t", "MENU TOURNOIS : Consulter les tournois passés, en créer un nouveau", TournamentsMenuController(self.players, self.tournaments))
        self.menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", HomeMenuController(self.players, self.tournaments))
        self.menu_data.add_input_message("Saisissez votre choix")

        return self.view.get_user_choice()


class RoundsInfoMenuController:
    """
    Controller for tournament rounds info menu, interacting particularly with RoundsInfoMenuView.
    Shows every rounds matches in the tournament, with scores of each match.
    A MenuData instance is used to transmit informations to the view.
    """
    def __init__(self, players, tournaments, tournament, sorting):
        """
        Init method.
        self.menu_data is an instance of MenuData
        self.view is an instance of PlayersMenuView taking self.menu_data as parameter.
        :param players: A list of instances of all players registered in database.
        :param tournaments: A list of instances of all tournaments registered in database.
        :param tournament: the instance of tournament detailed in this menu.
        :param sorting: Stores the choice of sorting type of the user.
                Transmitted by TournamentInfoMenuController.
                Allows persistance of the choice when user goes back to tournament info menu.
        """
        self.players = players
        self.tournaments = tournaments
        self.tournament = tournament
        self.menu_data = MenuData()
        self.view = RoundsInfoMenuView(self.menu_data)
        self.sorting = sorting

    def __call__(self):
        """
        Defines informations in self.menu_data:
            - Lines of title
            - Lines of rounds name
            - For each rounds lines with matches information
            - A "pause" query which accept any entry (no choice required, will return to previous menu)
        :return: An instance of TournamentInfoMenuController
        """

        self.menu_data.add_line(f"{'####################'.center(147)}")
        self.menu_data.add_line(f"{'# RONDES ET MATCHS #'.center(147)}")
        self.menu_data.add_line(f"{'####################'.center(147)}")
        self.menu_data.add_line("")
        self.menu_data.add_line(
            f"|{'Nom'.center(35)}|{'Lieu'.center(15)}|{'Début'.center(10)}|"
            f"{'Fin'.center(10)}|{'Rondes'.center(6)}|"
            f"{'Cadence'.center(13)}|{'Description'.center(50)}|"
        )
        self.menu_data.add_line(
            f"|{'-' * 35}|{'-' * 15}|{'-' * 10}|"
            f"{'-' * 10}|{'-' * 6}|"
            f"{'-' * 13}|{'-' * 50}|"
        )
        self.menu_data.add_line(self.tournament)
        self.menu_data.add_line("")
        self.menu_data.add_line(f"{'*' * 147}")
        self.menu_data.add_line("")
        self.menu_data.add_line(f"{'-' * 93}")

        for chess_round in self.tournament.rounds:

            self.menu_data.add_line(f"{chess_round.name}")
            self.menu_data.add_line("")
            for match in chess_round.matches:
                player1 = f"{Player.get(match[0][0]).surname}, {Player.get(match[0][0]).name}"
                player2 = f"{Player.get(match[1][0]).surname}, {Player.get(match[1][0]).name}"
                score = f"({match[0][1]} - {match[1][1]})"
                self.menu_data.add_line(f"{player1.center(40)} {score.center(13)} {player2.center(40)}")
            self.menu_data.add_line(f"{'-' * 93}")

        self.menu_data.add_query("Appuyez sur Entrée pour revenir au tableau des scores du tournoi")

        self.view.get_user_choice()

        return TournamentInfoMenuController(self.players, self.tournaments, self.tournament, self.sorting)


class EndScreenController:
    """
    Controller for end screen. Interacts with EndScreenView.
    Shows an exit message and doesn't return anything.
    A MenuData instance is used to transmit informations to the view.
    """
    def __init__(self):
        """
        Init method.
        self.menu_data is an instance of MenuData
        self.view is an instance of PlayersMenuView taking self.menu_data as parameter.
        """
        self.menu_data = MenuData()
        self.view = EndScreenView(self.menu_data)

    def __call__(self):
        """
        Defines information in self.menu_data.
        Doesn't return anything so the loop in the main controller will stop.
        """
        self.menu_data.add_line("Merci d'avoir utilisé Chess Tournament")
        self.menu_data.add_line("Tous les changements ont été sauvegardés au fur et à mesure")
        self.menu_data.add_line("Fermeture du programme")

        self.view.display_menu()
