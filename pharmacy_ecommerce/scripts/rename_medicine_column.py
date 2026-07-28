import sqlite3
conn=sqlite3.connect('db.sqlite3')
c=conn.cursor()
try:
    c.execute('ALTER TABLE orders_order RENAME COLUMN medicine_id TO product_id')
    conn.commit()
    print('renamed column')
    print(c.execute("PRAGMA table_info('orders_order')").fetchall())
except Exception as e:
    print('error', e)
finally:
    conn.close()
