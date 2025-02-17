import json

from flask import request, jsonify, redirect, url_for, render_template, \
    render_template_string, Response

from app import inventory_app
from app.data import Data
from app.utils.logging import make_logger

logger = make_logger()

@inventory_app.route("/export", methods=['GET', 'POST'])
def inventory_export():
    """Route for doing inventory export."""
 
    with Data() as data_handle:
        inventory = sorted(data_handle.fetch_inventory(), key=lambda item: item['product'])
        json_inventory = json.dumps(inventory, indent = 4)

        response = Response(json_inventory, content_type="application/json")
        response.headers["Content-Disposition"] = "attachment; filename=inventory.json"
 
        return response

@inventory_app.route("/import", methods=['POST'])
def inventory_import():
    """Route for doing inventory import.

       Read from import stream into a JSON object, then hand to Data class to
       selectively insert/update contents.
    """

    inventory_import = request.files.get('import')
    # would NEVER do this in a production / public
    # facing environment
    inventory_string = inventory_import.read()

    message = None
    message_color = None
    try:
        # and would NEVER do this in a production / public
        # facing environment, needs more sanity checking
        # than just validating the JSON
        inventory = json.loads(inventory_string)

        with Data() as data_handle:
            if data_handle.import_from_json(inventory):
                message = 'Imported data to inventory'
                message_color = 'blue'
            else:
                message = 'Data import failed'
                message_color = 'red'

    # should do more granular exception handling, and error details
    except Exception as error:
        message = 'Invalid import data format'
        message_color = 'red'

    return redirect(url_for('inventory_manage', 
        message = message, message_color = message_color))

@inventory_app.route("/edit", methods=['POST'])
def edit():
    """Route for building the edit product screen."""

    # get previously chosen filters, to re-create them in
    # inventory page
    department_filter = request.values.get('department-filter')
    price_filter = request.values.get('price-filter')
    quantity_filter = request.values.get('quantity-filter')

    with Data() as data_handle:
        # clicked item is the product to load edit page for
        item = data_handle.fetch_product(request.values.get('edit-submit'))

        # this shouldn't happen, but handle it anyway
        if not item:
            return redirect(url_for('inventory_manage', 
                department_filter = department_filter,
                price_filter = price_filter,
                quantity_filter = quantity_filter))

        # render edit page
        return render_template(
            'edit.html',
            item = item[0],
            department_filter = request.values.get('department-filter'),
            price_filter = request.values.get('price-filter'),
            quantity_filter = request.values.get('quantity-filter'),
        )

@inventory_app.route("/edit_product", methods=['POST'])
def edit_product():
    """Route for doing the edit of a product.

       Routes back to the inventory page, with the previous filters.
    """

    # get previously chosen filters, to re-create them in
    # inventory page
    department_filter = request.values.get('department-filter')
    price_filter = request.values.get('price-filter')
    quantity_filter = request.values.get('quantity-filter')

    # get form values for the edit
    product = request.values.get('product')
    department = request.values.get('department')
    price = request.values.get('price')
    quantity = request.values.get('quantity')

    with Data() as data_handle:
        data_handle.update_product(product, department, price, quantity)

    # send user back to inventory page, with update message
    return redirect(url_for('inventory_manage', 
        message = f'Updated {product} in inventory', message_color = 'blue',
        department_filter = department_filter, price_filter = price_filter,
        quantity_filter = quantity_filter))

@inventory_app.route("/delete_product", methods=['POST'])
def delete_product():
    """Route for doing the delete of a product.

       Routes back to the inventory page, with the previous filters.
    """

    # get previously chosen filters, to re-create them in
    # inventory page
    department_filter = request.values.get('department-filter')
    price_filter = request.values.get('price-filter')
    quantity_filter = request.values.get('quantity-filter')

    # get form values for the delete
    product = request.values.get('product')

    with Data() as data_handle:
        data_handle.delete_product(product)

    # send user back to inventory page, with delete message
    return redirect(url_for('inventory_manage', 
        message = f'Deleted {product} from inventory', message_color = 'blue',
        department_filter = department_filter, price_filter = price_filter,
        quantity_filter = quantity_filter))

