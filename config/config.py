import os
import tempfile
from tempfile import mkdtemp
from os import path
from os import listdir
from os.path import isfile, join
from os import walk
from os.path import isfile, join
from os import listdir
import toml

export class config:
    def __init__(self, api_key):
        self.toml_file = "config.toml"
        self.api_key = api_key
        self.baseConfig = {
        'master': {
            'port': 8080,
            'tempPath': tempfile.mkdtemp(prefix='cloudkit-', dir=os.tempdir)
        }
}

def overrideToml(base, overrides):
    for key, value in overrides.items():
        if isinstance(value, dict):
            base[key] = overrideToml(base.get(key, {}), value)
        else:
            base[key] = value

    return base



def findConfig():
    paths = [
        './config.toml',
        '../config.toml',
        '../config/config.toml',
        './config/config.toml'
    ]

    foundPath = next((p for p in paths if os.path.exists(p)), None)

    return os.path.abspath(foundPath) if foundPath else None

def loadConfig(configPath, overrides):
    with open(configPath) as f:
        config = toml.load(f)

    return overrideToml(baseConfig, config, overrides)

def requireConfig(opts):
    configPath = findConfig() or opts.get('config')

    if not configPath:
        print('no config file found')
        print('make sure config.toml is in the working directory')
        print('or specify path using --config')
        exit(1)

    return loadConfig(configPath, opts)
