import sqlite3
db='c:\\Users\\LENOVO\\Desktop\\Pharmacy\\Django\\PharmacyProject\\pharmacy_ecommerce\\db.sqlite3'
con=sqlite3.connect(db)
cur=con.cursor()
try:
    cur.execute('SELECT id,name,image,price,stock,expiry_date,created_at FROM products_product')
    for row in cur.fetchall():
        print(row)
except Exception as e:
    print('ERROR', e)
con.close()
