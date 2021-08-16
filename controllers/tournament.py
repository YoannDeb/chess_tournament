from models.player import Player
from models.tournament import Tournament
from views.menus import PlayersMenuView
from views.tournament import InfoTournamentCreationView, TimeControlMenuView, TournamentRecoveryView, FillRoundView, FillMatchView, TournamentRankingView
from core.utils import MenuData, get_player_tournament_info


class CreateTournament:
    def __init__(self, players, sorting="surname"):
        self.players = players
        self.sorting = sorting
        self.menu_data_info = MenuData()
        self.menu_data_players = MenuData()
        self.menu_data_time_control = MenuData()
        self.view_info = InfoTournamentCreationView(self.menu_data_info)
        self.view_players = PlayersMenuView(self.menu_data_players)
        self.view_time_control = TimeControlMenuView(self.menu_data_time_control)
        self.tournament_players_id = []

    def __call__(self):
        # todo add format verification for all tournament info
        name = self.tournament_name()
        location = self.tournament_location()
        round_number = int(self.rounds_number())

        while True:
            choice = self.player_menu()
            if choice == "surname" or choice == "elo_ranking":
                self.sorting = choice
            elif choice == "end" or len(self.tournament_players_id) == 8:
                # todo add player verification and confirmation ?
                break
            else:
                self.tournament_players_id.append(choice)

        time_control = self.time_control()
        description = self.description()

        return Tournament(name, location, self.tournament_players_id, time_control, description, round_number)

    def tournament_name(self):
        self.menu_data_info.add_query("Entrez le nom du tournoi")
        return self.view_info.get_user_choice()

    def tournament_location(self):
        self.menu_data_info.queries[0] = "Entrez le lieu du tournoi"
        return self.view_info.get_user_choice()

    def rounds_number(self):
        self.menu_data_info.queries[0] = "Entrez le nombre de rondes du tournoi (par défaut 4)"
        return self.view_info.get_user_choice()

    def player_menu(self):
        # todo rajouter la possibilité d'enlever un joueur
        already_selected_name_list = [f"{Player.get(player_id).surname}, {Player.get(player_id).name}" for player_id in self.tournament_players_id]
        self.menu_data_players.clear_data()
        self.menu_data_players.add_header("SELECTION DES JOUEURS DU TOURNOI")

        if self.sorting == "surname":
            self.players.sort(key=lambda chess_player: chess_player.surname)
        elif self.sorting == "elo_ranking":
            self.players.sort(key=lambda chess_player: chess_player.elo_ranking)
            self.players.reverse()

        for player in self.players:
            if player.id not in self.tournament_players_id:
                self.menu_data_players.add_entry("auto", player, player.id)
        if len(self.menu_data_players.entries) != 0:
            self.menu_data_players.add_header(
                "Index, Nom, Prénom, Date de naissance, Sexe, Classement Elo"
            )  # todo adjust header or decide not to show them or make a real table !
            if self.sorting == "surname":
                self.menu_data_players.add_entry("e", "Classer par Elo", "elo_ranking")
            elif self.sorting == "elo_ranking":
                self.menu_data_players.add_entry("a", "Classer par ordre alphabétique", "surname")
        else:
            self.menu_data_players.add_header("Plus de joueur disponible dans la base")

        # todo self.menu_data_players.add_entry("c", "Créer un nouveau joueur", PlayersMenuCreationController(self.players, self.tournaments))  # todo implement player creation in tournament creation
        self.menu_data_players.add_entry("t", "Terminer la selection", "end")
        self.menu_data_players.add_input_message(f"{len(self.tournament_players_id)} joueur(s) déjà sélectionné(s):\n {already_selected_name_list} \nSélectionnez un joueur supplémentaire ou choisissez une autre option")

        return self.view_players.get_user_choice()

    def time_control(self):
        self.menu_data_time_control.add_header("Choix de la cadence (Contrôle du temps):")
        self.menu_data_time_control.add_entry("auto", "Bullet", "Bullet")
        self.menu_data_time_control.add_entry("auto", "Blitz", "Blitz")
        self.menu_data_time_control.add_entry("auto", "Coup rapide", "Coup rapide")
        self.menu_data_time_control.add_input_message("Veuillez choisir la cadence")
        return self.view_time_control.get_user_choice()

    def description(self):
        self.menu_data_info.queries[0] = "Entrez une description du tournoi"
        return self.view_info.get_user_choice()


