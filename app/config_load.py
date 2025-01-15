import configargparse

def config_load():
    """Utility function for loading runtime configuration."""

    arg_parser = configargparse.ArgumentParser(default_config_files = ['./../inventory_app.cfg'])

    arg_parser.add_argument(
        '--database',
        dest = 'database',
        env_var = 'INVENTORY_DATABASE',
        default = 'inventory.db',
        required = False,
        help = 'inventory database'
    )
    arg_parser.add_argument(
        '--port',
        dest = 'port',
        env_var = 'INVENTORY_PORT',
        default = 8080,
        required = False,
        help = 'inventory app port'
    )

    parsed_args, unknown_args = arg_parser.parse_known_args()

    return parsed_args

