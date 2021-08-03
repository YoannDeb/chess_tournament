class Player:
    def __init__(self, surname, name, birth_date, sex, elo_ranking):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.sex = sex
        self.elo_ranking = elo_ranking
        self.tournament_score = 0

    def __repr__(self):
        return repr(f"{self.name} {self.surname}, né le {self.birth_date}, sexe : {self.sex}, classement Elo : {self.elo_ranking}, score dans le tournoi : {self.tournament_score}")

    def modify_elo(self, new_elo):
        self.elo_ranking = new_elo

    def modify_tournament_score(self, last_match_score):
        self.tournament_score += last_match_score

    def serialize(self):
        pass

    def deserialize(self):
        pass
