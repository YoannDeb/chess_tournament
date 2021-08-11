from models.player import Player
from models.tournament import Tournament

DATABASE_FILE = 'db.json'

def main():
#
#     # if database exist : load database
#
    # normalement players généré par le menu
    player1 = Player("Vachier-Lagrave", "Maxime", "12/12/12", "M", "2653")
    player2 = Player("Bacrot", "Etienne", "12/12/12", "M", "2452")
    player3 = Player("Mazetovich","Sebastien",  "12/12/12", "M", "1645")
    player4 = Player("Libizeswski", "Fabien", "12/12/12", "M", "2224")
    player5 = Player("Bordi", "Kévin", "12/12/12", "M", "1200")
    player6 = Player("Tkachiev", "Vladimir", "12/12/12", "M", "0850")
    player7 = Player("Cornette", "Mathieu", "12/12/12", "M", "2000")
    player8 = Player("Firouja", "Alireza", "12/12/12", "M", "2500")
#
#     # test = player5.serialize()
#     # print(test)
#     # playertest = Player.deserialize(test)
#     # print(playertest)
#
    players = [
        player1, player2, player3, player4,
        player5, player6, player7, player8
    ]
#
#     # serialized_players = []
#     # for player in players:
#     #     serialized_players.append(player.serialize())
#     #
#     # db = TinyDB('db.json')
#     # players_table = db.table('players')
#     # players_table.truncate()
#     # players_table.insert_multiple(serialized_players)
#
    for player in players:
        player.save(DATABASE_FILE)
        # print(player.id)
#
#     players = Player.get_all('db.json')
#     print(players)
#
#     breakpoint()
#
#
    players_id = [player.id for player in players]
#
#     # create tournament
    tournament = Tournament("tournament1", "place1", players_id, "Bullet", "this is the description of tournament")
    tournament.sort_players_id_by_rank(DATABASE_FILE)
    tournament.generate_first_round()
    tournament.save(DATABASE_FILE)
    print(f"{tournament.rounds[-1].name} generated with following pairs :")
    for match in tournament.rounds[-1].matches:
        print(f"{Player.get(match[0][0], DATABASE_FILE).name} vs {Player.get(match[1][0], DATABASE_FILE).name}")
    input("press enter to input scores")
    tournament.rounds[-1].input_scores(DATABASE_FILE)
    tournament.sort_players_id_by_rank(DATABASE_FILE)
    tournament.save(DATABASE_FILE)
#
    while len(tournament.rounds) < tournament.total_round_number:
        tournament.generate_following_round(DATABASE_FILE)
        tournament.save(DATABASE_FILE)
        print(f"{tournament.rounds[-1].name} generated with following pairs :")
        for match in tournament.rounds[-1].matches:
            print(f"{Player.get(match[0][0], DATABASE_FILE).name} vs {Player.get(match[1][0], DATABASE_FILE).name}")
        input("press enter to input scores")
        tournament.rounds[-1].input_scores(DATABASE_FILE)
        tournament.sort_players_id_by_rank(DATABASE_FILE)
        tournament.save(DATABASE_FILE)
        print("end of ", tournament.rounds[-1].name)
        print(tournament.rounds[-1].matches)
        print(tournament)

    tournament.end_tournament()
    tournament.save(DATABASE_FILE)
#
    print("tournament", tournament)
#     # serialization test
#     serialized_tournament = tournament.serialize()
#     print("serialized_tournament", serialized_tournament)
#     tournament2 = Tournament.deserialize(serialized_tournament)
#     print("serialized then deserialized tournament", tournament2)
#     print("tournament rounds", tournament.rounds)
#     for tournament_round in tournament.rounds:
#         print(tournament_round.matches)


if __name__ == "__main__":
    main()
