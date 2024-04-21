import sys
import os
import json
import subprocess
from subprocess import * 
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import config
import requests

class web3storage():
    def __init__( self, collection=None, meta=None):
        w3cfg = None
        if meta is not None:
            if "api_key" in meta:
                self.api_key = meta["api_key"]
            elif "api_key" in list(self.keys()):
                self.api_key = self["api_key"]
            else:
                self.api_key = None
                        
            if "config" in meta:
                self.config = meta["config"]
            elif "config" in list(self.keys()):
                self.config = self["config"]
            else :
                self.config = config()
            
            if "local_path" in meta:
                self.local_path = meta["local_path"]
            elif "local_path" in list(self.keys()):
                self.local_path = self["local_path"]    
            else:                
                self.local_path = None
            
            if "w3cfg" in meta:
                self.w3cfg = meta["w3cfg"]
            elif "w3cfg" in list(self.keys()):
                self.w3cfg = self["w3cfg"]
            else:
                self.w3cfg = subprocess.check_output("which w3cfg", shell=True)
        else:
            meta = {}
            self.toml_file = "config.toml"
            self.config = config()

        self.state = None
        self.ready()

    def ready(self):
        try:
            self.w3cfg = subprocess.check_output("which w3cfg", shell=True).toString()
        except:
            while "w3cfg" not in list(dir(self)) or  self.w3cfg is None or int(self.w3cfg) == 0 :
                print("w3cfg not found")
                ps_command = "ps -ef | grep w3cfg | grep install | grep -v grep | wc -l"
                ps_result = subprocess.check_output(ps_command, shell=True) 
                if int(ps_result) == 0:
                    install_command = "npm install -g @web3api/w3cfg"
                    print("Please install w3cfg by running the following command: " + install_command)
                    os.system(install_command)
                    ps_command = "ps -ef | grep w3cfg | grep install | grep -v grep | wc -l"
                    ps_result = subprocess.check_output(ps_command, shell=True)
                    
                else:
                    try:
                        self.w3cfg = subprocess.check_output("which w3cfg", shell=True)
                    except:
                        self.w3cfg = None
                    finally:
                        pass

            w3cfg = self,w3cfg
    
        while int(self.w3cfg) == 0:
            print("w3cfg not found")
            install_command = "npm install -g @web3api/w3cfg"
            print("Please install w3cfg by running the following command: " + install_command)
            install_result = subprocess.check_output(install_command, shell=True)
            print(install_result)
            self.w3cfg = subprocess.check_output("which w3cfg", shell=True)
            
        command = "w3cfg login " + self.config.baseConfig["WEB3STORAGE"]["email"]
        self.creds = subprocess.check_output(command, shell=True)
        self.state = None
        web3storage_test_connection = self.web3storage_test_connection()
        return web3storage_test_connection


    def web3storage_create(self, config, **kwargs):
        if "space_name" in kwargs:
            space_name = kwargs["space_name"]
        elif "space_name" in list(self.keys()):
            space_name = self["space_name"]
        elif "space_name" in self.config.baseConfig["WEB3STORAGE"]:
            space_name = self.config.baseConfig["WEB3STORAGE"]["space_name"]
        else:
            print("web3storage_create")
            print("Missing required parameters")
            print("Space Name: " + str(space_name))
            raise Exception("Missing required parameters")

        if space_name is not None:
            print("web3storage_create")
            command ="w3 space create --name " + space_name
            results = subprocess.check_output(command, shell=True)
            with open("./config/config.toml", 'w') as f:
                config_toml = f.read(results)
        
            config_toml = config_toml.replace("space_name", space_name) 
            with open("./config/config.toml", 'w') as f:
                f.write(config_toml)
        
            self.config = config()
            self.config.baseConfig["WEB3STORAGE"]["space_name"] = space_name
            return self.config

    def web3storage_bridge(self, config, **kwargs):
        if "key" in kwargs:
            key = kwargs["key"]
        elif "key" in list(self.keys()):
            key = self["key"]
        elif "key" in self.config.baseConfig["WEB3STORAGE"]:
            key = self.config.baseConfig["WEB3STORAGE"]["key"]

        if key is not None:
            command  = "w3 bridge generate-tokens did:key:"+key+"  --can 'store/add' --can 'upload/add' --can 'upload/list' --expiration `date -v +24H +%s`"
            results = subprocess.check_output(command, shell=True)
            return results
        else:
            print("web3storage_bridge")
            print("Missing required parameters")
            print("Key: " + str(key))
            raise Exception("Missing required parameters")

    def web3storage_test_connection(self, config, **kwargs):
        command = "w3 --version"
        results = subprocess.check_output(command, shell=True)
        self.web3storage_test_connection_results = results
        return results
    
    def web3storage_test(self, config, **kwargs):
        ready = self.ready(config, **kwargs)

        didKey = self.web3storage_create(space_name=self.config.baseConfig["WEB3STORAGE"]["space_name"])
        authkey = self.web3storage_bridge(key=didKey)

        if didKey is not None and authkey is not None:
            web3storage_request = self.web3storage_request(didKey, authkey)
            return True
        else:
            print("web3storage_test")
            print("Missing required parameters")
            print("DID Key: " + str(didKey))
            print("Auth Key: " + str(authkey))
            raise Exception("Missing required parameters")
            return False

    def web3storage_request(self, pin, **kwargs):
        config = self.config
        auth_key = self.config.baseConfig["WEB3STORAGE"]["auth_key"]
        ipfs_endpoint = self.config.baseConfig["WEB3STORAGE"]["ipfs_endpoint"]
        https_endpoint = self.config.baseConfig["WEB3STORAGE"]["https_endpoint"]
        cid = None
        path = None

        if "pin" in kwargs:
            cid = kwargs["pin"]
        elif isinstance(pin, dict) and "hash" in pin:
            cid = pin["hash"]
        elif isinstance(pin, str):
            cid = pin

        if "path" in kwargs:
            path = kwargs["path"]
        elif isinstance(pin, dict) and "path" in pin:
            path = pin["path"]
        elif isinstance(pin, str):
            path = pin
        
        if cid is not None and path is not None and auth_key is not None:
            command = f"""curl -X POST '{https_endpoint}' \
            --header 'Accept: */*' \
            --header 'Authorization: Bearer {auth_key}' \
            --header 'Content-Type: application/json' \
            -d '{{
            \"cid\": \"{cid}\",
            \"name\": \"{path}\"
            }}' """

            response = requests.post(https_endpoint, headers={'Accept': '*/*', 'Authorization': f'Bearer {auth_key}', 'Content-Type': 'application/json'}, json={'cid': cid, 'name': path})
            command.replace("$(auth_key)", auth_key)
            command.replace("$(cid)", cid)
            command.replace("$(path)", path)
            command.replace("$(ipfs_endpoint)", ipfs_endpoint)

            command_results = subprocess.check_output(command, shell=True)
            return command_results
        else:
            print("Missing required parameters")
            print("CID: " + str(cid))
            print("Path: " + str(path))
            print("Auth Key: " + str(auth_key))
            raise Exception("Missing required parameters")


    def web3storage_push(self, pin, **kwargs):
        return False
        config = self.config
        auth_key = self.config.baseConfig["WEB3STORAGE"]["auth_key"]
        https_endpoint = self.config.baseConfig["WEB3STORAGE"]["https_endpoint"]
        cid = None
        path = None

        if "pin" in kwargs:
            cid = kwargs["pin"]
        elif isinstance(pin, dict) and "hash" in pin:
            cid = pin["hash"]
        elif isinstance(pin, str):
            cid = pin

        if "path" in kwargs:
            path = kwargs["path"]
        elif isinstance(pin, dict) and "path" in pin:
            path = pin["path"]
        elif isinstance(pin, str):
            path = pin
        
        if cid is not None and path is not None and auth_key is not None:
            command = f"""curl -X POST '{https_endpoint}' \
            --header 'Accept: */*' \
            --header 'Authorization: Bearer {auth_key}' \
            --header 'Content-Type: application/json' \
            -d '{{
            \"cid\": \"{cid}\",
            \"name\": \"{path}\"
            }}' """

            response = requests.post(https_endpoint, headers={'Accept': '*/*', 'Authorization': f'Bearer {auth_key}', 'Content-Type': 'application/json'}, json={'cid': cid, 'name': path})
            command.replace("$(auth_key)", auth_key)
            command.replace("$(cid)", cid)
            command.replace("$(path)", path)
            command.replace("$(ipfs_endpoint)", https_endpoint)

            command_results = subprocess.check_output(command, shell=True)
            return command_results
        else:
            print("Missing required parameters")
            print("CID: " + str(cid))
            print("Path: " + str(path))
            print("Auth Key: " + str(auth_key))
            raise Exception("Missing required parameters")
        

    def web3storage_push_bak(self, pin, **kwargs):
        config = self.config
        auth_key = self.config.baseConfig["WEB3STORAGE"]["auth_key"]
        ipfs_endpoint = self.config.baseConfig["WEB3STORAGE"]["ipfs_endpoint"]
        cid = None
        path = None

        if "pin" in kwargs:
            cid = kwargs["pin"]
        elif isinstance(pin, dict) and "hash" in pin:
            cid = pin["hash"]
        elif isinstance(pin, str):
            cid = pin

        if "path" in kwargs:
            path = kwargs["path"]
        elif isinstance(pin, dict) and "path" in pin:
            path = pin["path"]
        elif isinstance(pin, str):
            path = pin
        
        if cid is not None and path is not None and auth_key is not None:
            command = f"""curl -X POST '{ipfs_endpoint}' \
            --header 'Accept: */*' \
            --header 'Authorization: Bearer {auth_key}' \
            --header 'Content-Type: application/json' \
            -d '{{
            \"cid\": \"{cid}\",
            \"name\": \"{path}\"
            }}' """

            response = requests.post(ipfs_endpoint, headers={'Accept': '*/*', 'Authorization': f'Bearer {auth_key}', 'Content-Type': 'application/json'}, json={'cid': cid, 'name': path})
            command.replace("$(auth_key)", auth_key)
            command.replace("$(cid)", cid)
            command.replace("$(path)", path)
            command.replace("$(ipfs_endpoint)", ipfs_endpoint)

            command_results = subprocess.check_output(command, shell=True)
            return command_results
        else:
            print("Missing required parameters")
            print("CID: " + str(cid))
            print("Path: " + str(path))
            print("Auth Key: " + str(auth_key))
            raise Exception("Missing required parameters")
    
    
    def web3storage_request(self, pin, **kwargs):
        config = self.config
        auth_key = self.config.baseConfig["WEB3STORAGE"]["auth_key"]
        ipfs_endpoint = self.config.baseConfig["WEB3STORAGE"]["ipfs_endpoint"]
        cid = None
        path = None

        if "pin" in kwargs:
            cid = kwargs["pin"]
        elif isinstance(pin, dict) and "hash" in pin:
            cid = pin["hash"]
        elif isinstance(pin, str):
            cid = pin

        if "path" in kwargs:
            path = kwargs["path"]
        elif isinstance(pin, dict) and "path" in pin:
            path = pin["path"]
        elif isinstance(pin, str):
            path = pin
        
        if cid is not None and path is not None and auth_key is not None:
            command = f"""curl -X POST '{ipfs_endpoint}' \
            --header 'Accept: */*' \
            --header 'Authorization: Bearer {auth_key}' \
            --header 'Content-Type: application/json' \
            -d '{{
            \"cid\": \"{cid}\",
            \"name\": \"{path}\"
            }}' """

            response = requests.post(ipfs_endpoint, headers={'Accept': '*/*', 'Authorization': f'Bearer {auth_key}', 'Content-Type': 'application/json'}, json={'cid': cid, 'name': path})
            command.replace("$(auth_key)", auth_key)
            command.replace("$(cid)", cid)
            command.replace("$(path)", path)
            command.replace("$(ipfs_endpoint)", ipfs_endpoint)

            command_results = subprocess.check_output(command, shell=True)
            return command_results
        else:
            print("Missing required parameters")
            print("CID: " + str(cid))
            print("Path: " + str(path))
            print("Auth Key: " + str(auth_key))
            raise Exception("Missing required parameters")
    
        

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