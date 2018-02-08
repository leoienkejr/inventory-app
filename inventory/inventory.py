'''

inventory.py
~~~~~~~~~~~~

Inventory management command-line application.

'''
import os
import appdirs
import core

APPNAME = 'inventory-app'
DB_FILENAME = 'inventory.db'

if __name__ == '__main__':
    db_path = appdirs.user_data_dir(appname=APPNAME, appauthor=False)
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    db_path = os.path.join(db_path, DB_FILENAME)
    db = lib.Inventory(db_path)
