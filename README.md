# chess_tournament

Readme en français : [README_FR.md](https://github.com/YoannDeb/chess_tournament/blob/master/README_FR.md)

Training Project to create and handle chess tournaments with Swiss pairing.

The interface is in French langage.

Part of [Open Classrooms](https://openclassrooms.com) "DA Python" formation, 4th Project.

## Creating Virtual environment, downloading and running the program:

You need Python 3 (tested on 3.9.5), git and venv installed on your machine.

Open a terminal and navigate into the folder you want chess_tournament to be downloaded, and run the following commands:

* On Linux or macOS:
```bash
git clone https://github.com/YoannDeb/chess_tournament.git
cd chess_tournament
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python chess_tournament.py
```

* On Windows:
```bash
git clone https://github.com/YoannDeb/chess_tournament.git
cd chess_tournament
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python chess_tournament.py
```

## How to use chess_tournament?
### Create players:

- In the main menu, type `j` then `Enter` to enter "Menu joueurs" (Players menu).
You will see a list of already created players. You can select a player to modify it's elo ranking.

- Type `c` then `Enter` to enter "Création de joueur" ("Player creation) menu.

- Fill the required fields.

### Create a tournament:

- In the main menu, type `t` then `Enter` to enter "Menu tournois" (Tournaments menu).
You will see a list of all past tournaments. You can select a tournament to show details about it.

- Type `c` then `Enter` to enter "Création de tournoi" (Tournament creation) menu.

- Fill the required fields.

- The tournament will begin. The program will show the matches for the first round.

- You can then enter the results by selecting a match.

- Once all results have been filled, you can finish the round by typing `t` then press `Enter`.

- It will show the ranking at this stage of the tournament.

- You can press `Enter` to repeat the process for the next round till the final one.

- At the end of the last round the program will show the definitive ranking.
You can press `Enter` to return to the main menu.

### Save state and database:
 
By default, the database file will be registered in a db.json file in a database folder at the root of the main program.

You can change the name of the database file with the `--databse` or `-d` argument.

Example: `$ python chess_tournament.py -d db2.json`

if the database file (and folder) does not exist, it will be created.

All changes (Player creation, player modification, tournament creation, end of a round...) are immediately saved to the database.

If a tournament was not finished and the program closed, the tournament will be recovered where it was after last entry (typically a match result).

## Flake8 and flake8-html report

### Generate an HTML report:

* Open a terminal in chess_tournament folder and make sure virtual environment is activated.

```bash
flake8 --format=html --htmldir=flake8 --max-line-length=119 --exclude=winenv/,env/
```

* Report will be generated in flake8 folder.
