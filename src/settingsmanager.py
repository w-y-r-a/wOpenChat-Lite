from configparser import ConfigParser
import pathlib  

config_path = pathlib.Path(__file__).parent / "config.ini"

config = ConfigParser()
config.read(config_path)

def read_config(section: str, key: str):
    try:
        return config[section][key]   # section first, then key
    except KeyError:
        return "Config item Not Found"
