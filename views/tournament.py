from core.utils import clear_screen


class InfoTournamentCreationView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def get_user_choice(self):
        clear_screen()
        return input(f"{self.menu_data.queries[0]} >> ").strip()


class TimeControlMenuView:
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
            choice = input(f"{self.menu_data.input_message} >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class TournamentRecoveryView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        input(f"{self.menu_data.input_message} >> ")


class FillRoundView:
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
            choice = input(f"{self.menu_data.input_message} >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class FillMatchView:
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
            choice = input(f"{self.menu_data.input_message} >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class TournamentRankingView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)

    def get_user_choice(self):
        clear_screen()
        self.display_menu()
        input(f"{self.menu_data.input_message} >> ")


