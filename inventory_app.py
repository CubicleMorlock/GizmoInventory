from app import inventory_app
from app.config_load import config_load

if __name__ == '__main__':
    parsed_args = config_load()

    # used to do this using the netifaces module, picking the correct
    # interface to get the IP address, but that module requires a licensed
    # compiler on Windows
    inventory_app.run(host = '0.0.0.0', port = parsed_args.port, debug = True)

