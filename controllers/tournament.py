"""
Controller classes for tournament management.
"""
from models.player import Player
from models.tournament import Tournament
from views.menus import PlayersMenuView
from views.tournament import InfoTournamentCreationView, TimeControlMenuView, TooMuchRoundsView,\
    TournamentRecoveryView, FillRoundView, FillMatchView, TournamentRankingView
from controllers.utils import check_name_format, check_rounds_number_format, get_player_tournament_scores
from core.utils import MenuData


class CreateTournament:
    """
    Controller for tournament creation interface.
    Interacting with InfoTournamentCreationView, PlayersMenuView, TooMuchRoundsView and TimeControlMenuView.
    """
    def __init__(self, players, sorting="surname"):
        """
        Init method.
        self.menu_data: An instance of MenuData.
        self.view_info: An instance of InfoTournamentCreationView taking self.menu_data as parameter.
        self.view_players: An instance of PlayersMenuView taking self.menu_data as parameter.
        self.view_too_much_rounds: An instance of TooMuchRoundsView taking self.menu_data as parameter.
        self.view_time_control: An instance of TimeControlMenuView taking self.menu_data as parameter.
        self.tournament_players_ids: A list of players' ids participating to the tournament.
        :param players: A list of instances of all players registered in database.
        :param sorting: A list of instances of all tournaments registered in database.
        """
        self.players = players
        self.sorting = sorting
        self.menu_data = MenuData()
        self.view_info = InfoTournamentCreationView(self.menu_data)
        self.view_players = PlayersMenuView(self.menu_data)
        self.view_too_much_rounds = TooMuchRoundsView(self.menu_data)
        self.view_time_control = TimeControlMenuView(self.menu_data)
        self.tournament_players_ids = []

    def __call__(self):
        """
        Creation of the tournament in itself :
        - Uses dedicated functions to gather validated info from the views (name, location, rounds number).
        - A loop to add players to self.players_ids, with sorting and validating functions,
            and possibility to change the rounds number.
        - Gathering last info (time control and description)
        :return: An instance of tournament created with info previously gathered.
        """
        name = self.tournament_name()
        self.menu_data.clear_data()
        location = self.tournament_location()
        self.menu_data.clear_data()
        rounds_number = int(self.rounds_number())

        # Player selection loop
        while True:
            self.menu_data.clear_data()
            choice = self.player_menu(rounds_number)
            if choice == "surname" or choice == "elo_ranking":
                self.sorting = choice
            elif choice == "rounds":
                self.menu_data.clear_data()
                rounds_number = int(self.rounds_number())
            elif choice == "end":
                if len(self.tournament_players_ids) < (rounds_number + 4):
                    self.menu_data.clear_data()
                    choice2 = self.too_much_rounds()
                    if choice2 == "rounds":
                        self.menu_data.clear_data()
                        rounds_number = int(self.rounds_number())
                elif len(self.tournament_players_ids) % 2 == 1:
                    self.menu_data.clear_data()
                    self.odd_players_number()
                else:
                    break
            else:
                self.tournament_players_ids.append(choice)

        self.menu_data.clear_data()
        time_control = self.time_control()
        self.menu_data.clear_data()
        description = self.description()

        return Tournament(name, location, self.tournament_players_ids, time_control, description, rounds_number)

    def tournament_name(self):
        """
        Tournament name controller function, interacting with InfoTournamentCreationView.
        Gathers tournament name and returns it if it is valid.
        :return: Name of the future tournament.
        """
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION TOURNOI #'.center(105)}")
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez entrer le nom du tournoi")
        while True:
            name = self.view_info.get_user_choice()
            if check_name_format(name):
                name = name.strip().capitalize()
                return name
            else:
                self.menu_data.add_line(
                    f"/!\\ Nom du tournoi '{name}' invalide, le nom du tournoi ne peut pas"
                    f" être vide et doit commencer par une lettre /!\\"
                )

    def tournament_location(self):
        """
        Tournament location controller function, interacting with InfoTournamentCreationView.
        Gathers tournament location and returns it if it is valid.
        :return: Location of the future tournament.
        """
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION TOURNOI #'.center(105)}")
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez entrer le lieu du tournoi")
        while True:
            location = self.view_info.get_user_choice()
            if check_name_format(location):
                location = location.strip().capitalize()
                return location
            else:
                self.menu_data.add_line(
                    f"/!\\ Lieu du tournoi '{location}' invalide, le lieu du tournoi ne peut pas"
                    f" être vide et doit commencer par une lettre /!\\"
                )

    def rounds_number(self):
        """
        Tournament rounds number controller function, interacting with InfoTournamentCreationView.
        Gathers tournament rounds number and returns it if it is valid.
        :return: Rounds number of the future tournament.
        """
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION TOURNOI #'.center(105)}")
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez entrer le nombre de rondes du tournoi")
        while True:
            rounds_number = self.view_info.get_user_choice()
            if check_rounds_number_format(rounds_number):
                rounds_number = int(rounds_number)
                return rounds_number
            else:
                self.menu_data.add_line(
                    f"/!\\ Nombre de rondes '{rounds_number}' invalide, le nombre"
                    f" de rondes doit être un nombre entier supérieur à 2 /!\\"
                )

    def player_menu(self, rounds_number):
        """
        Tournament players' selection controller function, interacting with PlayersMenuView.
        Gathers one tournament player from the list of all players.
        Other choices are possible:
         - Sorting type (ranking or surname)
         - Rounds number selection menu
         - End the selection (will be validated or not in __call__ function of the class)
        :return: Users Choice
        """
        already_selected_name_list = []
        for player_id in self.tournament_players_ids:
            already_selected_name_list.append(f"{Player.get(player_id).surname}, {Player.get(player_id).name}")

        self.menu_data.clear_data()
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION TOURNOI #'.center(105)}")
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_line("/!\\ Il doit y avoir au moins quatre joueurs de plus que le"
                                " nombre de rondes du tournoi, et le nombre de joueurs doit être pair /!\\")
        self.menu_data.add_line("")
        self.menu_data.add_line(f"{len(self.tournament_players_ids)} joueur(s) déjà"
                                f" sélectionné(s) pour {rounds_number} rondes")
        if len(self.tournament_players_ids) != 0:
            self.menu_data.add_line(f"{already_selected_name_list}")
            self.menu_data.add_line("")
        self.menu_data.add_line("")

        if self.sorting == "surname":
            self.players.sort(key=lambda chess_player: chess_player.surname)
        elif self.sorting == "elo_ranking":
            self.players.sort(key=lambda chess_player: chess_player.elo_ranking, reverse=True)

        for player in self.players:
            if player.id not in self.tournament_players_ids:
                self.menu_data.add_entry("auto", player, player.id)
        if len(self.menu_data.entries) != 0:
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
            if self.sorting == "surname":
                self.menu_data.add_entry("e", "Classer par Elo", "elo_ranking")
            elif self.sorting == "elo_ranking":
                self.menu_data.add_entry("a", "Classer par ordre alphabétique", "surname")
        else:
            self.menu_data.add_line("Plus de joueur disponible dans la base")
        self.menu_data.add_entry("r", "Changer le nombre de rondes", "rounds")
        self.menu_data.add_entry("t", "Terminer la selection", "end")
        self.menu_data.add_input_message("Sélectionnez un joueur à ajouter au tournoi ou choisissez une autre option")

        return self.view_players.get_user_choice()

    def too_much_rounds(self):
        """
        Controller for a menu showed when there are too much rounds comparatively to the players total number.
        Interacting with TooMuchRoundsView.
        :return: User's choice ("player" or "rounds")
        """
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION TOURNOI #'.center(105)}")
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_line("Trop de rondes, pas assez de joueurs !")
        self.menu_data.add_line("")
        self.menu_data.add_entry("j", "Ajouter des joueurs au tournoi", "players")
        self.menu_data.add_entry("r", "Changer le nombre de rondes", "rounds")
        self.menu_data.add_input_message("Saisissez votre choix")
        return self.view_too_much_rounds.get_user_choice()

    def odd_players_number(self):
        """
        Controller for a menu showed when players total number id odd.
        Interacts with InfoTournamentCreationView.
        Returns nothing (no need for info here, user is redirected to players selection menu).
        """
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION TOURNOI #'.center(105)}")
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_line("Nombre de joueurs impair !")
        self.menu_data.add_line("")
        self.menu_data.add_query("Appuyez sur Entrée pour ajouter des joueurs")
        self.view_info.get_user_choice()

    def time_control(self):
        """
        Controller for a time control selection menu. Interacts with TimeControlMenuView.
        :return: A string containing time control type.
        """
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION TOURNOI #'.center(105)}")
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_entry("auto", "Bullet", "Bullet")
        self.menu_data.add_entry("auto", "Blitz", "Blitz")
        self.menu_data.add_entry("auto", "Coup rapide", "Coup rapide")
        self.menu_data.add_input_message("Veuillez choisir la cadence (Contrôle du temps)")
        return self.view_time_control.get_user_choice()

    def description(self):
        """
        Tournament description controller function, interacting with InfoTournamentCreationView.
        Gathers tournament name and returns it if it is valid.
        :return: Description of the future tournament.
        """
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line(f"{'# MENU CREATION TOURNOI #'.center(105)}")
        self.menu_data.add_line(f"{'#########################'.center(105)}")
        self.menu_data.add_line("")
        self.menu_data.add_query("Veuillez entrer une description pour le tournoi")
        while True:
            description = self.view_info.get_user_choice()
            if check_name_format(description):
                description = description.strip().capitalize()
                return description
            else:
                self.menu_data.add_line(
                    f"/!\\ Description '{description}' invalide, la description ne peut pas"
                    f" être vide et doit commencer par une lettre /!\\"
                )


