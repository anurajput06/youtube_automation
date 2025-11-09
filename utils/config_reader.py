import configparser

def read_config(section='DEFAULT'):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config[section]
