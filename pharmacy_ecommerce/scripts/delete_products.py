import sqlite3

path = r'c:\Users\LENOVO\Desktop\Pharmacy\Django\PharmacyProject\pharmacy_ecommerce\db.sqlite3'
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute('DELETE FROM products_product')
print('deleted', cur.rowcount)
conn.commit()
conn.close()
