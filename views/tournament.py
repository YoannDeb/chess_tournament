"""
Views classes for tournament management.
"""
from views.utils import clear_screen


class InfoTournamentCreationView:
    """
    View class for tournament creation's simple info, interacting with TournamentCreationController.
    A MenuData instance is used by the controller to transmit information to the view.
    """
    def __init__(self, menu_data):
        """
         Init method.
         :param menu_data: An instance of MenuData containing info to display.
         """
        self.menu_data = menu_data

    def display(self):
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
        self.display()
        return input(f"{self.menu_data.queries[0]} >> ").strip()


class TooMuchRoundsView:
    """
    View class for tournament creation when too much rounds are selected.
    Interacting with TournamentCreationController.too_much_rounds().
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
        """
        for line in self.menu_data.lines:
            print(line)
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes an user input and return choice if the input is in possible menu choices.
        :return: A string depending on the choice of the user ("players" or "rounds").
        """
        clear_screen()
        self.display_menu()
        while True:
            choice = input(f"{self.menu_data.input_message} >> ").strip()
            if choice in self.menu_data.entries:
                return self.menu_data.entries[choice][1]
            clear_screen()
            self.display_menu()
            print("/!\\ Choix invalide /!\\")


class TimeControlMenuView:
    """
    View class for tournament creation when the time control have to be choose.
    Interacting with TournamentCreationController.time_control().
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
        """
        for line in self.menu_data.lines:
            print(line)
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes an user input and return choice if the input is in possible menu choices.
        :return: A string depending on the choice of the user.
        """
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
    """
    View class for tournament recovery when a tournament have been interrupted.
    Interacting with TournamentCreationController.too_much_rounds().
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

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes any input and returns nothing (no choice or info needed here).
        """
        clear_screen()
        self.display_menu()
        input(f"{self.menu_data.input_message} >> ")


class FillRoundView:
    """
    Round's matches view, interacting with TournamentController.
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
        :return: A tuple of the match, or "end" string depending on the choice of the user.
        """
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
    """
    View class for scores filling for one match, interacting with TournamentController.
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
        """
        for line in self.menu_data.lines:
            print(line)
        for key in self.menu_data.entries:
            print(f"{key}: {self.menu_data.entries[key][0]}")
        print()

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes an user input and return choice if the input is in possible menu choices.
        :return: A tuple with scores of the match depending on the choice of the user.
        """
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
    """
    Tournament ranking view, displayed at each end of round, interacting with TournamentController.
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

    def get_user_choice(self):
        """
        Clears screen then displays menu content.
        Finally takes any input and returns nothing (no choice or info needed here).
        """
        clear_screen()
        self.display_menu()
        input(f"{self.menu_data.input_message} >> ")
