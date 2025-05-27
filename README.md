# TravelBooking – Plateforme de Réservation de Voyages

**TravelBooking** est une application web développée avec Django qui centralise les offres de voyages organisés et permet aux utilisateurs de réserver facilement leurs séjours. Ce projet a été réalisé dans le cadre d'un projet universitaire.

## 🚀 Fonctionnalités principales

* Recherche de voyages avec filtres (destination, prix, durée).
* Détails complets pour chaque offre (description, images, itinéraire).
* Authentification et gestion d’un espace personnel utilisateur.
* Suivi des réservations.
* Espace administrateur pour la gestion des offres et visualisation des statistiques.
* Interface responsive avec Bootstrap.

## 📚 Technologies utilisées

* **Framework** : Django (architecture MVT)
* **Langages** : Python, HTML, CSS, JavaScript
* **Frontend** : Django Templates, Bootstrap
* **Base de données** : MySQL



## 📖 Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/TravelBooking.git
cd TravelBooking
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Configurer la base de données (MySQL) :

```sql
CREATE DATABASE travelbooking_db;
```

4. Appliquer les migrations :

```bash
python manage.py migrate
```

5. Démarrer le serveur :

```bash
python manage.py runserver
```

## 📍 Utilisation

* Rechercher un voyage : utilisez la barre de recherche avec les filtres souhaités.
* Réserver : connectez-vous puis choisissez une offre.
* Accès admin : rendez-vous sur `/admin` avec un compte staff.



## 📊 Améliorations prévues

* Module de paiement en ligne sécurisé.
* Système de notation et avis pour les voyages.
* Déploiement sur cloud via Docker/Kubernetes.

## 📚 Références

* [Documentation Django](https://docs.djangoproject.com)
* Tutoriels Django sur [MDN Web Docs](https://developer.mozilla.org/fr/docs/Learn/Server-side/Django)

---

*Projet réalisé dans le cadre d'un projet universitaire sur les technologies web avec Django.*
