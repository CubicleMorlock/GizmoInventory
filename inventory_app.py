import re
import configargparse

from app import inventory_app
from app.utils.logging import make_logger

logger = make_logger()

if __name__ == '__main__':
    arg_parser = configargparse.ArgumentParser(default_config_files = ['./inventory_app.cfg'])
    arg_parser.add_argument(
        '--port',
        dest = 'port',
        env_var = 'INVENTORY_PORT',
        default = 8080,
        required = False,
        help = 'inventory app port'
    )

    parsed_args, unknown_args = arg_parser.parse_known_args()

    # used to do this using the netifaces module, picking the correct
    # interface to get the IP address, but that module requires a licensed
    # compiler on Windows
    inventory_app.run(host = '0.0.0.0', port = parsed_args.port, debug = True)

