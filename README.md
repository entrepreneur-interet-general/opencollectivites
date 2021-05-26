# Open Collectivités

![Open Collectivités](open-collectivites.png?raw=true "Open Collectivités")


Simplifier l’accès aux informations financières et statistiques des collectivités locales

[Page de présentation du défi](https://entrepreneur-interet-general.etalab.gouv.fr/defis/2020/open-collectivites.html)

## Install
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

# Notes
Up to version 0.5, the front-end was a separate VueJS project. It is now archived at https://github.com/entrepreneur-interet-general/opencollectivites-front.
