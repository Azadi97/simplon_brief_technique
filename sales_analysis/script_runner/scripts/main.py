import sqlite3
import csv
import os

# ---------------------- SETUP ----------------------
DB_PATH = "/data/sales.db"
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ---------------------- TABLE CREATION ----------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id_référence_produit TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        prix REAL NOT NULL,
        stock INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS magasins (
        id_magasin INTEGER PRIMARY KEY,
        ville TEXT NOT NULL,
        nombre_de_salariés INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventes (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        id_référence_produit TEXT NOT NULL,
        quantité INTEGER NOT NULL,
        id_magasin INTEGER NOT NULL,
        UNIQUE(date, id_référence_produit, id_magasin, quantité),
        FOREIGN KEY (id_référence_produit) REFERENCES produits(id_référence_produit),
        FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin)
    )
""")

print("✅ Tables created with French column names intact.")

# ---------------------- FUNCTION ----------------------
def import_csv_to_table(csv_path, insert_query, rename_map):
    try:
        print(f"📂 Trying to load: {csv_path}")
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                cleaned = {db_key: row[csv_key].strip() for db_key, csv_key in rename_map.items()}
                rows.append(cleaned)
            print(f"✅ Loaded {len(rows)} rows from {csv_path}")
            cursor.executemany(insert_query, rows)
    except Exception as e:
        print(f"❌ Error importing {csv_path}: {e}")

# ---------------------- IMPORT DATA ----------------------
import_csv_to_table(
    "data/produits.csv",
    """
    INSERT OR IGNORE INTO produits (id_référence_produit, nom, prix, stock)
    VALUES (:id_référence_produit, :nom, :prix, :stock)
    """,
    {
        "id_référence_produit": "ID Référence produit",
        "nom": "Nom",
        "prix": "Prix",
        "stock": "Stock"
    }
)

import_csv_to_table(
    "data/magasins.csv",
    """
    INSERT OR IGNORE INTO magasins (id_magasin, ville, nombre_de_salariés)
    VALUES (:id_magasin, :ville, :nombre_de_salariés)
    """,
    {
        "id_magasin": "ID Magasin",
        "ville": "Ville",
        "nombre_de_salariés": "Nombre de salariés"
    }
)

import_csv_to_table(
    "data/ventes.csv",
    """
    INSERT OR IGNORE INTO ventes (date, id_référence_produit, quantité, id_magasin)
    VALUES (:date, :id_référence_produit, :quantité, :id_magasin)
    """,
    {
        "date": "Date",
        "id_référence_produit": "ID Référence produit",
        "quantité": "Quantité",
        "id_magasin": "ID Magasin"
    }
)

# ---------------------- FINISH ----------------------
conn.commit()
conn.close()
print("✅ Données importées avec succès, sans doublons 🚀")
