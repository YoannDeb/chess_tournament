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
