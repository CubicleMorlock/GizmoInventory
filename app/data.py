import os
import sys
import sqlite3
import configargparse
from datetime import datetime, UTC

from app.utils.logging import make_logger
from app.config_load import config_load

logger = make_logger()

def database_path(database_filename):
    if database_filename.find('/') < 0:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
        return parent_directory + '/' + database_filename 
    else:
        return database_filename 

class Data():
    """Inventory database interaction class."""

    def __init__(self):
        self.parsed_args = config_load()
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(database_path(self.parsed_args.database))
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()
        self.connection = None

    def fetch_inventory(self):
        """Inventory fetch method.

        Args:
            self (object)
        """
        try:
            # if connection not context managed, handle it locally
            self_connected = False
            if not self.connection:
                self.__enter__()
                self_connected = True

            # fetch as dictionary
            self.connection.row_factory = sqlite3.Row

            cursor = self.connection.cursor()
            rows = cursor.execute("SELECT product, department, price, quantity, stock_date FROM inventory").fetchall()

            # if connection not context managed, handle it locally
            if self_connected:
                self.__exit__(None, None, None)

            return [dict(row) for row in rows]

        except Exception as error:
            # just log the error and return an empty result
            logger.error(f'Database error - {str(error)}')
            return []

    def fetch_product(self, product):
        """Product fetch method.

        Args:
            self (object)
            product (string) - name of product to return
        """
        try:
            # if connection not context managed, handle it locally
            self_connected = False
            if not self.connection:
                self.__enter__()
                self_connected = True

            # fetch as dictionary
            self.connection.row_factory = sqlite3.Row

            cursor = self.connection.cursor()
            rows = cursor.execute("SELECT product, department, price, quantity, stock_date FROM inventory WHERE product = ?", (product,)).fetchall()

            # if connection not context managed, handle it locally
            if self_connected:
                self.__exit__(None, None, None)

            return [dict(row) for row in rows]

        except Exception as error:
            # just log the error and return an empty result
            logger.error(f'Database error - {str(error)}')
            return []

    def insert_product(self, product, department, price, quantity):
        """Product add method.

        Args:
            self (object)
            product (string) - name of product to add
            department (string) - department to set on product
            price (string) - price to set on product
            quantity (string) - quantity to set on product
        """
        try:
            # if connection not context managed, handle it locally
            self_connected = False
            if not self.connection:
                self.__enter__()
                self_connected = True

            stock_date = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", (product, department, price, quantity, stock_date))

            # if connection not context managed, handle it locally
            if self_connected:
                self.__exit__(None, None, None)

            self.connection.commit()

        except Exception as error:
            # just log the error and return
            logger.error(f'Database error - {str(error)}')


    def update_product(self, product, department, price, quantity):
        """Product update method.

        Args:
            self (object)
            product (string) - name of product to update
            department (string) - department to set on product
            price (string) - price to set on product
            quantity (string) - quantity to set on product
        """
        try:
            # if connection not context managed, handle it locally
            self_connected = False
            if not self.connection:
                self.__enter__()
                self_connected = True

            stock_date = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
            cursor = self.connection.cursor()
            cursor.execute("UPDATE inventory SET department = ?, price = ?, quantity = ?, stock_date = ? WHERE product = ?", (department, price, quantity, stock_date, product))

            # if connection not context managed, handle it locally
            if self_connected:
                self.__exit__(None, None, None)

            self.connection.commit()

        except Exception as error:
            # just log the error and return
            logger.error(f'Database error - {str(error)}')

    def delete_product(self, product):
        """Product delete method.

        Args:
            self (object)
            product (string) - name of product to delete
        """
        try:
            # if connection not context managed, handle it locally
            self_connected = False
            if not self.connection:
                self.__enter__()
                self_connected = True

            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM inventory WHERE product = ?", (product,))

            # if connection not context managed, handle it locally
            if self_connected:
                self.__exit__(None, None, None)

            self.connection.commit()

        except Exception as error:
            # just log the error and return
            logger.error(f'Database error - {str(error)}')

    def import_from_json(self, inventory):
        """Data import method. Adds items that aren't in
           the inventory, updates ones that are.

        Args:
            self (object)
            inventory (json) - data to import from
        """

        stock_date = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")

        if isinstance(inventory, dict):
            inventory = [inventory]
        if isinstance(inventory, list):
            for item in inventory:
                # this is an error, should do more than just skip the entry
                if not isinstance(item, dict):
                    continue
                
                try:
                    # should also be doing data validation here - type
                    # checking, etc
                    product = item['product']
                    department = item['department']
                    price = item['price']
                    quantity = item['quantity']

                    # if it exists, this is an update...
                    if (self.fetch_product(product)):
                        self.update_product(product, department, price, quantity)
                    # ...otherwise, this is an insert
                    else:
                        self.insert_product(product, department, price, quantity)
                except KeyError:
                    # this is an error, should do more than just skip the entry
                    # on a missing key
                    continue
                except Exception as error:
                    # this is an error, should do better exception handling
                    # than just base type
                    continue
            return True
        else:
            # this is a data formatting error, and should be handled better
            return False
