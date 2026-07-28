import sqlite3
from pathlib import Path

base = Path(__file__).resolve().parent.parent
db = base / 'db.sqlite3'
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute(
    "INSERT INTO products_product (name, description, price, stock, expiry_date, image, created_at) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))",
    ('Fresh Medicine', 'Fresh new medicine, ready to use.', 120.00, 20, '2027-12-31', 'product_images/paracetamol.svg')
)
conn.commit()
print('inserted', cur.lastrowid)
conn.close()
