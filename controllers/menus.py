from controllers.tournament import TournamentController
from models.player import Player
from views.menus import (
    HomeMenuView, PlayersMenuView, PlayerCreationMenuView, ModifyPlayerMenuView,
    TournamentMenuView, TournamentInfoMenuView, TournamentRoundsMenuView, EndScreenView
)
from core.utils import MenuData, get_player_tournament_scores
from controllers.verification import check_elo_format, check_name_format, check_date_format


class HomeMenuController:
    def __init__(self, players, tournaments):
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.view = HomeMenuView(self.menu_data)

    def __call__(self):
        self.menu_data.add_entry("j", "MENU JOUEURS : Consulter, modifier et créer les joueurs", PlayersMenuController(self.players, self.tournaments))
        self.menu_data.add_entry("t", "MENU TOURNOIS : Consulter les tournois passés, en créer un nouveau", TournamentMenuController(self.players, self.tournaments))
        self.menu_data.add_entry("q", "Quitter le programme (tous les changements sont automatiquement enregistrés au fur et à mesure)", EndScreenController())
        self.menu_data.add_input_message("Saisissez votre choix")

        return self.view.get_user_choice()


class PlayersMenuController:
    def __init__(self, players, tournaments, sorting="surname"):
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.view = PlayersMenuView(self.menu_data)
        self.sorting = sorting
        self.parent_menu = HomeMenuController(self.players, self.tournaments)

    def __call__(self):
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
        self.menu_data.add_input_message("Saisissez le numéro d'un joueur pour modifier son Elo, ou choisissez une autre option")

        return self.view.get_user_choice()


class PlayerCreationMenuController:
    def __init__(self, players, tournaments, sorting):
        self.players = players
        self.tournaments = tournaments
        self.sorting = sorting
        self.menu_data = MenuData()
        self.view = PlayerCreationMenuView(self.menu_data)

    def __call__(self):
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

        self.menu_data.clear_data()
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION JOUEUR #'.center(105)}")
        self.menu_data.add_line(f"{'########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_entry("m", "Masculin", "M")
        self.menu_data.add_entry("f", "Féminin", "F")
        self.menu_data.add_input_message("Saisissez votre choix")
        sex = self.view.get_user_choice()

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

        player = Player(
            surname.capitalize(),
            name.capitalize(),
            birth_date,
            sex,
            elo,
        )

        player.save()
        self.players.append(player)

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
    def __init__(self, players, tournaments, player, sorting):
        self.players = players
        self.tournaments = tournaments
        self.player = player
        self.menu_data = MenuData()
        self.view = ModifyPlayerMenuView(self.menu_data)
        self.sorting = sorting

    def __call__(self):
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

        self.menu_data.add_line(f"{'#################'.center(150)}")
        self.menu_data.add_line(f"{'# MENU TOURNOIS #'.center(150)}")
        self.menu_data.add_line(f"{'#################'.center(150)}")
        self.menu_data.add_line("")
        if len(self.tournaments) != 0:
            self.menu_data.add_line(
                f"   |{'Nom'.center(35)}|{'Lieu'.center(15)}|{'Début'.center(10)}|"
                f"{'Fin'.center(10)}|{'Rondes'.center(6)}|"
                f"{'Cadence'.center(13)}|{'Description'.center(50)}|"
            )
            self.menu_data.add_line(
                f"---|{'-' * 35}|{'-' * 15}|{'-' * 10}|"
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
    def __init__(self, players, tournaments, tournament, sorting="score"):
        self.players = players
        self.tournaments = tournaments
        self.tournament = tournament
        self.menu_data = MenuData()
        self.view = TournamentInfoMenuView(self.menu_data)
        self.sorting = sorting

    def __call__(self):
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

        self.menu_data.add_entry("c", "Consulter le rapport des rondes et matchs du tournoi", TournamentRoundsMenuController(self.players, self.tournaments, self.tournament, self.sorting))
        if self.sorting == "score":
            self.menu_data.add_entry("a", "Classer les joueurs par ordre alphabétique", TournamentInfoMenuController(self.players, self.tournaments, self.tournament, "name"))
        elif self.sorting == "name":
            self.menu_data.add_entry("s", "Classer les joueurs par score du tournoi", TournamentInfoMenuController(self.players, self.tournaments, self.tournament, "score"))
        self.menu_data.add_entry("t", "MENU TOURNOIS : Consulter les tournois passés, en créer un nouveau", TournamentMenuController(self.players, self.tournaments))
        self.menu_data.add_entry("r", "ACCUEIL : Retourner au menu de démarrage", HomeMenuController(self.players, self.tournaments))
        self.menu_data.add_input_message("Saisissez votre choix")

        return self.view.get_user_choice()


class TournamentRoundsMenuController:
    def __init__(self, players, tournaments, tournament, sorting):
        self.players = players
        self.tournaments = tournaments
        self.tournament = tournament
        self.menu_data = MenuData()
        self.view = TournamentRoundsMenuView(self.menu_data)
        self.sorting = sorting

    def __call__(self):
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
    def __init__(self):
        self.menu_data = MenuData()
        self.view = EndScreenView(self.menu_data)

    def __call__(self):
        self.menu_data.add_line("Merci d'avoir utilisé Chess Tournament")
        self.menu_data.add_line("Tous les changements ont été sauvegardés au fur et à mesure")
        self.menu_data.add_line("Fermeture du programme")

        self.view.get_user_choice()
