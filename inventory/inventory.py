'''

inventory.py
~~~~~~~~~~~~

inventory-app command line interface

'''
import os
import argparse
import appdirs
import core

APPNAME = 'inventory-app'
DB_FILENAME = 'inventory.db'

if __name__ == '__main__':
    # Initialize database.
    db_path = appdirs.user_data_dir(appname=APPNAME, appauthor=False)
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    db_path = os.path.join(db_path, DB_FILENAME)
    db = core.Inventory(db_path)

    # Interface functions.
    def _show(_args):
        '''
        List all items in the inventory.
        '''
        _items = db.items

        def print_items(item_list):
            if len(item_list) < 1:
                print('\nThere are no items in the inventory.')
            else:
                print('\n')
                for item in item_list:
                    print(
                        '{}    {}    {}    {}    {}'
                        .format(
                            item.ref, item.desc,
                            item.get_price_per_unit(), item.get_quantity(),
                            item.get_total_price()))
                print('\n')

        if _args.order:
            if _args.order == 'pu':
                # lowest to highest price
                _items.sort(key=lambda x: x.get_price_per_unit(),
                            reverse=False)
                print_items(_items)

            elif _args.order == 'pd':
                # highest to lowest price
                _items.sort(key=lambda x: x.get_price_per_unit(),
                            reverse=True)
                print_items(_items)
            elif _args.order == 'qu':
                # lowest to highest quantity
                _items.sort(key=lambda x: x.get_quantity(),
                            reverse=False)
                print_items(_items)
                pass
            elif _args.order == 'qd':
                # highest to lowest quantity
                _items.sort(key=lambda x: x.get_quantity(),
                            reverse=True)
                print_items(_items)
                pass
            elif _args.order == 'tu':
                # lowest to highest total price
                _items.sort(key=lambda x: x.get_total_price(),
                            reverse=False)
                print_items(_items)
                pass
            elif _args.order == 'td':
                # highest to lowest total price
                _items.sort(key=lambda x: x.get_total_price(),
                            reverse=True)
                print_items(_items)
                pass
            else:
                print('\nGiven argument {} is invalid, showing items \
in default inventory order.'.format(_args.order))
                print_items(_items)
        else:
            print_items(_items)

    def _new(_args):
        '''
        Create a new item in the inventory.
        '''
        if _args.desc:
            try:
                db.new_item(_args.desc, _args.price, _args.quantity)
                return 0
            except Exception as e:
                print(e)
        else:
            print('Item description (-d) is required to create a new item.')

    def _del(_args):
        if _args.ref is None:
            print('Reference code must be given to delete item.')
            return 0
        else:
            try:
                db.delete_item(_args.ref)
                print('Item {} deleted'.format(_args.ref))
            except Exception as e:
                print(e)

    def _edit(_args):
        if _args.ref is None:
            print('Reference code must be given to edit item.')
            return 0
        else:
            try:
                db.modify_item(_args.ref, desc=args.desc,
                               price_per_unit=args.price,
                               quantity=args.quantity)
            except Exception as e:
                print(e)

    # Command parsing.
    functions = {'show': _show, 'new': _new, 'del': _del, 'edit': _edit}
    parser = argparse.ArgumentParser()

    parser.add_argument('command',
                        help='The desired action: show, new, del, edit')
    parser.add_argument('-d', '--desc', help='Item description.')
    parser.add_argument('-p', '--price', help='Price per unit of the item.')
    parser.add_argument('-q', '--quantity', help='Item quantity.')
    parser.add_argument('-o', '--order',
                        help='Order in which items will be shown.')
    parser.add_argument('-r', '--ref', help='Item reference code.')

    args = parser.parse_args()
    command = args.command

    if command in functions:
        functions[command](args)
    else:
        print('Given command {} is invalid.'.format(command))
