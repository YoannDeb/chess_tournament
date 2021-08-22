from views.utils import clear_screen


class HomeMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        print("                                    ####################")
        print("                                    # CHESS TOURNAMENT #")
        print("                                    ####################")
        print()
        print("                                             @")
        print("                                          &@@@@@(")
        print("                                       .@@@@@@@@@@@")
        print("                                     %@@@@@@@@@@@@@@@(")
        print("                                   @@@@@@@@@   @@@@@@@@@")
        print("                                %@@@@@@@@@#     @@@@@@@@@@(")
        print("             ,@@              @@@@@@@@@@@@@@   &@@@@@@@@@@@@@             ,@@")
        print("           &@@@@@@#        &@@@@@@@@@@@@@        .@@@@@@@@@@@@@/        &@@@@@@%")
        print("        ,@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@      .@@@@@@@@@@@@@@@@@   ,@@@@@@@@@@@@")
        print("       #@@@@@@@@@@@@@@,,@@@@@@@@@@@@@@@@@@&     &@@@@@@@@@@@@@@@@@@.(@@@@@@@@@@@@@@,")
        print("          @@@@@@@@@@      @@@@@@@@@@@@@@&        .@@@@@@@@@@@@@@&      @@@@@@@@@@")
        print("            #@@@@*          *@@@@@@@@@@@@@@     @@@@@@@@@@@@@@.          (@@@@*")
        print("              ,                @@@@@@@@@@@&    .@@@@@@@@@@@@               , ")
        print("            &@@@@(          #@@@@@@@@@@@@@&    .@@@@@@@@@@@@@@/          &@@@@#")
        print("         ,@@@@@@@@@@      @@@@@@@@@@@@@@@@@     &@@@@@@@@@@@@@@@@     .@@@@@@@@@@")
        print("       @@@@@@@@@@@@@@@#%@@@@@@@@@@@@@@@@@@,     &@@@@@@@@@@@@@@@@@@*&@@@@@@@@@@@@@@%")
        print("        @@@@@@@@@@@@    @@@@@@@@@@@@@@@@&       &@@@@@@@@@@@@@@@&    @@@@@@@@@@@@")
        print("           #@@@@@@*        /@@@@@@@@@@@@.         (@@@@@@@@@@@@,        #@@@@@@/")
        print("              @@              @@@@@@@@.             #@@@@@@@@              @@")
        print("                                (@@@@@#             &@@@@@,")
        print("                                   @@@@@@@@@@@@@@@@@@@@&")
        print("                                     /@@@@@@@@@@@@@@@,")
        print("                                        @@@@@@@@@@&")
        print("                                          /@@@@@,")
        print("                                             @")
        print()

        for key in self.menu_data.entries:
            if self.menu_data.entries[key][2] == "top_menu":
                print(f"{key} : {self.menu_data.entries[key][0]}")
        print()
        for key in self.menu_data.entries:
            if self.menu_data.entries[key][2] == "bottom_menu":
                print(f"{key} : {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            choice = input(f"{self.menu_data.input_message} >> ").strip().lower()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class PlayersMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for line in self.menu_data.lines:
            print(line)

        for key in self.menu_data.entries:
            if self.menu_data.entries[key][2] == "top_menu":
                print(f"{key.center(4)}{self.menu_data.entries[key][0]}")
        print()
        for key in self.menu_data.entries:
            if self.menu_data.entries[key][2] == "bottom_menu":
                print(f"{key} : {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            choice = input(f"{self.menu_data.input_message} >> ").strip().lower()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class PlayerCreationMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for line in self.menu_data.lines:
            print(line)

        for key in self.menu_data.entries:
            print(f"{key} : {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        if self.menu_data.entries:
            while True:
                choice = input(f"{self.menu_data.input_message} >> ").strip().lower()
                if choice in self.menu_data.entries:
                    return self.menu_data.entries[choice][1]
                clear_screen()
                self.display_menu()
                print("/!\\ Choix invalide /!\\")
        else:
            return input(f"{self.menu_data.queries[0]} >> ").strip()


class ModifyPlayerMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for line in self.menu_data.lines:
            print(line)
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        return input(f"{self.menu_data.queries[0]} >> ").strip()


class TournamentMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for line in self.menu_data.lines:
            print(line)

        for key in self.menu_data.entries:
            if self.menu_data.entries[key][2] == "top_menu":
                print(f"{key.center(4)}{self.menu_data.entries[key][0]}")
        print()
        for key in self.menu_data.entries:
            if self.menu_data.entries[key][2] == "bottom_menu":
                print(f"{key} : {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            choice = input(f"{self.menu_data.input_message} >> ").strip().lower()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class TournamentInfoMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for line in self.menu_data.lines:
            print(line)

        for key in self.menu_data.entries:
            if self.menu_data.entries[key][2] == "top_menu":
                print(f"{key} : {self.menu_data.entries[key][0]}")
        print()
        for key in self.menu_data.entries:
            if self.menu_data.entries[key][2] == "bottom_menu":
                print(f"{key} : {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        while True:
            choice = input(f"{self.menu_data.input_message} >> ").strip().lower()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class TournamentRoundsMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for line in self.menu_data.lines:
            print(line)

        print()

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        return input(f"{self.menu_data.queries[0]} >> ").strip()


class EndScreenView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        clear_screen()

        for line in self.menu_data.lines:
            print(line)

    def get_user_choice(self):
        self.display_menu()
