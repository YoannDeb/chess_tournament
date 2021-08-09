class Menu:
    def __init__(self):
        self.entries = {}
        self.autokey = 1

    def add(self, key, menu_option, destination_controller):
        if key == "auto":
            key = self.autokey
            self.autokey += 1

        self.entries[str(key)] = (menu_option, destination_controller)


class HomeMenuView:
    def __init__(self, menu):
        self.menu = menu

    def display_menu(self):
        print("Chess Tournament")
        for key in self.menu.entries:
            print(f"{key}: {self.menu.entries[key][0]}")
        print("")

    def get_user_choice(self):
        while True:
            self.display_menu()
            choice = input("Saisissez votre choix >>")
            if choice in self.menu.entries:
                return self.menu.entries[choice][1]


class PlayerMenuView:
    def __init__(self, menu):
        self.menu = menu

    def display_menu(self):
        print("Menu Joueurs")
        for key in self.menu.entries:
            print(f"{key}: {self.menu.entries[key][0]}")
        print()

    def get_user_choice(self):
        while True:
            self.display_menu()
            choice = input("Saisissez votre choix >>")
            if choice in self.menu.entries:
                return self.menu[choice][1]
    pass


class ModifyPlayerMenuView:
    pass

