"""
Module for utils used by controllers.
"""
import re


def check_elo_format(elo):
    """
    Checks if Elo entered by user is valid, ie a positive number.
    :param elo: Elo entered by user.
    :return: True if Elo is valid, False if not.
    """
    try:
        elo = int(elo)
    except ValueError:
        return False
    if elo < 0:
        return False
    else:
        return True


def check_name_format(name):
    """
    Checks if a name or description is valid, ie begins with a letter, and is not empty.
    :param name: A string entered by a user.
    :return: True if the string is valid, False if not.
    """
    if len(name) == 0:
        return False

    if re.match(r'[a-zA-Z]', name[0]):
        return True
    else:
        return False


def check_date_format(birth_date):
    """
    Checks if a date is valid, ie in JJ/MM/AAAA format, and plausible:
    Day between 1 and 31, month between 1 and 12, year between 1800 and 2099
    :param birth_date: Date entered by user.
    :return: True if the date is valide, False if not.
    """
    if re.match(r'(0[1-9]|[12][\d]|3[01])/(0[1-9]|1[0-2])/[12][089]\d{2}$', birth_date):
        return True
    else:
        return False


def check_rounds_number_format(rounds_number):
    """
    Checks if rounds number is valid, ie a number greater than 3.
    :param rounds_number: number given by a user.
    :return: True if rounds number is valid, False if not.
    """
    try:
        rounds_number = int(rounds_number)
    except ValueError:
        return False
    if rounds_number <= 3:
        return False
    else:
        return True


def get_player_tournament_scores(player_id, tournament):
    """
    Used by controllers to get the scores of a player in a tournament.
    :param player_id: ID of the player.
    :param tournament: Instance of the tournament.
    :return: A list of all scores of the player in all the matches of a tournament.
    """
    match_scores = []
    for chess_round in tournament.rounds:
        for match in chess_round.matches:
            if player_id == match[0][0]:
                match_scores.append(match[0][1])
            elif player_id == match[1][0]:
                match_scores.append(match[1][1])
    return match_scores
