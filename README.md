# OCP2: Books To Scrape   

Ce script permet de récupérer les informations de touts les produits du site http://books.toscrape.com/

Les données récupérées sont les suivantes :
* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url

Les données extraites sont ensuite insérées dans un fichier CSV pour chaque catégories de produit.
Le script télécharge également les images de chaque produit en utilisant leur upc pour les nommer.

L'ensemble des données sont organisées de la manière suivante :

```
├───data/
    └───category1/
        └───img/
    └───category2/
        └───img/         
    ...etc
```

## Installation

Récupérez le dépot github :

```
git clone https://github.com/nopalpite/OCP2.git
```

Placez-vous dans le dossier OCP2 et créez un environnement virtuel:

```
python -m venv env
```
Activez l'environnement virtuel
Sur Windows :
```
env\Scripts\activate
```
Sur Linux:
```
source env/bin/activate
```
Installez les packages requis:
```
pip install -r requirements.txt
```
Enfin, lancez le script:
```
python main.py
```

