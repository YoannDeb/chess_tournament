"""
Views classes for menus.
"""
from views.utils import clear_screen


class HomeMenuView:
    """
    View class for home menu, interacting with HomeMenuController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
        Init method.
        :param menu_data: An instance of MenuData containing info to display.
        """
        self.menu_data = menu_data

    def display_menu(self):
        """
        Displays a title and ASCII art logo.
        Displays menu_data entries.
        """
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

        for line in self.menu_data.lines:
            print(line)
        for key in self.menu_data.entries:
            print(f"{key} : {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes an user input and return choice if the input is in possible menu choices.
        :return: A instance of a controller class depending on the choice of the user.
        """
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
    """
    View class for home menu, interacting with PlayersMenuController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
        Init method.
        :param menu_data: An instance of MenuData containing info to display.
        """
        self.menu_data = menu_data

    def display_menu(self):
        """
        Displays self.menu_data's lines, top_menu entries, then bottom_menu entries.
        """
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
        """
        Clears screen then displays menu content.
        Finally takes an user input and return choice if the input is in possible menu choices.
        :return: A instance of a controller class depending on the choice of the user.
        """
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
    """
    View class for home menu, interacting with PlayerCreationMenuController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
        Init method.
        :param menu_data: An instance of MenuData containing info to display.
        """
        self.menu_data = menu_data

    def display_menu(self):
        """
        Displays self.menu_data's lines then entries.
        :return:
        """
        for line in self.menu_data.lines:
            print(line)
        for key in self.menu_data.entries:
            print(f"{key} : {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes an user input and return choice if the input is in possible menu choices.
        :return: A instance of a controller class depending on the choice of the user.
        """
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


class ModifyPlayerEloMenuView:
    """
    View class for home menu, interacting with ModifyPlayerEloController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
        Init method.
        :param menu_data: An instance of MenuData containing info to display.
        """
        self.menu_data = menu_data

    def display_menu(self):
        """
        Displays self.menu_data's lines.
        """
        for line in self.menu_data.lines:
            print(line)
        print()

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes an input and returns it.
        :return: User input.
        """
        clear_screen()
        self.display_menu()
        return input(f"{self.menu_data.queries[0]} >> ").strip()


class TournamentsMenuView:
    """
    View class for home menu, interacting with TournamentsMenuController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
        Init method.
        :param menu_data: An instance of MenuData containing info to display.
        """
        self.menu_data = menu_data

    def display_menu(self):
        """
        Displays self.menu_data's lines, top_menu entries, then bottom_menu entries.
        """
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
        """
        Clears screen then displays menu content.
        Finally takes an user input and return choice if the input is in possible menu choices.
        :return: A instance of a controller class depending on the choice of the user.
        """
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
    """
    View class for home menu, interacting with TournamentInfoMenuController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
        Init method.
        :param menu_data: An instance of MenuData containing info to display.
        """
        self.menu_data = menu_data

    def display_menu(self):
        """
        Displays self.menu_data's lines, top_menu entries, then bottom_menu entries.
        """
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
        """
        Clears screen then displays menu content.
        Finally takes an user input and return choice if the input is in possible menu choices.
        :return: A instance of a controller class depending on the choice of the user.
        """
        clear_screen()
        self.display_menu()
        while True:
            choice = input(f"{self.menu_data.input_message} >> ").strip().lower()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class RoundsInfoMenuView:
    """
    View class for home menu, interacting with RoundsInfoMenuController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
        Init method.
        :param menu_data: An instance of MenuData containing info to display.
        """
        self.menu_data = menu_data

    def display_menu(self):
        """
        Displays self.menu_data's lines.
        """
        for line in self.menu_data.lines:
            print(line)
        print()

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes an input and returns it.
        :return: User input.
        """
        clear_screen()
        self.display_menu()
        return input(f"{self.menu_data.queries[0]} >> ").strip()


class EndScreenView:
    """
    View class for home menu, interacting with EndScreenController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
        Init method.
        :param menu_data: An instance of MenuData containing info to display.
        """
        self.menu_data = menu_data

    def display_menu(self):
        """
        Displays self.menu_data's lines.
        """
        clear_screen()
        for line in self.menu_data.lines:
            print(line)