@inventory_app.route("/add", methods=['POST'])
def add():
    """Route for building the add product screen."""

    # get previously chosen filters, to re-create them in
    # inventory page
    department_filter = request.values.get('department-filter')
    price_filter = request.values.get('price-filter')
    quantity_filter = request.values.get('quantity-filter')

    # render add page
    return render_template(
        'add.html',
        department_filter = request.values.get('department-filter'),
        price_filter = request.values.get('price-filter'),
        quantity_filter = request.values.get('quantity-filter'),
    )

@inventory_app.route("/add_product", methods=['POST'])
def add_product():
    """Route for doing the edit of a product.

       Routes back to the inventory page, with the previous filters.
    """

    # get previously chosen filters, to re-create them in
    # inventory page
    department_filter = request.values.get('department-filter')
    price_filter = request.values.get('price-filter')
    quantity_filter = request.values.get('quantity-filter')

    # get form values for the add
    product = request.values.get('product')
    department = request.values.get('department')
    price = request.values.get('price')
    quantity = request.values.get('quantity')

    message = None
    message_color = None
    with Data() as data_handle:
        item = data_handle.fetch_product(product)

        # if product name already exists, reject the add...
        if item:
            message = f'{product} already exists in inventory'
            message_color = 'red'
        # ...else add the new product
        else:
            message = f'Added {product} to inventory'
            message_color = 'blue'
            data_handle.insert_product(product, department, price, quantity)

    # send user back to inventory page, with add or error message
    return redirect(url_for('inventory_manage', 
        message = message, message_color = message_color,
        department_filter = department_filter, price_filter = price_filter,
        quantity_filter = quantity_filter))

@inventory_app.route("/cancel", methods=['POST'])
def cancel():
    """Route for doing the cancel of an edit on a product.

       Routes back to the inventory page, with the previous filters.

       This should probably be done purely client side.
    """

    # get previously chosen filters, to re-create them in
    # inventory page
    department_filter = request.values.get('department-filter')
    price_filter = request.values.get('price-filter')
    quantity_filter = request.values.get('quantity-filter')

    return redirect(url_for('inventory_manage', 
        department_filter = department_filter, price_filter = price_filter,
        quantity_filter = quantity_filter))

@inventory_app.route("/inventory", methods=['GET', 'POST'])
def inventory_manage():
    """Build inventory management screen, applying any previously
       set filters.
    """

    # get previously chosen filters, to re-create them in
    # this page
    department_filter = request.args.get('department_filter', '')
    price_filter = request.args.get('price_filter', 0)
    quantity_filter = request.args.get('quantity_filter', 0)

    # pull any operation status messages for user attention
    message = request.args.get('message', '')
    message_color = request.args.get('message_color', '')

    # type conversion from HTML stringification back to numeric values, might not be necessary
    if price_filter:
        price_filter = float(price_filter)
    if quantity_filter:
        quantity_filter = int(quantity_filter)

    with Data() as data_handle:
        inventory = sorted(data_handle.fetch_inventory(), key=lambda item: item['product'])

        # create filters lists from unique values in the database
        department_filters = sorted(set([item['department'] for item in inventory]))
        price_filters = sorted(set([item['price'] for item in inventory]))
        quantity_filters = sorted(set([item['quantity'] for item in inventory]))

        return render_template(
            'inventory.html',
            message = message,
            message_color = message_color,
            inventory = inventory,
            department_filters = department_filters,
            price_filters = price_filters,
            quantity_filters = quantity_filters,
            department_filter = department_filter,
            price_filter = price_filter,
            quantity_filter = quantity_filter,
        )

@inventory_app.route("/stock_report", methods=['GET'])
def stock_report():
    """Build stock report screen."""

    with Data() as data_handle:
        inventory = sorted(data_handle.fetch_inventory(), key=lambda item: item['product'])

        return render_template(
            'stock.html',
            inventory = inventory,
        )
