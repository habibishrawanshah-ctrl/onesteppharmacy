import sqlite3
conn=sqlite3.connect('db.sqlite3')
c=conn.cursor()
try:
    c.execute('ALTER TABLE products_medicine RENAME TO products_product')
    conn.commit()
    print('renamed products_medicine -> products_product')
    print('tables:', c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
except Exception as e:
    print('error:', e)
finally:
    conn.close()
