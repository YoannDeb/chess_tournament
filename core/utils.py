import os

from models.player import Player


def clear_screen():
    os.system('cls||clear')  # todo test on linux


class MenuData:
    def __init__(self):
        self.entries = {}
        self.lines = []
        self.queries = []
        self.input_message = None
        self.autokey = 1

    def add_entry(self, key, menu_option, destination_controller):
        if key == "auto":
            key = self.autokey
            self.autokey += 1
            self.entries[str(key)] = (menu_option, destination_controller, "top_menu")
        else:
            self.entries[str(key)] = (menu_option, destination_controller, "bottom_menu")

    def add_line(self, text):
        self.lines.append(text)

    def add_query(self, text):
        self.queries.append(text)

    def add_input_message(self, text):
        self.input_message = text

    def clear_data(self):
        self.entries = {}
        self.lines = []
        self.queries = []
        self.input_message = None
        self.autokey = 1

    def add_row(self):
        pass


def get_player_tournament_scores(player_id, tournament):
    match_scores = []
    for chess_round in tournament.rounds:
        for match in chess_round.matches:
            if player_id == match[0][0]:
                match_scores.append(match[0][1])
            elif player_id == match[1][0]:
                match_scores.append(match[1][1])
    return match_scores


def check_elo_format(elo):
    try:
        elo = int(elo)
    except ValueError:
        return False
    if elo < 0:
        return False
    else:
        return True
