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
            elif "api_key" in list(dir(self)):
                self.api_key = self["api_key"]
            else:
                self.api_key = None
                        
            if "config" in meta:
                self.config = meta["config"]
            elif "config" in list(dir(self)):
                self.config = self["config"]
            else :
                self.config = config.config("../config/config.toml")
            
            if "local_path" in meta:
                self.local_path = meta["local_path"]
            elif "local_path" in list(dir(self)):
                self.local_path = self["local_path"]    
            else:                
                self.local_path = None
            
            if "w3cfg" in meta:
                self.w3cfg = meta["w3cfg"]
            elif "w3cfg" in list(dir(self)):
                self.w3cfg = self["w3cfg"]
            else:
                self.w3cfg = subprocess.check_output("which w3", shell=True)
        else:
            meta = {}
            self.toml_file = "config.toml"
            this_config = config.config({"config" :"./config/config.toml"})
            self.config = this_config

        self.state = None

    def ready(self):
        self.w3 = None
        try:
            w3 = subprocess.check_output("which w3", shell=True)
            w3 = w3.decode("utf-8")
            self.w3 = w3
            #self.w3cfg = subprocess.check_output("which w3cfg", shell=True).toString()
        except Exception as e:
            print (e)
            while "w3" not in list(dir(self)) or  self.w3 is None or int(self.w3) == 0 :
                print("w3 not found")
                ps_command = "ps -ef | grep w3 | grep install | grep -v grep | wc -l"
                ps_result = subprocess.check_output(ps_command, shell=True) 
                ps_result = ps_result.decode("utf-8")
                if int(ps_result) == 0:
                    install_command = "npm install -g @web3-storage/w3cli "
                    print("Please install w3 by running the following command: " + install_command)
                    os.system(install_command)
                    ps_command = "ps -ef | grep w3 | grep install | grep -v grep | wc -l"
                    ps_result = subprocess.check_output(ps_command, shell=True)
                    ps_result = ps_result.decode("utf-8")
                    self.w3 = ps_result
                else:
                    try:
                        self.w3 = subprocess.check_output("which w3", shell=True)
                        self.w3 = self.w3.decode("utf-8")
                    except:
                        self.w3 = None
                    finally:
                        pass

            w3 = self.w3
            while "w3cfg" not in list(dir(self)) or  self.w3cfg is None or int(self.w3cfg) == 0 :
                print("w3cfg not found")
                ps_command = "ps -ef | grep w3cfg | grep install | grep -v grep | wc -l"
                ps_result = subprocess.check_output(ps_command, shell=True) 
                if int(ps_result) == 0:
                    install_command = "sudo npm install -g @web3-storage/w3cfg "
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

            w3cfg = self.w3cfg

            while "ipfs_car" not in list(dir(self)) or  self.ipfs_car is None or int(self.ipfs_car) == 0 :
                print("ipfs-car not found")
                ps_command = "ps -ef | grep ipfs-car | grep install | grep -v grep | wc -l"
                ps_result = subprocess.check_output(ps_command, shell=True) 
                if int(ps_result) == 0:
                    install_command = "sudo npm install -g ipfs-car "
                    print("Please install ipfs-car by running the following command: " + install_command)
                    os.system(install_command)
                    ps_command = "ps -ef | grep ipfs-car | grep install | grep -v grep | wc -l"
                    ps_result = subprocess.check_output(ps_command, shell=True)
                    
                else:
                    try:
                        self.ipfs_car = subprocess.check_output("which ipfs-car", shell=True)
                    except:
                        self.ipfs_car = None
                    finally:
                        pass
            ipfs_car = self.ipfs_car



        command = "w3 login " + self.config.baseConfig["WEB3STORAGE"]["email"]
        try:        
            self.creds = subprocess.check_output(command, shell=True)
        except Exception as e:
            print(e)
            print("Please login to web3.storage by running the following command: " + command)
            os.system(command)
            self.creds = subprocess.check_output(command, shell=True)
        finally:
            pass
        self.state = None
        web3storage_test_connection = self.web3storage_test_connection()
        return web3storage_test_connection


    def web3storage_create(self, config, **kwargs):
        if "space_name" in kwargs:
            space_name = kwargs["space_name"]
        elif "space_name" in list(dir(self)):
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
                for line in config_toml:
                    if "space_name" in line:
                        replace_line = line
                        config_toml = config_toml.replace(replace_line, "space_name="+space_name+"\n")
                        
            with open("./config/config.toml", 'w') as f:
                f.write(config_toml)
        
            self.config = config.config("../config/config.toml")
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

    def web3storage_test_connection(self, **kwargs):
        command = "w3 --version"
        results = subprocess.check_output(command, shell=True)
        results = results.decode("utf-8")
        print(results)
        self.web3storage_test_connection_results = results
        return results
    
    def web3storage_test(self, **kwargs):
        random_pin = ""
        random_pin = "QmXBUkLywjKGTWNDMgxknk6FJEYu9fZaEepv3djmnEqEqD"

        test_connection = self.web3storage_test_connection(**kwargs)
        if "did_key" in kwargs:
            did_key = kwargs["did_key"]
        elif "did_key" in list(dir(self)):
            did_key = self["did_key"]
        elif "did_key" in self.config.baseConfig["WEB3STORAGE"]:
            did_key = self.config.baseConfig["WEB3STORAGE"]["did_key"]
        else:
            did_key = self.web3storage_create(space_name=self.config.baseConfig["WEB3STORAGE"]["space_name"])
            with open("./config/config.toml", 'r') as f:
                config_toml = f.read()
                for line in config_toml:
                    if "did_key" in line:
                        replace_line = line
                        config_toml = config_toml.replace(replace_line, "did_key="+did_key+"\n")
                        break
            with open("./config/config.toml", 'w') as f:
                f.write(config_toml)

        if "auth_key" in kwargs:
            auth_key = kwargs["auth_key"]
        elif "auth_key" in list(dir(self)):
            auth_key = self["auth_key"]
        elif "auth_key" in self.config.baseConfig["WEB3STORAGE"]:
            auth_key = self.config.baseConfig["WEB3STORAGE"]["auth_key"]
        else:
            try:
                auth_key = self.web3storage_bridge(key=did_key)
                with open("./config/config.toml", 'r') as f:
                    config_toml = f.read()
                    for line in config_toml:
                        if "auth_key" in line:
                            replace_line = line
                            config_toml = config_toml.replace(replace_line, "auth_key="+auth_key+"\n")
                            break
                with open("./config/config.toml", 'w') as f:
                    f.write(config_toml)
            except Exception as e:
                print(e)
                print("web3storage_test")
                print("Missing required parameters")
                print("DID Key: " + str(did_key))
                print("Auth Key: " + str(auth_key))
                raise Exception("Missing required parameters")
                return False

        if did_key is not None and auth_key is not None:
            web3storage_request = self.web3storage_request( random_pin,
                                                            did_kay =  did_key,
                                                            auth_key = auth_key
                                                        )
            return True
        else:
            print("web3storage_test")
            print("Missing required parameters")
            print("DID Key: " + str(did_key))
            print("Auth Key: " + str(auth_key))
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

    def web3storage_can_add(self, pin, **kwargs):
        if "path" in kwargs:
            path = kwargs["path"]

        command = f"""ipfs dag"""      

    def web3storage_push(self, pin, **kwargs):
        if "path" in kwargs and kwargs["path"] is not None:
            path = kwargs["path"]
        if "local_path" in kwargs and kwargs["local_path"] is not None:
            local_path = kwargs["local_path"]
        elif "local_path" in list(dir(self)) and self.local_path is not None:
            local_path = self.local_path
        elif "local_path" in self.config.baseConfig["PATHS"] and self.config.baseConfig["PATHS"]["local_path"] is not None:
            local_path = self.config.baseConfig["PATHS"]["local_path"]
        if "space" in kwargs and kwargs["space"] is not None:
            space = kwargs["space"]
        elif "space" in list(dir(self)) and self.space is not None:
            space = self.space
        elif "space" in self.config.baseConfig["WEB3STORAGE"] and self.config.baseConfig["WEB3STORAGE"]["space"] is not None:
            space = self.config.baseConfig["WEB3STORAGE"]["space"]

        set_space_command = "w3 space use " + space
        results = subprocess.check_output(set_space_command, shell=True)
        results = results.decode("utf-8")
        print(results)


        if path.startswith("/"):
            path = path[1:]

        found = False
        if found == False:
            joined_path = os.path.realpath(os.path.join(local_path, path))
            if joined_path.endswith("json"):
                if os.path.exists(path) or os.path.exists(joined_path):
                    if os.path.exists(path):
                        command = "w3 up " + path
                    else:
                        command = "w3 up " + joined_path
                    try:
                        results = subprocess.check_output(command, shell=True)
                        results = results.decode("utf-8")
                        new_cid = str(results.split("link/ipfs/")[-1])
                    except Exception as e:
                        print(e)
                        print("web3storage_push")
                        print("Failed to upload")
                        print("Path: " + str(path))
                        raise Exception("Failed to upload")
                    finally:
                        results_string = str("added") + str("\t") + str(new_cid).replace("\n","") + str("\t") + str(path)
                        cmd = str("echo '" + results_string + "' >> ./web3storage_pins.tsv")
                        os.system(cmd)
                        return new_cid

                    
        elif found == False:
                print("web3storage_push")
                print("Invalid path")
                print("Path: " + str(path))
                raise Exception("Invalid path")
                return False
    

    def web3storage_push_local(self, pin, **kwargs):
        path = None
        if isinstance(pin, dict):
            if "path" in kwargs:
                path = kwargs["path"]
        
        if path != None:
            if path.endswith("json"):
                command = "w3 up" + path
                results = subprocess.check_output(command, shell=True)
                print("uploading " + path)
                print(results)
                return results
            else:
                print("web3storage_push_local")
                print("Invalid path")
                print("Path: " + str(path))
                raise Exception("Invalid path")
                return False

    def web3storage_push_car(self, pin, **kwargs):

        try:
            command = "ipfs dag export " + pin + " > " + pin + ".car"
            results = subprocess.check_output(command, shell=True)
            results_car_file = results.decode("utf-8")
            print(results_car_file)
        except Exception as e:
            print(e)
            print("web3storage_push")
            print("Missing required parameters")
            print("Pin: " + str(pin))
            raise Exception("Missing required parameters")
            return False
        finally:
            pass

        try:
            command = "w3 can store add " + car_file
            results = subprocess.check_output(command, shell=True)
            results_store_add = results.decode("utf-8")
            print(results_store_add)
        except Exception as e:
            print(e)
            print("web3storage_push")
            print("Missing required parameters")
            print("Pin: " + str(pin))
            raise Exception("Missing required parameters")
            return False
        finally:
            pass

        try:
            command = "w3 upload add " + car_file
            results = subprocess.check_output(command, shell=True)
            results_upload_add = results.decode("utf-8")
            print(results_upload_add)
        except Exception as e:
            print(e)
            print("web3storage_push")
            print("Missing required parameters")
            print("Pin: " + str(pin))
            raise Exception("Missing required parameters")
            return False
        finally:
            pass

        results = {
            "car_file": results_car_file,
            "store_add": results_store_add,
            "upload_add": results_upload_add
        }

        return results


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

if __name__ == '__main__':
    test_web3storage = web3storage()
    test_web3storage.ready()
    test_web3storage.web3storage_test()
    test_web3storage.web3storage_state()
    test_web3storage.web3storage_create(
        "test",
        space_name = "test"
        )
    test_web3storage.web3storage_bridge("test")
    test_web3storage.web3storage_request("test", "pin")

