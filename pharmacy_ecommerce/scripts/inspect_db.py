import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
print('tables =', c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
print('products_product exists =', c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products_product'").fetchone())
print('products_medicine columns =', c.execute("PRAGMA table_info('products_medicine')").fetchall())
print('django_migrations sample =', c.execute("SELECT id, app, name FROM django_migrations LIMIT 10").fetchall())
conn.close()
