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

class config():
    def __init__(self, collection=None, meta=None):
        if meta is not None:
            if "config" in meta:
                self.toml_file = meta["config"]
                self.baseConfig = self.requireConfig(self.toml_file)
        else:
            self.toml_file = "./config/config.toml"
            self.baseConfig = self.requireConfig(self.toml_file)

    def overrideToml(self, base, overrides):
        for item in overrides.items():
            key = item[0]
            value = item[1]
            if isinstance(value, dict):
                base[key] = self.overrideToml(base[key], value)
            else:
                base[key] = value

        return base
    
    def findConfig(self):
        paths = [
            './config.toml',
            '../config.toml',
            '../config/config.toml',
            './config/config.toml'
        ]
        foundPath = None
        
        for path in paths:
            thisdir = os.getcwd() 
            this_path = os.path.realpath(os.path.join(thisdir, path))
            if os.path.exists(this_path):
                foundPath = this_path
            
        return foundPath if foundPath != None else None

    def loadConfig(self, configPath, overrides):
        with open(configPath) as f:
            config = toml.load(f)
        return self.overrideToml(config, overrides)

    def requireConfig(self, opts):
        configPath = None
        if type(opts) == str and os.path.exists(opts):
            configPath = opts
        elif  type(opts) == dict and 'config' in opts and os.path.exists(opts['config']):
            configPath = opts['config']
        else:
            configPath = self.findConfig()

        if not configPath:
            print('no config file found')
            print('make sure config.toml is in the working directory')
            print('or specify path using --config')
            exit(1)

        return self.loadConfig(configPath, opts)
