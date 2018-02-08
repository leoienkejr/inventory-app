'''

inventory.py
~~~~~~~~~~~~

Inventory management command-line application.

'''
import os
import argparse
import appdirs
import core

APPNAME = 'inventory-app'
DB_FILENAME = 'inventory.db'

if __name__ == '__main__':
    db_path = appdirs.user_data_dir(appname=APPNAME, appauthor=False)
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    db_path = os.path.join(db_path, DB_FILENAME)
    db = core.Inventory(db_path)

    def _show(_args):
        '''
        List all items in the inventory.
        '''
        if _args.order:
            if _args.order == 'pu':
                pass
            if _args.order == 'pd':
                pass
            if _args.order == 'qu':
                pass
            if _args.order == 'qd':
                pass
            if _args.order == 'tu':
                pass
            if _args.order == 'td':
                pass
            else:
                print('Given ordering option {} is invalid, showing items \
in default inventory order. \n'.format(_args.order))
        else:
            pass

    def _new(_parser):
        pass

    def _del(_parser):
        pass

    def _edit(_parser):
        pass

    functions = {'show': _show, 'new': _new, 'del': _del, 'edit': _edit}
    parser = argparse.ArgumentParser()

    parser.add_argument('command',
                        help='The desired command. - show; new; del; edit;')
    parser.add_argument('-o', '--order',
                        help='Show items in the specified order.')

    args = parser.parse_args()
    command = args.command

    if command in functions:
        functions[command](args)
    else:
        # raise Exception('Given command "{}" is invalid.'.format(command))
        print('Given command "{}" is invalid.'.format(command))
