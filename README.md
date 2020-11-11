# Open Collectivités

![Open Collectivités](open-collectivites.png?raw=true "Open Collectivités")


Simplifier l’accès aux informations financières et statistiques des collectivités locales

[Page de présentation du défi](https://entrepreneur-interet-general.etalab.gouv.fr/defis/2020/open-collectivites.html)

## Install
### Packages
- `apt install python3-dev python3-venv`postgresql

### Prepare database
- For now, the default SQLite3 database will suffice.

### Install the project
#### Clone the project and get the submodules
- `git clone` this repository somewhere and `cd` in.
- `git submodule init`
- `git submodule update`

#### Initiate local settings
- `cp settings_local.py.sample settings_local.py`
- Fill the `settings_local.py` file

#### Create and activate the virtualenv
- `python3 -m venv venv`
- `source venv/bin/activate`

#### Install the Python dependancies 
- `pip install wheel`
- `pip install -r requirements.txt`

#### Initiate the database and static files for Django
- `python3 manage.py migrate`
- `python3 manage.py collectstatic`

#### Create the superuser
- ` python manage.py createsuperuser`

### Launch it
 - `python3 manage.py runserver`
