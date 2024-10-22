import os
import sys
import json
from config import config

class pinata():
    def __init__(self, collection=None, meta=None):
        if meta is not None:
            if "api_key" in meta:
                self.api_key = meta["api_key"]
            if "config" in meta:
                self.config = meta["config"]
            if "local_path" in meta:
                self.local_path = meta["local_path"]
        else:
            meta = {}
            self.toml_file = "config.toml"
            self.config = config()

        self.state = None

    def pinata_test(self, config, **kwargs):

        return False
    
    def pinata_push(self, pin, **kwargs):
        config = self.config
        return False
    
    def pinata_pull(self, pin, **kwargs):
        config = self.config
        return False
    
    def pinata_state(self, **kwargs):
        config = self.config
    
        if self.state is None: 
            self.state = {
                "pinata": {
                    "status": "offline",
                    "message": "ready"
                },
                "pins": [],
                "quota": float(self.config.baseConfig["PINATA"]["quota"]),
                "usage": "0",
                "remaining": float(self.config.baseConfig["PINATA"]["quota"]) - 0
            }
        else:
            self.state = self.pinata_calc_state(self.state)
        
        state = self.state
        return state
    
    def pinata_calc_state(state):

        state["remaining"] = state["quota"] - state["usage"]
        
        return state
    
