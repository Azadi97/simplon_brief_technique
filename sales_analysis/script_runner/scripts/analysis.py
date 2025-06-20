import sqlite3
from datetime import datetime

DB_PATH = "/data/sales.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\nRunning SQL analyses and storing results...\n")

# Ensure the results table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS résultats_analyse (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_heure TEXT,
        type_analyse TEXT,
        résultat TEXT
    );
""")

# store a result
def store_result(type_analyse, résultat):
    cursor.execute("""
        INSERT INTO résultats_analyse (date_heure, type_analyse, résultat)
        VALUES (?, ?, ?);
    """, (datetime.now().isoformat(timespec='seconds'), type_analyse, str(résultat)))
    conn.commit()

# 1. Total revenue
cursor.execute("""
    SELECT SUM(v.quantité * p.prix)
    FROM ventes v
    JOIN produits p ON v.id_référence_produit = p.id_référence_produit
""")
revenue = cursor.fetchone()[0] or 0
print(f"Total Revenue: {revenue:.2f} €")
store_result("chiffre_affaires_total", f"{revenue:.2f} €")

# 2. Sales per product
print("\nVentes par produit:")
cursor.execute("""
    SELECT p.nom, SUM(v.quantité)
    FROM ventes v
    JOIN produits p ON v.id_référence_produit = p.id_référence_produit
    GROUP BY p.nom
""")
for nom, total in cursor.fetchall():
    print(f"  - {nom}: {total} unités")
    store_result("ventes_par_produit", f"{nom}: {total} unités")

# 3. Sales per city
print("\nVentes par ville:")
cursor.execute("""
    SELECT m.ville, SUM(v.quantité * p.prix)
    FROM ventes v
    JOIN produits p ON v.id_référence_produit = p.id_référence_produit
    JOIN magasins m ON v.id_magasin = m.id_magasin
    GROUP BY m.ville
""")
for ville, total in cursor.fetchall():
    print(f"  - {ville}: {total:.2f} €")
    store_result("ventes_par_ville", f"{ville}: {total:.2f} €")

conn.close()
print("\nAnalyses terminées et stockées dans 'résultats_analyse'.\n")