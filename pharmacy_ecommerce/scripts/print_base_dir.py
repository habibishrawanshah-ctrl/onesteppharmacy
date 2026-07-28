from pathlib import Path
import os
print('cwd:', os.getcwd())
print('file:', Path(__file__).resolve())
BASE_DIR = Path(__file__).resolve().parent.parent
print('BASE_DIR:', BASE_DIR)
print('templates dir exists:', (BASE_DIR / 'templates').exists())
print('templates path:', BASE_DIR / 'templates')
for p in (BASE_DIR / 'templates').glob('**/*'):
    print(p)
