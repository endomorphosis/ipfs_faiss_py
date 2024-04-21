from .config import config

class PinningApis():
    def __init__(self, collection=None, meta=None):
        self.toml_file = "config.toml"
        self.config = config()
        self.api_key = None
        self.local_path = None

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

    def pinata_test(self):

        return False
    
    def web3_test(self):
            
        return False

    def lighthouse_test(self):
                
        return False
    
    def filebase_test(self):

        return False

    def web3_push(self, pin):
        return False
    
    def pinata_push(self, pin):
        return False
    
    def lighthouse_push(self, pin):
        return False
    
    def filebase_push(self, pin):
        return False

    def web3_pull(self, pin):
        return False
    
    def pinata_pull(self, pin):
        return False
    
    def lighthouse_pull(self, pin):
        return False
    
    def filebase_pull(self, pin):
        return False
    
    def ready_status(self, **kwargs):
        results = {
            "pinata": False,
            "web3": False,
            "lighthouse": False,
            "filebase": False,
        }

        if "pinata" in list(self.config.keys()):
            pinata_test = self.pinata_test()
            results["pinata"] = pinata_test

        if "web3" in list(self.config.keys()):
            web3_test = self.web3_test()
            results["web3"] = web3_test
        
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
            push_pin_web3 = self.web3_push(pin)
            push_pin_lighthouse = self.lighthouse_push(pin)
            push_pin_filebase = self.filebase_push(pin)
        elif src == "pinata":
            push_pin_pinata = self.pinata_push(pin)
            return push_pin_pinata
        elif src == "web3":
            push_pin_web3 = self.web3_push(pin)
            return push_pin_web3
        elif src == "lighthouse":
            push_pin_lighthouse = self.lighthouse_push(pin)
            return push_pin_lighthouse
        elif src == "filebase":
            push_pin_filebase = self.filebase_push(pin)
            return push_pin_filebase
        else:
            push_pin_pinata = self.pinata_push(pin)
            push_pin_web3 = self.web3_push(pin)
            push_pin_lighthouse = self.lighthouse_push(pin)
            push_pin_filebase = self.filebase_push(pin)
            
        results = {
            "pinata": push_pin_pinata,
            "web3": push_pin_web3,
            "lighthouse": push_pin_lighthouse,
            "filebase": push_pin_filebase,
        }

        return results
    
    def pin_push_all_every(self, pins):
        results = {}
        for pin in pins:
            pin_cid = pin['cid']
            push_pin_pinata = self.pinata_push(pin_cid)
            push_pin_web3 = self.web3_push(pin_cid)
            push_pin_lighthouse = self.lighthouse_push(pin_cid)
            push_pin_filebase = self.filebase_push(pin_cid)

        results = {
            "pinata": push_pin_pinata,
            "web3": push_pin_web3,
            "lighthouse": push_pin_lighthouse,
            "filebase": push_pin_filebase,
        }
        pass

    def pin_push_one_every(self, pin):
        results = {}
        pin_cid = pin['cid']

        push_pin_pinata = self.pinata_push(pin)
        push_pin_web3 = self.web3_push(pin)
        push_pin_lighthouse = self.lighthouse_push(pin)
        push_pin_filebase = self.filebase_push(pin)

        results = {
            "pinata": push_pin_pinata,
            "web3": push_pin_web3,
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

    def pin_pull_one_every(self, pins):
        results = {}
        for pin in pins:
            pin_cid = pin['cid']

        decide = self.decide_fastest()
        if decide == "pinata":
            pull_pin_pinata = self.pinata_pull(pin)
            return pull_pin_pinata
        elif decide == "web3":
            pull_pin_web3 = self.web3_pull(pin)
            return pull_pin_web3
        elif decide == "lighthouse":
            pull_pin_lighthouse = self.lighthouse_pull(pin)
            return pull_pin_lighthouse
        elif decide == "filebase":
            pull_pin_filebase = self.filebase_pull(pin)
            return pull_pin_filebase
        elif decide == "all":
            pull_pin_pinata = self.pinata_pull(pin)
            pull_pin_web3 = self.web3_pull(pin)
            pull_pin_lighthouse = self.lighthouse_pull(pin)
            pull_pin_filebase = self.filebase_pull(pin)
        elif decide == None:
            pull_pin_pinata = self.pinata_pull(pin)
            pull_pin_web3 = self.web3_pull(pin)
            pull_pin_lighthouse = self.lighthouse_pull(pin)
            pull_pin_filebase = self.filebase_pull(pin)

        fastest = sorted([pull_pin_pinata, pull_pin_web3, pull_pin_lighthouse, pull_pin_filebase], key=lambda x: x['time'])
        decide = self.decide_fastest(fastest)
        results = {
            "fastest": fastest,
            "pinata": pull_pin_pinata,
            "web3": pull_pin_web3,
            "lighthouse": pull_pin_lighthouse,
            "filebase": pull_pin_filebase,
        }
        return results
    
    def test():

        return False
    
    def import_pins():
        
        return False
    
if __name__ == "__main__":
    test_pinset = PinningApis()
    test_pinset.test()
    pass