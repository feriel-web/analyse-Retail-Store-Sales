Projet d'analyse de données : ventes d'un magasin de détail

Ce projet étudie un fichier de 12 575 transactions d'un magasin de détail. Il se déroule en trois notebooks : l'exploration des données, leur nettoyage, puis leur analyse.

Organisation du projet
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   │   └── retail_store_sales.csv               # fichier d'origine (non versionné)
│   └── processed/
│       └── retail_store_sales_clean.csv         # fichier nettoyé (non versionné)
├── figures/                                     # graphiques enregistrés par les notebooks
└── notebooks/
    ├── 01_exploration.ipynb
    ├── 02_nettoyage.ipynb
    └── 03_analyse.ipynb


Lancer le projet
Installer les bibliothèques :
bash
pip install -r requirements.txt
Placer le fichier retail_store_sales.csv dans data/raw/.
Exécuter les notebooks dans l'ordre : 01, puis 02, puis 03. Le notebook 02 crée le fichier nettoyé utilisé par le notebook 03.


1. Exploration (01_exploration.ipynb)

Première lecture du fichier pour repérer les problèmes :

Taille : 12 575 lignes et 11 colonnes.
Valeurs manquantes : Discount Applied (4 199, soit 33,4 %), Item (1 213, soit 9,6 %), Price Per Unit (609), Quantity (604) et Total Spent (604).
Doublons : aucune ligne en double et aucun identifiant de transaction répété.
Valeurs aberrantes (méthode IQR) : aucune dans Price Per Unit et Quantity, 60 dans Total Spent.

Graphique produit : valeurs_manquantes.png.

2. Nettoyage (02_nettoyage.ipynb)

Chaque problème repéré a été analysé avant d'être corrigé :

Colonne	Problème	Traitement
Price Per Unit	609 prix manquants	Reconstitués avec montant ÷ quantité. Les 25 prix obtenus existaient déjà dans le fichier.
Item	1 213 noms d'articles manquants	Reconstitués : chaque couple (catégorie, prix) correspond à un seul article (200 couples vérifiés).
Quantity	604 valeurs manquantes	Conservées : le prix ou le montant manque aussi, le calcul est impossible.
Total Spent	604 valeurs manquantes	Conservées : même raison.
Discount Applied	4 199 valeurs manquantes	Conservées : aucune information ne permet de savoir s'il y a eu une remise.
Total Spent	60 valeurs aberrantes (410)	Conservées : elles sont cohérentes (41 × 10 articles).

Types corrigés :

Transaction Date : convertie en date ;
Quantity : convertie en entier ;
Discount Applied : convertie en booléen (vrai / faux).

Aucune ligne n'a été supprimée. Le fichier nettoyé est enregistré dans data/processed/retail_store_sales_clean.csv.

3. Analyse (03_analyse.ipynb)
1.1 Indicateurs généraux

12 575 transactions, 25 clients, 8 catégories, un chiffre d'affaires connu de 1 552 071 et un panier moyen de 129,65.

1.2 Ventes par catégorie

Butchers arrive en tête (208 118) et Milk Products en dernier (180 112). Les écarts entre catégories restent faibles.

1.3 Évolution dans le temps
Année	Transactions	Chiffre d'affaires
2022	4 134	510 330
2023	3 987	491 312 (−3,7 %)
2024	4 241	524 881 (+6,8 %)
2025	213	25 549 (année incomplète)

Les ventes sont stables et 2024 est la meilleure année.

1.4 Modes de paiement

Cash 34,3 %, Digital Wallet 33,0 %, Credit Card 32,8 %. Le panier moyen est quasiment identique quel que soit le mode de paiement.

1.5 En ligne et en magasin

En ligne : 51 % du chiffre d'affaires. En magasin : 49 %. Le panier moyen est très proche (130,42 contre 128,86).

1.6 Effet des remises

Avec remise, sans remise ou inconnu : environ un tiers des transactions chacun, et le même panier moyen (environ 130). Les remises n'augmentent pas les ventes.

1.7 Meilleurs clients et articles
Clients : chaque client représente entre 3,7 % et 4,4 % du chiffre d'affaires. Le premier client est CUST_24 (68 452) et le dernier CUST_25 (57 156).
Articles : le top 10 est dominé par les articles les plus chers (Item_22 à Item_25). Item_25_FUR arrive en tête avec 25 625.
1.8 Conclusion

L'activité est stable et très équilibrée : aucune catégorie, aucun mode de paiement, aucun canal et aucun client ne se démarque nettement. Les remises ne semblent pas augmenter les ventes.

Graphiques produits :

chiffre_affaires_par_categorie.png
evolution_mensuelle_ca.png
repartition_modes_paiement.png
ca_par_canal_et_annee.png
top10_articles.png
Limites
604 transactions sans quantité ni montant : le chiffre d'affaires est légèrement sous-estimé.
L'année 2025 ne contient que 213 transactions : elle n'est pas comparée aux autres années.
Le montant total est toujours égal à prix × quantité, même avec une remise : la valeur des remises n'est pas connue.
Le fichier ne contient pas de coûts : on mesure le chiffre d'affaires, pas la rentabilité.
Outils

Python, pandas, Matplotlib, Seaborn, Jupyter.