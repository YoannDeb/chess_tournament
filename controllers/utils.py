import re


def check_elo_format(elo):
    try:
        elo = int(elo)
    except ValueError:
        return False
    if elo < 0:
        return False
    else:
        return True


def check_name_format(name):
    if len(name) == 0:
        return False

    if re.match(r'[a-zA-Z]', name[0]):
        return True
    else:
        return False


def check_date_format(birth_date):
    if re.match(r'(0[1-9]|[12][\d]|3[01])/(0[1-9]|1[0-2])/[12][089]\d{2}$', birth_date):
        return True
    else:
        return False


def check_rounds_number_format(rounds_number):
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
