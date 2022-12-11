# Epic Events

### Formation Python OC - Projet 12.
#### Mise en place d'une architecture back-end DRF / PostgreSQL


## Installation de PostgreSQL
- Télécharger et installer PSQL : https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Sous Windows : Penser à ajouter les executables PSQL au PATH : https://blog.sqlbackupandftp.com/setting-windows-path-for-postgres-tools
- Se connecter à PSQL :
```bash
psql -U postgres
```
- Entrer le mot de passe défini lors de l'installation
- Créer la base de données :
```bash
CREATE DATABASE epicevents2;
```
- Vérifier que la base de donnée est bien créée
```bash
\l
```
- Quitter PSQL
```bash
\q
```

## Installation de l'application
- Cloner le projet
```bash
git clone https://github.com/CedPi/EpicEvents.git
```

- Se placer dans le répertoire
```bash
cd EpicEvents
```

- Créer l'environnement virtuel
```bash
python -m venv env
```

- Activer l'environnement virtuel (Windows)
```bash
source env/Scripts/activate
```

- Activer l'environnement virtuel (Linux)
```bash
source env/bin/activate
```

- Se placer dans le répertoire epicevents
```bash
cd epicevents
```

- Installer les modules
```bash
pip install -r requirements.txt
```

- S'assurer que le mot de passe de la base de données dans le fichier settings.py corresponde à celui entré lors de l'installation de PostgreSQL
- Créer les tables dans la bases de données
```bash
python manage.py migrate
```

IMPORTANT: Vérifier que le fichier db.json soit bien encodé en UTF-8 en l'ouvrant avec un éditeur de texte (ex: notepad++). Si ce n'est pas le cas, le convertir en UTF-8.
- Importer le jeu de données de base contenant les utilisateurs
```bash
python manage.py loaddata db.json
```

- Lancer le serveur :
```bash
python manage.py runserver
```

## Accès à l'application
- URL de l'application : http://127.0.0.1:8000/
- URL de l'Admin : http://127.0.0.1:8000/admin/
- Accès admin :
  - user: admin
  - mdp: azerty1234
- Mot de passe pour tous les utilisateurs : azerty1234

Utilisateurs déjà créés :
- Manage_A (groupe Manager - staff)
- Sales_A (groupe Sales)
- Sales_B (groupe Sales)
- Support_A (groupe Support)
- Support_B (groupe Support)




