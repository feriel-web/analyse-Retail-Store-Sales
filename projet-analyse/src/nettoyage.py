"""Nettoyage du jeu de données Retail Store Sales.

Reprend, sans les explications, les corrections décidées dans
notebooks/02_nettoyage.ipynb.

Utilisation (depuis la racine du projet) :
    python nettoyage.py
"""

from pathlib import Path

import pandas as pd

# Chemins construits à partir de l'emplacement de ce fichier,
# pour que le script marche quel que soit le dossier d'où on le lance
DOSSIER_PROJET = Path(__file__).resolve().parent
FICHIER_BRUT = DOSSIER_PROJET / "data" / "raw" / "retail_store_sales.csv"
FICHIER_PROPRE = DOSSIER_PROJET / "data" / "processed" / "retail_store_sales_clean.csv"


def charger_donnees(chemin=FICHIER_BRUT):
    """Charge le fichier brut."""
    return pd.read_csv(chemin)


def reconstituer_prix(df):
    """Recalcule le prix unitaire manquant avec montant ÷ quantité.

    Possible pour les 609 lignes où le montant et la quantité sont connus.
    """
    df = df.copy()
    masque = (
        df["Price Per Unit"].isna()
        & df["Total Spent"].notna()
        & df["Quantity"].notna()
    )
    df.loc[masque, "Price Per Unit"] = (
        df.loc[masque, "Total Spent"] / df.loc[masque, "Quantity"]
    )
    return df


def reconstituer_articles(df):
    """Retrouve le nom de l'article manquant à partir de la catégorie et du prix.

    Chaque couple (catégorie, prix) correspond à un seul article :
    la correspondance est donc sans ambiguïté. Doit être appelée
    après reconstituer_prix, sinon il manque des prix.
    """
    df = df.copy()
    articles_connus = df.dropna(subset=["Item"])

    # Sécurité : on vérifie que la règle est toujours vraie avant de l'appliquer
    nb_articles = articles_connus.groupby(["Category", "Price Per Unit"])["Item"].nunique()
    if (nb_articles > 1).any():
        raise ValueError("Un couple (catégorie, prix) correspond à plusieurs articles.")

    correspondance = (
        articles_connus
        .drop_duplicates(subset=["Category", "Price Per Unit"])
        .set_index(["Category", "Price Per Unit"])["Item"]
    )

    masque = df["Item"].isna()
    cles = zip(df.loc[masque, "Category"], df.loc[masque, "Price Per Unit"])
    df.loc[masque, "Item"] = [correspondance.get(cle) for cle in cles]
    return df


def corriger_types(df):
    """Met chaque colonne au bon type en conservant les valeurs manquantes."""
    df = df.copy()
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
    df["Quantity"] = df["Quantity"].astype("Int64")
    df["Discount Applied"] = df["Discount Applied"].astype("boolean")
    return df


def nettoyer(df):
    """Applique toutes les étapes de nettoyage, dans le bon ordre."""
    df = reconstituer_prix(df)
    df = reconstituer_articles(df)
    df = corriger_types(df)
    # Quantity, Total Spent et Discount Applied manquants sont conservés :
    # impossible de les retrouver sans inventer de données.
    return df


def enregistrer(df, chemin=FICHIER_PROPRE):
    """Enregistre le fichier nettoyé dans data/processed."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(chemin, index=False)


if __name__ == "__main__":
    donnees = charger_donnees()
    print("Valeurs manquantes avant nettoyage :")
    print(donnees.isna().sum(), "\n")

    donnees_propres = nettoyer(donnees)
    enregistrer(donnees_propres)

    print("Valeurs manquantes après nettoyage :")
    print(donnees_propres.isna().sum(), "\n")
    print("Fichier nettoyé enregistré :", FICHIER_PROPRE)