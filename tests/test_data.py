import os
import sys
from functools import reduce

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.append(parent_directory)

from app.data import Data

def test_fetch_inventory():
    with Data() as data_handle:
        items = data_handle.fetch_inventory()

        assert items
        assert list(filter(lambda item: 'Babel Fish' == item['product'], items))

def test_fetch_product():
    with Data() as data_handle:
        items = data_handle.fetch_product('Babel Fish')

        assert items
        assert list(filter(lambda item: 'Babel Fish' == item['product'], items))

def test_insert_product():
    with Data() as data_handle:
        data_handle.insert_product(
            'Unobtainium', 'Hardware', 9999.99, 0,
        )

        items = data_handle.fetch_product('Unobtainium')

        assert items
        assert list(filter(lambda item: 'Unobtainium' == item['product'], items))

def test_update_product():
    with Data() as data_handle:
        data_handle.update_product(
            'Unobtainium', 'Hardware', 9999.99, 1,
        )

        items = data_handle.fetch_product('Unobtainium')

        assert items
        assert list(filter(lambda item: 1 == item['quantity'], items))

def test_delete_product():
    with Data() as data_handle:
        data_handle.delete_product(
            'Unobtainium'
        )

        items = data_handle.fetch_product('Unobtainium')

        filtered = filter(lambda item: 'Unobtainium' == item['product'], items)
        assert not list(filter(lambda item: 'Unobtainium' == item['product'], items))

