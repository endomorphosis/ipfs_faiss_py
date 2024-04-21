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

        self.pinata_quota = None
        self.web3storage_quota = None
        self.lighthouse_quota = None
        self.filebase_quota = None

        self.pinata_usage = None
        self.web3storage_usage = None
        self.lighthouse_usage = None
        self.filebase_usage = None

        self.pinata_pins = None
        self.web3storage_pins = None
        self.lighthouse_pins = None
        self.filebase_pins = None

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

        if "PINATA" in list(self.config.baseConfig.keys()):
            self.pinata_config = self.config.baseConfig["PINATA"]
            self.pinata_state = self.pinata.pinata_state()
        else:
            self.pinata_config = None
            self.pinata_state = None
        if "WEB3STORAGE" in list(self.config.baseConfig.keys()):
            self.web3storage_config = self.config.baseConfig["WEB3STORAGE"]
            self.web3storage_state = self.web3storage.web3storage_state()
        else:
            self.web3storage_config = None
            self.web3storage_state = None
        if "LIGHTHOUSE" in list(self.config.baseConfig.keys()):
            self.lighthouse_config = self.config.baseConfig["LIGHTHOUSE"]
            self.lighthouse_state = self.lighthouse.lighthouse_state()
        else:
            self.lighthouse_config = None
            self.lighthouse_state = None
        if "FILEBASE" in list(self.config.baseConfig.keys()):
            self.filebase_config = self.config.baseConfig["FILEBASE"]
            self.filebase_state = self.filebase.filebase_state()
        else:
            self.filebase_config = None
            self.filebase_state = None    

        if self.web3storage_config != None:
            self.web3storage_quota = self.web3storage_state["quota"]
            self.web3storage_usage = self.web3storage_state["usage"]
            self.web3storage_pins = self.web3storage_state["pins"]

        if self.lighthouse_config != None:
            self.lighthouse_quota = self.lighthouse_state["quota"]
            self.lighthouse_usage = self.lighthouse_state["usage"]
            self.lighthouse_pins = self.lighthouse_state["pins"]
        
        if self.filebase_config != None:
            self.filebase_quota = self.filebase_state["quota"]
            self.filebase_usage = self.filebase_state["usage"]
            self.filebase_pins = self.filebase_state["pins"]

        if self.pinata_config != None:
            self.pinata_quota = self.pinata_state["quota"]
            self.pinata_usage = self.pinata_state["usage"]
            self.pinata_pins = self.pinata_state["pins"]

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
            return push_pin_web3storage
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
            
        if "file_by_folder_pins" in kwargs:
            folder = kwargs["file_by_folder_pins"]
        else:
            folder = None

        if "folder_pins" in kwargs:
            folders_pins = kwargs["folder_pins"]
        else:
            folder_pins = None

        if "file_pins" in kwargs:
            file_pins = kwargs["file_pins"]
        else:
            file_pins = None
                    
        if "path"in kwargs:
            path = kwargs["path"]
        elif "path" in pin:
            path = pin['path']
        else:    
            path = None
        
        pinata_remaining = float(self.pinata_quota) - float(self.pinata_usage)
        web3storage_remaining = float(self.web3storage_quota) - float(self.web3storage_usage)
        lighthouse_remaining = float(self.lighthouse_quota) - float(self.lighthouse_usage)
        filebase_remaining = float(self.filebase_quota) - float(self.filebase_usage)

        if "or" in folder:
            if pinata_remaining > 0:
                push_pin_pinata = self.pinata_push(pin, path=path)
            else:
                push_pin_pinata = None
            if web3storage_remaining > 0:
                push_pin_web3storage = self.web3storage_push(pin, path=path)
            else:
                push_pin_web3storage = None
            if lighthouse_remaining > 0:
                push_pin_lighthouse = self.lighthouse_push(pin, path=path)
            else:
                push_pin_lighthouse = None
            if filebase_remaining > 0:
                push_pin_filebase = self.filebase_push(pin, path=path)
            else:
                push_pin_filebase = None
        else:
            if web3storage_remaining > 0:
                push_pin_web3storage = self.web3storage_push(pin, path=path)
            else:
                push_pin_web3storage = None
            push_pin_pinata = None
            push_pin_lighthouse = None
            push_pin_filebase = None
            pass

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