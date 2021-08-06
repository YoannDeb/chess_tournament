from tinydb import TinyDB

from model.tournament import Tournament
from model.player import Player


def save_tournament(tournament):
    tournament.save()
    for player in tournament.tournament_players():
        player.save()


def main():

    # if database exist : load database

    # normalement players généré par le menu
    player1 = Player("Maxime", "Vachier-Lagrave", "12/12/12", "M", "2653")
    player2 = Player("Etienne", "Bacrot", "12/12/12", "M", "2452")
    player3 = Player("Sebastien", "Mazetovich", "12/12/12", "M", "1645")
    player4 = Player("Fabien", "Libizeswski", "12/12/12", "M", "2224")
    player5 = Player("Kévin", "Bordi", "12/12/12", "M", "1200")
    player6 = Player("Vladimir", "Tkachiev", "12/12/12", "M", "0850")
    player7 = Player("Mathieu", "Cornette", "12/12/12", "M", "2000")
    player8 = Player("Alireza", "Firouja", "12/12/12", "M", "2500")
    players = [player1, player2, player3, player4, player5, player6, player7, player8]

    print(player1.id)

    # serialized_players = []
    # for player in players:
    #     serialized_players.append(player.serialize())
    #
    # db = TinyDB('db.json')
    # players_table = db.table('players')
    # players_table.truncate()
    # players_table.insert_multiple(serialized_players)

    for player in players:
        player.save()
        print(player.id)

    players_id = [player.id for player in players]

    # create tournament
    tournament = Tournament("tournament1", "place1", players_id, "Bullet", "this is the description of tournament")
    tournament.generate_first_round()

    while len(tournament.rounds) < tournament.total_round_number:
        tournament.generate_following_round()
        print("end of ", tournament.rounds[-1].name)
        print(tournament.rounds[-1].matches)
        print(tournament)

        # for match in tournament.rounds[-1].matches:
        #     match.input_scores()
        #     print(match)

    tournament.end_tournament()
    print(tournament)

    # print("tournament", tournament)
    # # serialization test
    # serialized_tournament = tournament.serialize()
    # print("serialized_tournament", serialized_tournament)
    # tournament2 = Tournament.deserialize(serialized_tournament)
    # print("serialized then deserialized tournament", tournament2)
    # print("tournament rounds", tournament.rounds)
    # for tournament_round in tournament.rounds:
    #     print(tournament_round.matches)


if __name__ == "__main__":
    main()
