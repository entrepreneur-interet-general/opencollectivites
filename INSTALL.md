# Installation
Ce document décrit la procédure intégrale d'installation d'Open Collectivités sur un serveur Ubuntu 18.04 LTS

## Paramétrage initial du serveur
- Installer les paquets de base
    - `sudo apt install python3-dev python-pip postgresql libpq-dev postgis postgresql-10-postgis-2.4` 
 - Installer poetry, cf. https://python-poetry.org/docs/

## Installer la base Aspic

- Cf documentation interne dédiée


## Préparer la base de données dédiée
- Créer une base de données PostgreSQL et l'utilisateur associé
```
sudo -u postgres psql
postgres=# CREATE DATABASE <db_name>;
postgres=# CREATE USER <db_user> WITH ENCRYPTED PASSWORD '<db_password>';
postgres=# GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <db_user>;
```

- Ajouter l'extension Unaccent manuellement

```
postgres=# \c <db_name>
<db_name>=# CREATE EXTENSION  IF NOT EXISTS unaccent;
```

## Installer le projet
### Cloner le projet et récupérer les sous-modules
- `git clone` ce répertoire quelque part et `cd` dedans.
- `git submodule init`
- `git submodule update`

### Régler les paramètres locaux
- `cp settings_local.py.sample settings_local.py`
- Remplir le fichier `settings_local.py`

### Créer et activer l'environnement virtuel et installer les dépendances
- `poetry install`
- `poetry shell`
 
### Installer la structure de base de données et récupérer les fichiers statiques
- `python3 manage.py migrate`
- `python3 manage.py collectstatic`

### Créer le super-utilisateur
- ` python manage.py createsuperuser`

### Lancer le projet
 - `python3 manage.py runserver`
 
 En local pour le développement, c'est fini. Pour l'installation en production / préproduction, suivre la suite de cette documentation

## Paramétrer le lancement avec Green Unicorn/NGINX/systemd
#### Gunicorn
 - `cd devops`
 - `cp .env.sample .env`
 - Remplir le fichier `.env`
 - `chmod ug+x gunicorn_start.sh`
 - `chmod ug+x update.sh`

#### Systemd
 - Copier `devops/config_files/gunicorn.service.sample` vers `/etc/systemd/system/gunicorn-<projectname>.service` et remplir les paramètres

#### NGINX
 - Créer le certificat SSL (avec LetsEncrypt)
 - Copier `devops/config_files/nginx-conf.sample` vers `/etc/nginx/sites-available/<projectname>.conf` et remplir les paramètres
 - Faire un lien symbolique vers le fichier de configuration dans le répertoire `sites-enabled`
 - Tester la configuration avec `nginx -t`
 - Si tout est OK, relancer NGINX

