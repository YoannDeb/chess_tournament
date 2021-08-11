class MenuData:
    def __init__(self):
        self.entries = {}
        self.headers = []
        self.queries = []
        self.autokey = 1

    def add_entry(self, key, menu_option, destination_controller):
        if key == "auto":
            key = self.autokey
            self.autokey += 1

        self.entries[str(key)] = (menu_option, destination_controller)

    def add_header(self, text):
        self.headers.append(text)

    def add_query(self, text):
        self.queries.append(text)

    def add_bottom(self):
        pass

    def add_row(self):
        pass


class HomeMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        print("CHESS TOURNAMENT")
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print("")

    def get_user_choice(self):
        self.display_menu()
        while True:
            choice = input("Saisissez votre choix >>")
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            print("/!\\ Choix invalide /!\\")


class PlayersMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        print("MENU JOUEURS")
        for header in self.menu_data.headers:
            print(header)
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        self.display_menu()
        while True:
            choice = input("Saisissez le numéro d'un joueur pour modifier son Elo, ou choisissez une autre option >>")
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            print("/!\\ Choix invalide /!\\")


class PlayerCreationMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data
        self.player_attributes = []

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)
        print()

    def get_user_choice(self):
        print("CREATION D'UN NOUVEAU JOUEUR")
        self.display_menu()
        for query in self.menu_data.queries:
            self.player_attributes.append(input(f"{query} >>"))
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
        self.display_menu()
        while True:
            choice = input("Saisissez votre choix >>")
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            print("/!\\ Choix invalide /!\\")


class ModifyPlayerMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        for header in self.menu_data.headers:
            print(header)
        print()

    def get_user_choice(self):
        self.display_menu()
        return input(f"{self.menu_data.queries[0]} >>")


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
        self.display_menu()
        while True:
            choice = input("Saisissez le numéro d'un tournoi pour plus d'informations, ou choisissez une autre option >>")
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
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
        self.display_menu()
        while True:
            choice = input("Saisissez votre choix >>")
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            print("/!\\ Choix invalide /!\\")





