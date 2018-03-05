'''

core.py
~~~~~~~~~~~~~~~~

inventory-app core logic

'''

import random
import sqlite3


class Item:
    def __init__(self, ref, desc, price_per_unit, quantity):
        if len(str(desc)) > 70:
            raise Exception(
                'Description must not contain more than 70 characters.')

        if len(str(desc)) == 0:
            raise Exception('''Description must not be blank.''')

        if float(price_per_unit) < 0:
            raise Exception('''Price per unit must not a negative number.''')
        if int(quantity) < 0:
            raise Exception('''Quantity must not be a negative number.''')

        try:
            self.__price_per_unit = float(price_per_unit)
        except ValueError:
            raise ValueError(
                'Price per unit must be a positive real number.'
                ' Example: 2.72, 5.4 or 7.')
        try:
            self.__quantity = int(quantity)
        except ValueError:
            raise ValueError('''Quantity must be whole number. Example: 5''')

        self.ref = ref
        self.desc = desc
        self.__set_total_price()

    def __set_total_price(self):
        self.__total_price = self.__price_per_unit * self.__quantity

    def get_price_per_unit(self):
        return self.__price_per_unit

    def get_quantity(self):
        return self.__quantity

    def get_total_price(self):
        return self.__total_price

    def set_price_per_unit(self, price_per_unit):
        self.__price_per_unit = price_per_unit
        self.__set_total_price()

    def set_quantity(self, quantity):
        self.__quantity = quantity
        self.__set_total_price()


class Inventory:
    def __init__(self, path):
        self.__path = path
        self.__created = set()  # Keeps the index of new items.
        self.__changed = set()  # Keeps the index of changed items.
        self.__deleted = set()  # Keeps the ref code of deleted items.
        self.items = []
        self.__load()

    def __gen_ref(self, length):
        '''
        Generate a reference code for new items.
        '''
        chars = ['a', 'b', 'c', 'd', 'e', 'e', 'f',
                 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'r', 's', 't', 'u',
                 'v', 'w', 'x', 'y', 'z', '1', '2',
                 '3', '4', '5', '6', '7', '8', '9',
                 '0']
        ref = ''
        for i in range(length):
            ref += random.choice(chars)

        for item in self.items:
                if item.ref == ref:
                    return self.__gen_ref(length)
        return ref

    def new_item(self, desc, price_per_unit=None, quantity=None):
        if price_per_unit is not None:
            new_price = price_per_unit
        else:
            new_price = 0

        if quantity is not None:
            new_quantity = quantity
        else:
            new_quantity = 0

        new_ref = self.__gen_ref(8)
        new_item = Item(new_ref, desc, new_price, new_quantity)
        self.items.append(new_item)
        self.__created.add(len(self.items) - 1)
        self.__refresh()

    def modify_item(self, ref, desc=None, price_per_unit=None, quantity=None):
        for index, item in enumerate(self.items):
            if item.ref == ref:
                mod = index
                if desc is not None:
                    self.items[mod].desc = desc
                if price_per_unit is not None:
                    self.items[mod].set_price_per_unit(price_per_unit)
                if quantity is not None:
                    self.items[mod].set_quantity(quantity)
                self.__changed.add(mod)
                self.__refresh()
                return 0
        raise Exception('Item does not exist.')

    def delete_item(self, ref):
        for item in self.items:
            if item.ref == ref:
                self.__deleted.add(item.ref)
                self.__refresh()
                return 0
        raise Exception('''Item does not exist''')

    def clear(self):
        '''
        Remove all items from inventory.
        '''
        self.__deleted = {item.ref for item in self.items}
        self.__refresh()

    def __save(self):
        db = sqlite3.connect(self.__path)
        for index in list(self.__changed):
            item = self.items[index]
            db.execute(
                '''UPDATE inventory SET description = ?, price_per_unit = ?, quantity = ?
                WHERE ref = ?''',
                (item.desc, item.get_price_per_unit(), item.get_quantity(),
                    item.ref))

        for index in list(self.__created):
            item = self.items[index]
            new_row = (
                item.ref, item.desc, item.get_price_per_unit(),
                item.get_quantity())
            db.execute('''INSERT into inventory values (?,?,?,?)''', new_row)

        for ref in list(self.__deleted):
            db.execute('''DELETE from inventory where ref = ?''', (ref, ))

        db.commit()

    def __refresh(self):
        self.__save()
        self.__load()

    def __load(self):
        self.__created = set()
        self.__changed = set()
        self.__deleted = set()
        self.items = []

        db = sqlite3.connect(self.__path)
        db.execute('''CREATE TABLE IF NOT EXISTS inventory(ref TEXT PRIMARY KEY NOT NULL,
         description TEXT NOT NULL, price_per_unit REAL NOT NULL,
          quantity INT NOT NULL )''')

        rows = db.execute('''SELECT ref, description,
             price_per_unit, quantity from inventory''')

        for row in rows:
            self.items.append(Item(row[0], row[1], row[2], row[3]))


if __name__ == '__main__':
    pass