class TournamentController:
    def __init__(self, players, tournaments, parent_controller, tournament=None):
        self.players = players
        self.tournaments = tournaments
        self.menu_data = MenuData()
        self.parent_controller = parent_controller
        self.tournament = tournament

    def __call__(self):
        if self.tournament is None:
            create_tournament = CreateTournament(self.players)
            self.tournament = create_tournament()
            self.tournament.save()
            self.tournaments.append(self.tournament)
            self.view = None

        print(self.tournament.players_id)
        self.tournament.sort_players_id_by_rank()
        print(self.tournament.players_id)
        input()

        if len(self.tournament.rounds) == 0:
            self.tournament.generate_first_round()
            self.tournament.save()
        else:
            self.menu_data.add_header("REPRISE DU TOURNOI PRECEDEMMENT INTERROMPU:")
            self.menu_data.add_header(f"{self.tournament}")
            self.menu_data.add_input_message("Appuyez sur Entrée pour poursuivre le tournoi")
            TournamentRecoveryView(self.menu_data).get_user_choice()

        for round_index in range(self.tournament.total_round_number):
            if round_index == len(self.tournament.rounds) - 1:
                while True:
                    self.menu_data.clear_data()
                    self.menu_data.add_header(f"APPARIEMENTS {self.tournament.rounds[round_index].name} :")
                    match_number = 0
                    all_matches_filled = True
                    for match in self.tournament.rounds[round_index].matches:
                        match_number += 1
                        if match[0][1] is None:
                            match_score = "Non renseigné"
                            all_matches_filled = False
                        else:
                            match_score = f"{match[0][1]} - {match[1][1]}"
                        self.menu_data.add_entry("auto", f"Échiquier {match_number} : {Player.get(match[0][0]).surname} vs {Player.get(match[1][0]).surname} | Résultat : {match_score}", match)
                    if all_matches_filled:
                        self.menu_data.add_entry("t", "Terminer le Round et afficher le classement", "end")
                        self.menu_data.add_input_message("Choisissez un match pour modifier son résultat ou bien entrez \"t\" pour terminer le Round")
                    else:
                        self.menu_data.add_input_message("Choisissez un match pour renseigner ou modifier son résultat")

                    choice = FillRoundView(self.menu_data).get_user_choice()
                    if choice == "end":
                        break
                    else:
                        self.menu_data.clear_data()
                        self.menu_data.add_header(f"Résultat du match {Player.get(choice[0][0]).surname} vs {Player.get(choice[1][0]).surname}")
                        self.menu_data.add_entry("auto", f"Victoire de {Player.get(choice[0][0]).surname}", (1, 0))
                        self.menu_data.add_entry("auto", f"Victoire de {Player.get(choice[1][0]).surname}", (0, 1))
                        self.menu_data.add_entry("auto", "Match nul", (0.5, 0.5))
                        self.menu_data.add_input_message("Choisissez le résultat du match")
                        scores = FillMatchView(self.menu_data).get_user_choice()
                        choice[0][1] = scores[0]
                        choice[1][1] = scores[1]
                        self.tournament.save()

                self.tournament.rounds[round_index].register_end_time()
                print(self.tournament.players_id)
                self.tournament.sort_players_id_by_rank()
                print(self.tournament.players_id)
                input()
                self.menu_data.clear_data()  # todo apparemment non classés + score 1.0 moches ou alors tout en 1 chiffre après la virgule
                self.menu_data.add_header("TABLEAU DES SCORES")
                for player_id in self.tournament.players_id:
                    self.menu_data.add_header(get_player_tournament_info(player_id, self.tournament))
                if round_index == self.tournament.total_round_number - 1:
                    self.tournament.end_tournament()
                    self.menu_data.add_header("Le tournoi est terminé")
                    self.menu_data.add_input_message("Appuyez sur Entrée pour revenir au menu principal")
                else:
                    self.menu_data.add_input_message("Appuyez sur Entrée pour passer à la ronde suivante")
                    self.tournament.generate_following_round()
                self.tournament.save()
                TournamentRankingView(self.menu_data).get_user_choice()

        return self.parent_controller(self.players, self.tournaments)






