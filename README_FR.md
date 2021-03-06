# chess_tournament

English readme : [README.md](https://github.com/YoannDeb/chess_tournament/blob/master/README.md)

Projet exercice pour créer et gérer des tournois en utilisant le système suisse d'appariement.

L'interface est en français.

Ceci est le projet n°4 de la formation Open Classrooms "DA Python".

## Création de l'environnement virtuel, téléchargement et execution du programme :

Python 3 (testé sur 3.9.5), git et venv doivent être installés.

Ouvrir un terminal, se placer dans le dossier voulu et lancer les commandes suivantes :

* Sur Linux ou macOS :
```bash
git clone https://github.com/YoannDeb/chess_tournament.git
cd chess_tournament
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python chess_tournament.py
```

* Sur Windows :
```bash
git clone https://github.com/YoannDeb/chess_tournament.git
cd chess_tournament
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python chess_tournament.py
```

## Comment utiliser chess_tournament ?
### Créer des joueurs :

- Dans le menu principal, tapez `j` et pressez `Entrée` pour entrer dans le "Menu joueurs".
Vous verrez alors une liste des joueurs déjà créés. Vous pouvez sélectionner un joueur pour modifier son classement Elo.

- Tapez `c` et pressez `Entrée` pour entrer dans le menu "Création joueur".

- Renseignez les champs requis.

### Créer un tournoi :

- Dans le menu principal, tapez `t` et pressez `Entrée` pour entrer dans le "Menu tournois".
Vous verrez alors une liste des tournois passés. Vous pouvez sélectionner un tournoi pour afficher plus de renseignements sur celui-ci.

- Tapez `c` et pressez `Entrée` pour entrer dans le menu "Création tournoi".

- Renseignez les champs requis.

- Le tournoi va commencer. Le programme va montrer les matchs de la première ronde.

- Vous pouvez entrer le résultat d'un match en le sélectionnant.

- Une fois que tous les résultats ont été renseignés, vous pouvez terminer la ronde en tapant `t` puis `Entrée`.

- Le programme va afficher le classement à ce stade du tournoi.

- Vous pouvez alors presser la touche `Entrée` pour répéter le processus pour la ronde suivante.

- À la fin de la dernière ronde, le classement final sera affiché. Vous pourrez alors presser la touche `Entrée` pour revenir au menu principal.

### Sauvegarde et base de données :

Par défaut, la base de donnée sera enregistrée dans un fichier `db.json`, dans un dossier `database` à la racine du programme.

Vous pouvez changer le nom du fichier de base de données utilisé avec l'argument `--database` ou `-d`.

Exemple: `$ python chess_tournament.py -d db2.json`

Si le fichier de base de données (et le dossier database) n'existent pas, il sera créé.

Tous les changements (Création d'un joueur, modification d'un joueur, création d'un tournoi, fin d'une ronde...) seront sauvegardés automatiquement dans la base de donnée.

Si le programme est fermé alors qu'un tournoi n'était pas terminé, le tournoi reprendra après la dernière entrée (typiquement le résultat d'un match) à sa reprise. 

## Rapport flake8 et flake8-html

### Générer un rapport au format HTML :

* Ouvrez un terminal dans le dossier chess_tournament et assurez-vous d'avoir activé l'environnement virtuel.

```bash
flake8 --format=html --htmldir=flake8 --max-line-length=119 --exclude=winenv/,env/
```

* Le rapport est consultable dans le dossier flake8 nouvellement créé.
