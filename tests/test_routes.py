import os
import sys

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.append(parent_directory)

from app import inventory_app
from app.data import Data

def test_stock_report():
    response = inventory_app.test_client().get('/stock_report')

    assert response.status_code == 200
    assert response.data.decode('utf-8').find('Babel Fish') > -1

def test_inventory_manage():
    response = inventory_app.test_client().get('/inventory?department_filter=Pets&message="Ferrets are loose in the building"&message_color="red"')

    assert response.status_code == 200
    assert response.data.decode('utf-8').find('Babel Fish') > -1
    assert response.data.decode('utf-8').find('Ferrets') > -1
    assert response.data.decode('utf-8').find('red') > -1

def test_cancel():
    data = {
        'department-filter': 'Hardware',
        'price-filter': '',
        'quantity-filter': '',
    }

    response = inventory_app.test_client().post('/cancel', data = data)

    assert response.status_code == 302

def test_add_product():
    data = {
        'department-filter': 'Hardware',
        'price-filter': '',
        'quantity-filter': '',
        'product': 'Unobtainium',
        'department': 'Hardware',
        'price': 9999.99,
        'quantity': 0,
    }

    response = inventory_app.test_client().post('/add_product', data = data)

    assert response.status_code == 302

    with Data() as data_handle:
        item = data_handle.fetch_product('Unobtainium')

        assert item

def test_edit_product():
    data = {
        'department-filter': 'Hardware',
        'price-filter': '',
        'quantity-filter': '',
        'product': 'Unobtainium',
        'department': 'Hardware',
        'price': 9999.99,
        'quantity': 1,
    }

    response = inventory_app.test_client().post('/edit_product', data = data)

    assert response.status_code == 302

    with Data() as data_handle:
        item = data_handle.fetch_product('Unobtainium')

        assert item
        assert item[0]['quantity'] == 1

def test_delete_product():
    data = {
        'department-filter': 'Hardware',
        'price-filter': '',
        'quantity-filter': '',
        'product': 'Unobtainium',
    }

    response = inventory_app.test_client().post('/delete_product', data = data)

    assert response.status_code == 302

    with Data() as data_handle:
        item = data_handle.fetch_product('Unobtainium')

        assert not item

def test_add():
    data = {
        'department-filter': 'Hardware',
        'price-filter': '',
        'quantity-filter': '',
    }

    response = inventory_app.test_client().post('/add', data = data)

    assert response.status_code == 200
    assert response.data.decode('utf-8').find('Product') > -1
    assert response.data.decode('utf-8').find('Cancel') > -1

def test_edit():
    data = {
        'department-filter': 'Hardware',
        'price-filter': '',
        'quantity-filter': '',
        'edit-submit': 'Babel Fish',
    }

    response = inventory_app.test_client().post('/edit', data = data)

    assert response.status_code == 200
    assert response.data.decode('utf-8').find('Product') > -1
    assert response.data.decode('utf-8').find('Babel Fish') > -1
    assert response.data.decode('utf-8').find('Cancel') > -1

# TBD test_inventory_import

# TBD test_inventory_export
