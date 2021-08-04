from model.tournament import Tournament
from model.player import Player


def main():
    # normalement players généré par le menu
    player1 = Player("Vachier-Lagrave", "Maxime", "12/12/12", "M", "2653")
    player2 = Player("Bacrot", "Etienne", "12/12/12", "M", "2452")
    player3 = Player("Mazetovich", "Sebastien", "12/12/12", "M", "1645")
    player4 = Player("Libizeswski", "Fabien", "12/12/12", "M", "2224")
    player5 = Player("Bordi", "Kévin", "12/12/12", "M", "1200")
    player6 = Player("Tkachiev", "Vladimir", "12/12/12", "M", "0850")
    player7 = Player("Cornette", "Mathieu", "12/12/12", "M", "2000")
    players = [player1, player2, player3, player4, player5, player6, player7]

    tournament = Tournament("tournament1", "place1", players, "Bullet", "this is the description of tournament")

    while tournament.round_count < tournament.total_round_number:
        tournament.generate_rounds()
        # input scores, (round_count -1) because round_count already increase in, generate rounds
        print(tournament.rounds[tournament.round_count - 1].name)
        print(tournament.rounds[tournament.round_count - 1].matches)

        for match in tournament.rounds[tournament.round_count - 1].matches:
            match.input_scores()
            print(match)

    tournament.end_tournament()
    print(tournament)
    for tournament_round in tournament.rounds:
        print(tournament_round.matches)


if __name__ == "__main__":
    main()
