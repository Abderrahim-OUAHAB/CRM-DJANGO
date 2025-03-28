# Customer Relationship Management Django

Ce projet est un système de gestion de la relation client (CRM) développé avec Django. Il permet de gérer les clients, les commandes et les produits avec des fonctionnalités CRUD complètes. Il offre également la possibilité de télécharger les données en formats CSV et PDF, ainsi qu'un tableau de bord interactif pour visualiser et filtrer les données.

## Fonctionnalités

- **Gestion des clients** : Ajout, modification, suppression et visualisation des clients.
- **Gestion des commandes** : Ajout, modification, suppression et visualisation des commandes.
- **Gestion des produits** : Ajout, modification, suppression et visualisation des produits.
- **Téléchargement des données** : Exportation des données en fichiers CSV et PDF.
- **Tableau de bord** : Visualisation des statistiques et des données des clients, commandes et produits.
- **Filtrage des données** : Fonctionnalités de filtrage pour faciliter la recherche et la gestion des données.
- **Accès et inscription** : Gestion des utilisateurs avec Django, permettant l'inscription, la connexion et la gestion des sessions.

## Technologies utilisées

- **Django** : Framework backend pour le développement web.
- **Bootstrap** : Framework CSS pour un design réactif et moderne.
- **JavaScript** : Langage de programmation pour les interactions dynamiques.
- **HTML** : Langage de balisage pour structurer les pages web.
- **CSS** : Feuilles de style pour la présentation des pages web.

## Installation

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/Abderrahim-OUAHAB/MY-PROJECT.git
    ```
2. Accédez au répertoire du projet :
    ```sh
    cd path to/COSTUMER_RELATIONSHIP_MANAGEMENT/CRM
    ```
3. Créez un environnement virtuel :
    ```sh
    python -m venv env
    ```
4. Activez l'environnement virtuel :
    - Sur Windows :
        ```sh
        .\env\Scripts\activate
        ```
    - Sur macOS/Linux :
        ```sh
        source env/bin/activate
        ```
5. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```
6. Appliquez les migrations :
    ```sh
    python manage.py migrate
    ```
7. Démarrez le serveur de développement :
    ```sh
    python manage.py runserver
    ```

## Utilisation

1. Ouvrez votre navigateur web et accédez à `http://127.0.0.1:8000`.
2. Inscrivez-vous ou connectez-vous avec vos identifiants.
3. Naviguez dans l'interface pour gérer les clients, commandes et produits.
4. Utilisez le tableau de bord pour visualiser les statistiques et filtrer les données.
5. Téléchargez les données en CSV ou PDF depuis les sections appropriées.


## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com/Abderrahim-OUAHAB/MY-PROJECT/blob/main/LICENSE) pour plus d'informations.


### Développé par  Abderrahim OUAHAB.
