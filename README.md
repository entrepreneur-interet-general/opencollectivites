# Open Collectivités

![Open Collectivités](open-collectivites.png?raw=true "Open Collectivités")


Simplifier l’accès aux informations financières et statistiques des collectivités locales

[Page de présentation du défi](https://entrepreneur-interet-general.etalab.gouv.fr/defis/2020/open-collectivites.html)

## Install
### Packages
- `apt install python3-dev python3-venv`

### Prepare database
- For now, the default SQLite3 database will suffice.

### Install the project

- `git clone` this repository somewhere and `cd` in.
- `cp settings_local.py.sample settings_local.py`
- Fill the `settings_local.py` file
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install wheel`
- `pip install -r requirements.txt`
- `python3 manage.py migrate`
- `python3 manage.py collectstatic`

### Launch it
 - `python3 manage.py runserver`
