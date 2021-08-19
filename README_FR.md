# chess_tournament

Projet exercice pour créer et gérer des tournois en utilisant le sytème suisse d'appariement.

L'interface est en français.

Ceci est le projet n°4 de la formation Open Classrooms "DA Python".

## Création de l'environnement virtuel, téléchargement et execution du programme

Python 3 (testé sur 3.9.5) et git doivent être installés.

Ouvrir un terminal, se placer dans le dossier voulu et lancer les commandes suivantes :

* Sur Linux ou MacOS:
```
git clone https://github.com/YoannDeb/chess_tournament.git
cd chess_tournament
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python chess_tournament.py
```

* Sur Windows:
```
git clone https://github.com/YoannDeb/chess_tournament.git
cd chess_tournament
python -m venv env
env\Scripts\activate.bat
pip install -r requirements.txt
python chess_tournament.py
```

## Comment utiliser chess_tournament?
### Créer des joueurs:

- Dans le menu principal, tapez "j" et pressez "Entrée" pour entrer dans le "Menu joueurs".
Vous verrez alors une liste des joueurs déjà créés. Vous pouvez selectionner un joueur pour modifier son classement Elo.

- Tapez "c" et pressez "Entrée" pour entrer dans le menu "Création joueur".

- Renseignez les champs requis.

### Créer un tournoi:

- Dans le menu principal, tapez "t" et pressez "Entrée" pour entrer dans le "Menu tournois".
Vous verrez alors une liste des tournois passés. Vous pouvez selectionner un tournoi pour afficher plus de renseignements sur celui-ci.

- Tapez "c" et pressez "Entrée" pour entrer dans le menu "Création tournoi".

- Renseignez les champs requis.

- Le tournoi va commencer. Le programme va montrer les matchs de la première ronde.

- Vous pouvez entrer le resultat d'un match en le sélectionnant.

- Une fois que tous les résultats ont été renseignés, vous pouvez terminer la ronde en tapant "t" puis "Entrée".

- Le programme va afficher le classement à ce stade du tournoi.

- Vous pouvez alors presser la touche "Entrée" pour répéter le processus pour la ronde suivante.

- A la fin de la dernière ronde, le classement final sera affiché. Vous pourrez alors presser la touche "Entrée" pour revenir au menu principal.

### Sauvegarde et base de données:

Par défaut, la base de donnée sera enregistrée dans un fichier db.json, dans un dossier "database" à la racine du programme.

Vous pouvez changer le nom du fichier de base de données utilisé avec l'argument --database ou -d.

Exemple: python chess_tournament.py -d db2.json

Si le fichier de base de données (et le dossier database) n'existent pas, il sera créé.

Tous les changements (Création d'un joueur, modification d'un joueur, création d'un tournoi, fin d'une ronde...) seront sauveagardés automatiquement dans la base de donnée.

Si le programme est fermé alors qu'un tournoi n'était pas terminé, le tournoi reprendra après la dernière entrée (typiquement le résultat d'un match) à sa reprise. 

### Flake 8
TODO
