import sqlite3
db=r'c:\Users\LENOVO\Desktop\Pharmacy\Django\PharmacyProject\pharmacy_ecommerce\db.sqlite3'
con=sqlite3.connect(db)
cur=con.cursor()
# set image field for product id 1
cur.execute("UPDATE products_product SET image=? WHERE id=?",('product_images/paracetamol.svg',1))
con.commit()
print('updated', cur.rowcount)
con.close()
