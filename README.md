[![Made with Django](https://img.shields.io/badge/Made%20with-Django-0C4B33.svg)](https://www.djangoproject.com/)
[![Made with Wagtail](https://img.shields.io/badge/Made%20with-Wagtail-0F7676.svg)](https://wagtail.io/)
[![GitHub license](https://img.shields.io/github/license/entrepreneur-interet-general/opencollectivites.svg)](https://github.com/entrepreneur-interet-general/opencollectivites/blob/master/LICENSE)
[![Website open-collectivites.fr](https://img.shields.io/website.svg?down_color=red&down_message=down&up_color=green&up_message=up&url=https%3A%2F%2Fwww.open-collectivites.fr)](https://www.open-collectivites.fr)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=entrepreneur-interet-general_opencollectivites&metric=alert_status)](https://sonarcloud.io/dashboard?id=entrepreneur-interet-general_opencollectivites)
[![CodeQL](https://github.com/entrepreneur-interet-general/opencollectivites/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/entrepreneur-interet-general/opencollectivites/actions/workflows/codeql-analysis.yml)

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

- **[django-francedata](https://github.com/entrepreneur-interet-general/django-francedata/)** : Contient des tables reprenant la structure des collectivités locales françaises (communes, EPCI à fiscalité propre, départements, régions) ainsi que des tables de données associées pour gérer des données concernant ces collectivités, importées depuis [data.gouv.fr](https://www.data.gouv.fr/fr/) et [banatic](https://www.banatic.interieur.gouv.fr/V5/accueil/index.php).
- **aspic** : Contient la structure de la base aspic (Application de la DGCL sur les intercommunalités, destinée aux préfectures), actuellement utilisée pour les données concernant les collectivités locales. Elle est appelée à disparaître à terme.
- **dashboard** : Contient les personnalisations des panneaux d’administration de Django (dans `templates/admin`) et Wagtail (dans `templates/wagtailadmin` et `wagtail_hooks.py`)
- **[django-feed-reader](https://github.com/Ash-Crow/django-feed-reader)** : Un agrégateur de flux RSS permettant de récupérer les métadonnées sur les publications des différents sites des services statistiques des ministères (SSM). Il est prévu de remplacer ce fonctionnement par une application récupérant ces métadonnées sur la future version de la [bibliothèque nationale de la statistique publique](https://www.insee.fr/fr/information/1303569), en s'appuyant sur l'[API de Gallica](https://api.bnf.fr/fr/api-gallica-de-recherche)
- **[django-dsfr](https://github.com/entrepreneur-interet-general/django-dsfr)** : Permet d'utiliser facilement le [système de design de l'État](https://www.systeme-de-design.gouv.fr/) dans des templates Django.
- **pages** : Application basée sur le moteur de CMS [Wagtail](https://wagtail.io/) qui gère les pages dynamiques du site, dont la page d’accueil.

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
