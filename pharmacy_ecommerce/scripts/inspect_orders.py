import sqlite3
conn=sqlite3.connect('db.sqlite3')
c=conn.cursor()
print('orders_order columns:', c.execute("PRAGMA table_info('orders_order')").fetchall())
print('foreign keys:', c.execute("PRAGMA foreign_key_list('orders_order')").fetchall())
conn.close()
