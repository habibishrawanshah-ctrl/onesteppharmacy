import urllib.request
for path in ['http://127.0.0.1:8000/','http://127.0.0.1:8000/products/','http://127.0.0.1:8000/products/1/']:
    try:
        r=urllib.request.urlopen(path)
        print(path, r.getcode(), len(r.read()))
    except Exception as e:
        print(path, 'ERROR', e)
