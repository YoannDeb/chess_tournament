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
        print("Chess Tournament")
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print("")

    def get_user_choice(self):
        while True:
            self.display_menu()
            choice = input("Saisissez votre choix >>")
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]


class PlayerMenuView:
    def __init__(self, menu_data):
        self.menu_data = menu_data

    def display_menu(self):
        print("Menu Joueurs")
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        while True:
            self.display_menu()
            choice = input("Saisissez votre choix >>")
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]


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