class TournamentController:
    """
    Controller for ongoing tournament (match making, scores filling).
    Including tournament recovery to the state where it was if a tournament is passed in parameters.
    Instantiate CreateTournament object if not.
    """
    def __init__(self, players, tournaments, parent_controller, tournament=None):
        """
        Init Method.
        self.menu_data: An instance of MenuData containing info to display.
        :param players: A list of instances of all players registered in database.
        :param tournaments: A list of instances of all tournaments registered in database.
        :param parent_controller: A controller (HomeMenuController) to return to when the tournament is done.
        :param tournament: The ongoing tournament if it is a tournament recovery, None if not.
        """
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.parent_controller = parent_controller
        self.tournament = tournament

    def __call__(self):
        """
        Call function, using multiple views to manage ongoing tournament, and save regularly:
        - First creates the tournament if needed
        - Generate first round's match making if no round exist.
        - Shows Recovery information if at least one round exist, using TournamentRecoveryView.
        - Iterates for each theoretical round.
        - Check if the round is the last created (means it is the ongoing round).
            If not it will do nothing and pass to the following round.
        - Loops to show match pairs to the user and allow scores filling for a match if selected.
            Interacts with FillRoundView.
        - If a match is selected, the user can enter the score via a menu using FillMatchView.
            The score is registered and the tournament is saved.
        - When all scores are given, the user can choose to terminate the round (or he can still change a score).
        - When the round is finished, a score table is sent to TournamentRankingView.
        - An other round is generated if it was not the last one.
            Tournament is saved and the same process is repeated for the next round.
        - If it was the last one, the tournament is terminated (registering end date). The iteration is finished.
        :return: Instance of HomeMenuController
        """
        # Creates tournament if needed.
        if self.tournament is None:
            create_tournament = CreateTournament(self.players)
            self.tournament = create_tournament()
            self.tournament.save()
            self.tournaments.append(self.tournament)
            self.view = None

        self.tournament.sort_players_ids_by_rank()

        # Generate first round's match making if no round exist.
        if len(self.tournament.rounds) == 0:
            self.tournament.generate_first_round()
            self.tournament.save()

        # Shows Recovery information if at least one round exist.
        else:
            self.menu_data.add_line(f"{'######################'.center(147)}")
            self.menu_data.add_line(f"{'# REPRISE DU TOURNOI #'.center(147)}")
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
            self.menu_data.add_input_message("Appuyez sur Entrée pour poursuivre le tournoi")
            TournamentRecoveryView(self.menu_data).get_user_choice()

        # Iterates for each theoretical round.
        for round_index in range(self.tournament.total_round_number):

            # Check if the round is the last created (means it is the ongoing round).
            # If not it will do nothing and pass to the following round.
            if round_index == len(self.tournament.rounds) - 1:

                # Shows match making to the user and allows scores filling.
                while True:
                    self.menu_data.clear_data()
                    title = f"# APPARIEMENTS {self.tournament.rounds[round_index].name.upper()} #"
                    title_frame = f"{'#' * len(title)}"
                    self.menu_data.add_line(f"{title_frame.center(147)}")
                    self.menu_data.add_line(f"{title.center(147)}")
                    self.menu_data.add_line(f"{title_frame.center(147)}")
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

                    self.menu_data.add_line(f"Appariements {self.tournament.rounds[round_index].name} :")
                    self.menu_data.add_line("")
                    match_number = 0
                    all_matches_filled = True
                    for match in self.tournament.rounds[round_index].matches:
                        match_number += 1
                        player1 = f"{Player.get(match[0][0]).surname}, {Player.get(match[0][0]).name}"
                        player2 = f"{Player.get(match[1][0]).surname}, {Player.get(match[1][0]).name}"
                        if match[0][1] is None:
                            match_score = "( Non renseigné )"
                            all_matches_filled = False
                        elif match[0][1] == 0.5:
                            match_score = f"  ( {match[0][1]} - {match[1][1]} )  "
                        else:
                            match_score = f"    ( {match[0][1]} - {match[1][1]} )    "
                        self.menu_data.add_entry("auto", f"Échiquier {match_number} : {player1.center(40)} "
                                                         f"{match_score.center(13)} {player2.center(40)}", match)
                    if all_matches_filled:
                        self.menu_data.add_entry("t", "Terminer la ronde et afficher le classement", "end")
                        self.menu_data.add_input_message(
                            "Choisissez un match pour modifier son résultat ou bien entrez "
                            "\"t\" pour terminer la ronde et afficher le classement"
                        )
                    else:
                        self.menu_data.add_input_message("Choisissez un match pour renseigner"
                                                         " ou modifier son résultat")

                    choice = FillRoundView(self.menu_data).get_user_choice()

                    # Goes to end of the round if all scores filled and "end" chosen by user.
                    if choice == "end":
                        break
                    # Score filling for the match selected.
                    else:
                        self.menu_data.clear_data()
                        self.menu_data.add_line(f"{'##########################'.center(147)}")
                        self.menu_data.add_line(f"{'# RENSEIGNEMENT DU SCORE #'.center(147)}")
                        self.menu_data.add_line(f"{'##########################'.center(147)}")
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
                        player1 = f"{Player.get(choice[0][0]).surname}, {Player.get(choice[0][0]).name}"
                        player2 = f"{Player.get(choice[1][0]).surname}, {Player.get(choice[1][0]).name}"
                        self.menu_data.add_line(f"Résultat du match : {player1} | {player2}")
                        self.menu_data.add_line("")
                        self.menu_data.add_entry("auto", f"Victoire de : {player1}", (1, 0))
                        self.menu_data.add_entry("auto", f"Victoire de : {player2}", (0, 1))
                        self.menu_data.add_entry("auto", "Match nul", (0.5, 0.5))
                        self.menu_data.add_input_message("Choisissez le résultat du match")
                        scores = FillMatchView(self.menu_data).get_user_choice()
                        choice[0][1] = scores[0]
                        choice[1][1] = scores[1]

                        self.tournament.save()

                # Round ending, shows ranking and creates a new round (if it is not the last one).
                self.tournament.rounds[round_index].register_end_time()
                self.tournament.rounds[round_index].normalize_score_signifiance()
                self.tournament.sort_players_ids_by_rank()
                self.menu_data.clear_data()
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

                self.menu_data.add_line(f"Classement à la ronde : {self.tournament.rounds[-1].name}")
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
                position = 0
                for player_id in self.tournament.players_ids:
                    position += 1
                    player = Player.get(player_id)
                    player_scores = get_player_tournament_scores(player_id, self.tournament)
                    self.menu_data.add_line(
                        f"|{str(position).center(12)}|{player.surname.center(30)}|{player.name.center(30)}|"
                        f"{str(player_scores).center(54)}|{str(sum(player_scores)).center(15)}|"
                    )
                self.menu_data.add_line("")
                # It is the last round, the ending date is registered
                if round_index == self.tournament.total_round_number - 1:
                    self.tournament.end_tournament()
                    self.menu_data.add_line("Le tournoi est terminé")
                    self.menu_data.add_line("")
                    self.menu_data.add_input_message("Appuyez sur Entrée pour revenir au menu principal")
                # It is not the last round, the following round is generated.
                else:
                    self.tournament.generate_following_round()
                    self.menu_data.add_input_message(f"Appuyez sur Entrée pour passer à la ronde"
                                                     f" suivante : {self.tournament.rounds[-1].name}")

                self.tournament.save()

                TournamentRankingView(self.menu_data).get_user_choice()

        # The loop is finished, returns to home menu.
        return self.parent_controller(self.players, self.tournaments)
