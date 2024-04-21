import os
import sys
import json
import requests
sys.path.append('./config')
sys.path.append('./web3storage')
sys.path.append('./filebase')
sys.path.append('./lighthouse')
sys.path.append('./pinata')
sys.path.append('..')
from config import config
from web3storage import web3storage
from filebase import filebase
from lighthouse import lighthouse
from pinata import pinata

class PinningApis():
    def __init__(self, collection=None, meta=None):
        self.toml_file = "config.toml"
        self.config = config()
        self.api_key = None
        self.local_path = None

        self.lighthouse = lighthouse()
        self.web3storage = web3storage()
        self.filebase = filebase()
        self.pinata = pinata()

        if meta is not None:
            if "api_key" in meta:
                self.api_key = meta["api_key"]
            if "config" in meta:
                self.toml_file = meta["config"]
                self.config = config(self.toml_file)
            if "local_path" in meta:
                self.local_path = meta["local_path"]
        
        else:
            meta = {}
            self.toml_file = "config.toml"
            self.config = config()

    def pinata_test(self, **kwargs):
        results = self.pinata.pinata_test()
        return results
    
    def web3storage_test(self, **kwargs):
        results = self.web3storage.web3storage_test()
        return results

    def lighthouse_test(self, **kwargs):
        results = self.lighthouse.lighthouse_test()
        return results
    
    def filebase_test(self, **kwargs):
        results = self.filebase.filebase_test()
        return False

    def web3storage_push(self, pin, **kwargs):
        results = self.web3storage.web3storage_push(pin)
        return results
    
    def pinata_push(self, pin, **kwargs):
        results = self.pinata.pinata_push(pin)
        return results
    
    def lighthouse_push(self, pin, **kwargs):
        results = self.lighthouse.lighthouse_push(pin)
        return results
    
    def filebase_push(self, pin, **kwargs):
        results = self.filebase.filebase_push(pin)
        return results

    def web3storage_pull(self, pin, **kwargs):
        results = self.web3storage.web3storage_pull(pin, **kwargs)
        return results
    
    def pinata_pull(self, pin, **kwargs):
        results = self.pinata.pinata_pull(pin, **kwargs)
        return False
    
    def lighthouse_pull(self, pin, **kwargs):
        results = self.lighthouse.lighthouse_pull(pin, **kwargs)
        return False
    
    def filebase_pull(self, pin, **kwargs):
        results = self.filebase.filebase_pull(pin, **kwargs)
        return False
    
    def ready_status(self, **kwargs):
        results = {
            "pinata": False,
            "web3storage": False,
            "lighthouse": False,
            "filebase": False,
        }

        if "pinata" in list(self.config.keys()):
            pinata_test = self.pinata_test()
            results["pinata"] = pinata_test

        if "web3storage" in list(self.config.keys()):
            web3storage_test = self.web3storage_test()
            results["web3storage"] = web3storage_test
        
        if "lighthouse" in list(self.config.keys()):
            lighthouse_test = self.lighthouse_test()
            results["lighthouse"] = lighthouse_test

        if "filebase" in list(self.config.keys()):
            filebase_test = self.filebase_test()
            results["filebase"] = filebase_test
        self.ready = results        
        return results
    
    def pin_push(self, pins, **kwargs):
        results = {}
        for pin in pins:
            pin_cid = pin['cid']

        if "src" in kwargs:
            src = kwargs["src"]
        else:
            src = None
        
        if src == "all":
            push_pin_pinata = self.pinata_push(pin)
            push_pin_web3storage = self.web3storage_push(pin)
            push_pin_lighthouse = self.lighthouse_push(pin)
            push_pin_filebase = self.filebase_push(pin)
        elif src == "pinata":
            push_pin_pinata = self.pinata_push(pin)
            return push_pin_pinata
        elif src == "web3storage":
            push_pin_web3storage = self.web3storage_push(pin)
            return push_pin_web3
        elif src == "lighthouse":
            push_pin_lighthouse = self.lighthouse_push(pin)
            return push_pin_lighthouse
        elif src == "filebase":
            push_pin_filebase = self.filebase_push(pin)
            return push_pin_filebase
        else:
            push_pin_pinata = self.pinata_push(pin)
            push_pin_web3storage = self.web3storage_push(pin)
            push_pin_lighthouse = self.lighthouse_push(pin)
            push_pin_filebase = self.filebase_push(pin)
            
        results = {
            "pinata": push_pin_pinata,
            "web3storage": push_pin_web3storage,
            "lighthouse": push_pin_lighthouse,
            "filebase": push_pin_filebase,
        }

        return results
    
    def pin_push_all_every(self, pins, **kwargs):
        results = {}
        for pin in pins:
            pin_cid = pin['cid']
            push_pin_pinata = self.pinata_push(pin_cid)
            push_pin_web3storage = self.web3storage_push(pin_cid)
            push_pin_lighthouse = self.lighthouse_push(pin_cid)
            push_pin_filebase = self.filebase_push(pin_cid)

        results = {
            "pinata": push_pin_pinata,
            "web3storage": push_pin_web3storage,
            "lighthouse": push_pin_lighthouse,
            "filebase": push_pin_filebase,
        }
        pass

    def pin_push_one_every(self, pin, **kwargs):
        results = {}
        if "hash" in kwargs:
            pin_cid = kwargs["hash"]
        elif isinstance(pin, dict) and "hash" in pin:
            pin_cid = pin['hash']
        elif isinstance(pin, str):
            pin_cid = pin
        else:
            print("No hash provided")
            pin_cid = None
        
        if "path"in kwargs:
            path = kwargs["path"]
        elif "path" in pin:
            path = pin['path']
        else:    
            path = None

        push_pin_pinata = self.pinata_push(pin, path=path)
        push_pin_web3storage = self.web3storage_push(pin, path=path)
        push_pin_lighthouse = self.lighthouse_push(pin, path=path)
        push_pin_filebase = self.filebase_push(pin, path=path)

        results = {
            "pinata": push_pin_pinata,
            "web3": push_pin_web3storage,
            "lighthouse": push_pin_lighthouse,
            "filebase": push_pin_filebase,
        }
        pass

    def decide_fastest(self, **kwargs):
        if "decide" in kwargs:
            decide = kwargs["decide"]
            self.decide = decide
        else:
            if "decide" in self.keys():
                decide = self.decide
            else: 
                self.decide = "web3"
                decide = "web3"
        return decide

    def pin_pull_one_every(self, pins, **kwargs):
        results = {}
        for pin in pins:
            pin_cid = pin['cid']

        decide = self.decide_fastest()
        if decide == "pinata":
            pull_pin_pinata = self.pinata_pull(pin)
            return pull_pin_pinata
        elif decide == "web3storage":
            pull_pin_web3storage = self.web3storage_pull(pin)
            return pull_pin_web3storage
        elif decide == "lighthouse":
            pull_pin_lighthouse = self.lighthouse_pull(pin)
            return pull_pin_lighthouse
        elif decide == "filebase":
            pull_pin_filebase = self.filebase_pull(pin)
            return pull_pin_filebase
        elif decide == "all":
            pull_pin_pinata = self.pinata_pull(pin)
            pull_pin_web3storage = self.web3storage_pull(pin)
            pull_pin_lighthouse = self.lighthouse_pull(pin)
            pull_pin_filebase = self.filebase_pull(pin)
        elif decide == None:
            pull_pin_pinata = self.pinata_pull(pin)
            pull_pin_web3storage = self.web3storage_pull(pin)
            pull_pin_lighthouse = self.lighthouse_pull(pin)
            pull_pin_filebase = self.filebase_pull(pin)

        fastest = sorted([pull_pin_pinata, pull_pin_web3storage, pull_pin_lighthouse, pull_pin_filebase], key=lambda x: x['time'])
        decide = self.decide_fastest(fastest)
        results = {
            "fastest": fastest,
            "pinata": pull_pin_pinata,
            "web3storage": pull_pin_web3storage,
            "lighthouse": pull_pin_lighthouse,
            "filebase": pull_pin_filebase,
        }
        return results
    
    def test(self):

        return False
    
    def import_pins():
        
        return False
    
if __name__ == "__main__":
    test_pinset = PinningApis()
    test_pinset.test()
    pass