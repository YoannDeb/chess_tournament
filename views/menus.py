from core.utils import clear_screen


class HomeMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        print("CHESS TOURNAMENT")
        print("                                        @")
        print("                                     &@@@@@(")
        print("                                  .@@@@@@@@@@@")
        print("                                %@@@@@@@@@@@@@@@(")
        print("                              @@@@@@@@@   @@@@@@@@@")
        print("                           %@@@@@@@@@#     @@@@@@@@@@(")
        print("        ,@@              @@@@@@@@@@@@@@   &@@@@@@@@@@@@@             ,@@")
        print("      &@@@@@@#        &@@@@@@@@@@@@@        .@@@@@@@@@@@@@/        &@@@@@@%")
        print("   ,@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@      .@@@@@@@@@@@@@@@@@   ,@@@@@@@@@@@@")
        print("  #@@@@@@@@@@@@@@,,@@@@@@@@@@@@@@@@@@&     &@@@@@@@@@@@@@@@@@@.(@@@@@@@@@@@@@@,")
        print("     @@@@@@@@@@      @@@@@@@@@@@@@@&        .@@@@@@@@@@@@@@&      @@@@@@@@@@")
        print("       #@@@@*          *@@@@@@@@@@@@@@     @@@@@@@@@@@@@@.          (@@@@*")
        print("         ,                @@@@@@@@@@@&    .@@@@@@@@@@@@               , ")
        print("       &@@@@(          #@@@@@@@@@@@@@&    .@@@@@@@@@@@@@@/          &@@@@#")
        print("    ,@@@@@@@@@@      @@@@@@@@@@@@@@@@@     &@@@@@@@@@@@@@@@@     .@@@@@@@@@@")
        print("  @@@@@@@@@@@@@@@#%@@@@@@@@@@@@@@@@@@,     &@@@@@@@@@@@@@@@@@@*&@@@@@@@@@@@@@@%")
        print("    @@@@@@@@@@@@    @@@@@@@@@@@@@@@@&       &@@@@@@@@@@@@@@@&    @@@@@@@@@@@@")
        print("      #@@@@@@*        /@@@@@@@@@@@@.         (@@@@@@@@@@@@,        #@@@@@@/")
        print("         @@              @@@@@@@@.             #@@@@@@@@              @@")
        print("                           (@@@@@#             &@@@@@,")
        print("                              @@@@@@@@@@@@@@@@@@@@&")
        print("                                /@@@@@@@@@@@@@@@,")
        print("                                   @@@@@@@@@@&")
        print("                                     /@@@@@,")
        print("                                        @")
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            choice = input("Saisissez votre choix >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class PlayersMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            if self.menu_data.input_message is not None:
                choice = input(f"{self.menu_data.input_message} >>")
            else:
                choice = input("Saisissez le numéro d'un joueur pour modifier son Elo, ou choisissez une autre option >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class PlayerCreationMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data
        self.player_attributes = []

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        for query in self.menu_data.queries:
            self.player_attributes.append(input(f"{query} >> ").strip())
        return self.player_attributes


class PlayerCreationConfirmationMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)
        print()

        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            choice = input("Saisissez votre choix >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class ModifyPlayerMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        return input(f"{self.menu_data.queries[0]} >> ").strip()


class TournamentMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        print("MENU TOURNOIS")
        for header in self.menu_data.headers:
            print(header)

        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            choice = input("Saisissez le numéro d'un tournoi pour plus d'informations, ou choisissez une autre option >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class TournamentInfoMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)

        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            choice = input("Saisissez votre choix >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")
