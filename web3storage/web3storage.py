from config import config
import os
import sys
import json

class web3storage():
    def __init__( self, collection=None, meta=None):
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

    def web3storage_test(self, config, **kwargs):
        
        return False

    def web3storage_push(self, pin, **kwargs):
        config = self.config
        
        return False
    
        
    def web3storage_state(self, **kwargs):
        config = self.config
        
        if self.state is None:
            self.state = {
                "pinata": {
                    "status": "offline",
                    "message": "ready"
                },
                "pins": [],
                "quota": float(self.config.baseConfig["WEB3STORAGE"]["quota"]),
                "usage": "0",
                "remaining": float(self.config.baseConfig["WEB3STORAGE"]["quota"]) - 0
            }
        else:
            self.state = self.web3storage_calc_state(self.state)

        state = self.state
        return state
    
    def web3storage_calc_state(state):

        state["remaining"] = state["quota"] - state["usage"]
        
        return state