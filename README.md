# projet_info707_bot_discord_reunion_resume

## Intro

Ce projet consiste en un bot Discord et une application web basée sur Django. Le bot Discord est conçu pour enregistrer les conversations vocales lors des réunions, les transcrire en texte et générer des résumés ainsi que des fichiers PDF contenant ces transcriptions et résumés. Parallèlement, l'application web Django permet de gérer les utilisateurs et les résumés de réunions, offrant une interface conviviale pour accéder et organiser les informations générées par le bot. Ensemble, ces deux composants fournissent une solution complète pour la gestion et la documentation des réunions sur Discord. Les données sont stockées dans une base de données SQLite qui est utilisée par les deux composantes.

### Fonctionnalités du Bot Discord

#### Les commandes du bot Discord

L'objectif du bot Discord est de récupérer les données et les stocker dans la base de données. Le bot, une fois installé, permet d'exécuter les commandes suivantes :

- `/join_channel` : Permet de rejoindre un channel vocal de l'utilisateur.
- `/leave_channel` : Permet de quitter un channel vocal.
- `/start title` : Permet de commencer l'enregistrement de la conversation et de lui donner un titre.
- `/stop_recording` : Permet d'arrêter l'enregistrement de la conversation.
- `/schedule channel date time` : Permet de planifier une réunion.
- `/generate_all_pdf title` : Permet de générer un fichier PDF contenant les transcriptions et le résumé de la réunion.
- `/generate_message_pdf title` : Permet de générer un fichier PDF contenant les messages de la réunion.
- `/generate_resume_pdf title` : Permet de générer un fichier PDF contenant le résumé de la réunion.
- `/help` : Permet d'afficher les commandes disponibles.

#### Fonctionnement du bot Discord

Pour la transcription des audio en texte, le bot utilise la librairie `whisper`. Les audios sont découpés comme une conversation par message, puis un résumé est généré à partir de ces messages. Les résumés sont effectués en utilisant la librairie `Llama` comme modèle de langage, avec un prompt personnalisé. Les deux parties sont executées en local, permetant de ne pas avoir de dépendances externes; et de garantir la confidentialité des données.

### Fonctionnalités de l'application Django

#### Gestion des utilisateurs :
- Authentification via Discord.
- Affichage du profil utilisateur avec les informations de Discord (nom, avatar, etc.).
- Liste des réunions auxquelles l'utilisateur a participé.

#### Gestion des réunions :
- Création et affichage des résumés de réunions.
- Affichage des messages associés à chaque réunion.
- Génération de fichiers PDF contenant les transcriptions et résumés des réunions.

#### Pages principales :
- **Page d'accueil** : Présente les fonctionnalités de l'application et permet d'ajouter le bot ou de consulter les résumés.
- **Page de tutoriel** : Fournit des instructions sur l'utilisation de l'application.
- **Page de profil** : Affiche les informations de l'utilisateur et les réunions récentes.
- **Page des résumés** : Liste tous les résumés de réunions disponibles.
- **Page de résumé détaillé** : Affiche les détails d'un résumé de réunion spécifique, y compris les participants et les messages.

#### Fonctionnalités supplémentaires :
- Génération de heatmaps pour visualiser la répartition des réunions au cours de l'année.
- Exportation des résumés et transcriptions en fichiers PDF.

#### Exemple de pages disponibles :
- **home.html** : Page d'accueil avec une présentation de l'application.
- **tutorial.html** : Page de tutoriel pour guider les utilisateurs.
- **profile.html** : Page de profil utilisateur avec les informations de Discord et les réunions récentes.
- **summaries.html** : Page listant tous les résumés de réunions.
- **summary.html** : Page détaillant un résumé de réunion spécifique.

Ces fonctionnalités permettent une gestion complète et intuitive des réunions et des utilisateurs, offrant une interface conviviale pour accéder et organiser les informations générées par le bot Discord.

## Installation

Super Utilisateur :

```
    username : huynh
    email : raphaellehuynh@gmail.com
    password : 0000
```


### Lancement du bot discord

Pour lancer le bot discord, il faut exécuter le fichier `bot.py` qui se trouve dans le dossier `bot_discord`.

```bash
source ./.venv/bin/activate
cd bot_discord
python bot.py
```

### Lancement de l'application Django

Pour lancer l'application Django, il faut exécuter le fichier `manage.py` qui se trouve à la racine du projet.

```bash
source ./.venv/bin/activate
cd app
python manage.py runserver
```