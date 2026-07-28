import sqlite3
conn=sqlite3.connect('db.sqlite3')
c=conn.cursor()
try:
    c.execute('ALTER TABLE products_product ADD COLUMN created_at datetime')
    conn.commit()
    print('added created_at')
    print(c.execute("PRAGMA table_info('products_product')").fetchall())
except Exception as e:
    print('error', e)
finally:
    conn.close()
