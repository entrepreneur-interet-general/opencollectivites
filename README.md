# Open Collectivités
<img align="right" width="250" src="open-collectivites.png?raw=true" title="Open Collectivités" alt="" />


Open Collectivités est un projet visant à simplifier l’accès aux informations financières et statistiques des collectivités locales. Il est développé au sein de la [Direction générale des collectivités locales](https://www.collectivites-locales.gouv.fr/) (DGCL), dans le cadre d'un défi de la quatrième promotion du programme [Entrepreneur d'intérêt général](https://entrepreneur-interet-general.etalab.gouv.fr/).

→ [Page de présentation du défi](https://entrepreneur-interet-general.etalab.gouv.fr/defis/2020/open-collectivites.html)

## Table des matières
* [Architecture](#architecture)
* [Installation](#installation)
* [Notes](#notes)

<a name="architecture"></a>
## Architecture
### Applications Django
Le site est développé en utilisant le framework [Django](https://www.djangoproject.com/) et est centré autour d'une application principale nommée **core**, accompagnée des applications suivantes :

- **[france-subdivisions](https://github.com/Ash-Crow/django-france-subdivisions)** : Contient des tables reprenant la structure des collectivités locales françaises (communes, EPCI, départements, régions). À terme, des tables de données y seront associées pour gérer des données concernant ces collectivités, importées depuis [data.gouv.fr](https://www.data.gouv.fr/fr/).
- **aspic** : Contient la structure de la base aspic, actuellement utilisée pour les données concernant les collectivités locales. Elle devra disparaître à terme.
- **[django-feed-reader](https://github.com/Ash-Crow/django-feed-reader)** : Un agrégateur de flux RSS permettant de récupérer les métadonnées sur les publications des différents sites des services statistiques des ministères (SSM). Il est prévu de remplacer ce fonctionnement par une application récupérant ces métadonnées sur la future version de la [bibliothèque nationale de la statistique publique](https://www.insee.fr/fr/information/1303569), en s'appuyant sur l'[API de Gallica](https://api.bnf.fr/fr/api-gallica-de-recherche)
- **dsfr** : Permet d'utiliser facilement le [système de design de l'État](https://gouvfr.atlassian.net/wiki/spaces/DB/overview) dans des templates Django.

![Application schema](docs/oc-app-schema.png?raw=true "Application schema")

### Librairies tierces
Le site utilise des contenus provenant des librairies tierces suivantes :
- [Remix Icon](https://remixicon.com/) : icônes
- [unDraw](https://undraw.co/) : illustrations
- [VueJS](https://vuejs.org/) : Scripts Javascript sur le front-end

### Structure du dépôt
En plus des applications déjà citées, le dépôt contient les répertoires suivants :
- **config** : le projet Django proprement dit
- **devops** : scripts de maintenance, et fichiers de configuration pour [NGINX](https://www.nginx.com/) et [Gunicorn](https://gunicorn.org/)
- **docs** : la documentation du projet

<a name="installation"></a>
## Installation
### Packages
- `sudo apt install python3-dev python3-venv postgresql libpq-dev`

### Prepare database
- Create a PostgreSQL database and user
```
sudo -u postgres psql
postgres=# CREATE DATABASE <db_name>;
postgres=# CREATE USER <db_user> WITH ENCRYPTED PASSWORD '<db_password>';
postgres=# GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <db_user>;
```

- Create the Unaccent extension manually

```
postgres=# \c <db_name>
<db_name>=# CREATE EXTENSION  IF NOT EXISTS unaccent;
```

### Install the project
#### Clone the project and get the submodules
- `git clone` this repository somewhere and `cd` in.
- `git submodule init`
- `git submodule update`

#### Initiate local settings
- `cp settings_local.py.sample settings_local.py`
- Fill the `settings_local.py` file

#### Create and activate the virtualenv with the dependencies
- `pipenv install`
- `pipenv shell`
 
#### Initiate the database and static files for Django
- `python3 manage.py migrate`
- `python3 manage.py collectstatic`

#### Create the superuser
- ` python manage.py createsuperuser`

### Launch it
 - `python3 manage.py runserver`

### Parameters for launching with Gunicorn/nginx/systemd
#### Gunicorn
 - `cd devops`
 - `cp .env.sample .env`
 - Fill the `.env` file
 - `chmod ug+x gunicorn_start.sh`
 - `chmod ug+x update.sh`

#### Systemd
 - Copy `devops/config_files/gunicorn.service.sample` to `/etc/systemd/system/gunicorn-<projectname>.service` and fill the correct data

#### Nginx
 - Create the SSL certificate
 - Copy `devops/config_files/nginx-conf.sample` to `/etc/nginx/sites-available/<projectname>.conf` and fill the correct data
 - Make a symbolic link to the config file in the sites-enabled folder
 - Test the configuration with `nginx -t`
 - If it is ok, relaunch nginx

<a name="notes"></a>
## Notes
- Versionning numbers follows the principles of [Semantic versioning](https://semver.org/)
- Up to version 0.5, the front-end was a separate VueJS project. It is now archived at https://github.com/entrepreneur-interet-general/opencollectivites-front.
