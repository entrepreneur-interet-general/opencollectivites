# Open Collectivités
<img align="right" width="250" src="open-collectivites.png?raw=true" title="Open Collectivités" alt="" />


**Open Collectivités** est un portail web visant à simplifier l’accès aux informations statistiques des collectivités locales. Il est développé au sein de la [Direction générale des collectivités locales](https://www.collectivites-locales.gouv.fr/) (DGCL), dans le cadre d'un défi de la quatrième promotion du programme [Entrepreneur d'intérêt général](https://entrepreneur-interet-general.etalab.gouv.fr/).

- [Page de présentation du défi](https://entrepreneur-interet-general.etalab.gouv.fr/defis/2020/open-collectivites.html)
- [Voir le portail Open Collectivités](https://www.open-collectivites.fr)

## Table des matières
* [Architecture](#architecture)
* [Installation](#installation)
* [Notes](#notes)

<a name="architecture"></a>
## Architecture
### Applications Django
Le site est développé en utilisant le framework [Django](https://www.djangoproject.com/) et est centré autour d'une application principale nommée **core**, accompagnée des applications suivantes :

- **[france-subdivisions](https://github.com/Ash-Crow/django-france-subdivisions)** : Contient des tables reprenant la structure des collectivités locales françaises (communes, EPCI à fiscalité propre, départements, régions). À terme, des tables de données y seront associées pour gérer des données concernant ces collectivités, importées depuis [data.gouv.fr](https://www.data.gouv.fr/fr/).
- **aspic** : Contient la structure de la base aspic (Application de la DGCL sur les intercommunalités, destinée aux préfectures), actuellement utilisée pour les données concernant les collectivités locales. Elle devra disparaître à terme.
- **[django-feed-reader](https://github.com/Ash-Crow/django-feed-reader)** : Un agrégateur de flux RSS permettant de récupérer les métadonnées sur les publications des différents sites des services statistiques des ministères (SSM). Il est prévu de remplacer ce fonctionnement par une application récupérant ces métadonnées sur la future version de la [bibliothèque nationale de la statistique publique](https://www.insee.fr/fr/information/1303569), en s'appuyant sur l'[API de Gallica](https://api.bnf.fr/fr/api-gallica-de-recherche)
- **dsfr** : Permet d'utiliser facilement le [système de design de l'État](https://gouvfr.atlassian.net/wiki/spaces/DB/overview) dans des templates Django.

![Application schema](docs/oc-app-schema.png?raw=true "Application schema")

### Structure du dépôt
En plus des applications déjà citées, le dépôt contient les répertoires suivants :
- **config** : le projet Django proprement dit
- **devops** : scripts de maintenance, et fichiers de configuration pour [NGINX](https://www.nginx.com/) et [Gunicorn](https://gunicorn.org/)
- **docs** : la documentation du projet

### Librairies tierces
Le site utilise des contenus provenant des librairies tierces suivantes :
- [Remix Icon](https://remixicon.com/) : icônes
- [unDraw](https://undraw.co/) : illustrations
- [VueJS](https://vuejs.org/) : Scripts Javascript sur le front-end

<a name="installation"></a>
## Installation
- Voir la [documentation dédiée](INSTALL.md).

<a name="notes"></a>
## Notes
- Les numéros de versions suivent les principes du [versionnage sémantique](https://semver.org/)
- Jusqu'à la version 0.5, le front-end était un projet séparé, entièrement en VueJS. Il est maintenant archivé sur https://github.com/entrepreneur-interet-general/opencollectivites-front.
