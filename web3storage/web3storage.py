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
            self.w3cfg = subprocess.check_output("which w3cfg", shell=True)
        
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

        command ="w3 space create --name " + space_name
        results = subprocess.check_output(command, shell=True)
        key = results
        return results

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
        return results
    
    def web3storage_test(self, config, **kwargs):

        didKey = self.web3storage_create(space_name=self.config.baseConfig["WEB3STORAGE"]["space_name"])
        authkey = self.web3storage_bridge(key=didKey)

        if didKey is not None and authkey is not None:
            web3storage_request = self.web3storage_request(didKey, authkey)

        return True
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