import datasets
import ipfs_datasets_py
import os 

class IpfsFaissDataset():
    def __init__(self, collection=None, meta=None):
        self.ipfs_faiss = []
        if meta is None:
            meta = {}
        else:
            self.hf_path = meta["hf_path"]
            self.folder_pins = meta["folder_pins"]
            self.file_pins = meta["file_pins"]

        if os.getuid() == 0:
            if meta is not None and type (meta) == dict:
                if "local_path" in meta:
                    self.local_path = meta["local_path"]			
                else:
                    self.local_path = "/huggingface/"
                if "ipfs_path" in meta:
                    self.ipfs_path = meta["ipfs_path"]
                else:
                    self.ipfs_path = "/ipfs/"
                if "s3_cfg" in meta:
                    self.s3cfg = meta["s3_cfg"]
                else:
                    self.s3cfg = None
                if "role" in meta:
                    self.role = meta["role"]
                else:
                    self.role = "leecher"
            else:
                self.local_path = "/huggingface/"
                self.ipfs_path = "/ipfs/"
                self.s3cfg = None
                self.role = "leecher"
                meta = {
					"local_path": self.local_path,
					"ipfs_path": self.ipfs_path,
					"s3_cfg": self.s3cfg,
					"role": self.role
				}
        else:
            if meta is not None and type (meta) == dict:
                if "local_path" in meta:
                    self.local_path = meta["local_path"]
                else:
                    self.local_path = os.path.join(os.getenv("HOME") , ".cache/huggingface/")
                if "ipfs_path" in meta:
                    self.ipfs_path = meta["ipfs_path"]
                else:
                    self.ipfs_path = os.path.join(os.getenv("HOME") , ".cache/ipfs/")
                if "s3_cfg" in meta:
                    self.s3cfg = meta["s3_cfg"]
                else:
                    self.s3cfg = None
                if "role" in meta:
                    self.role = meta["role"]
                else:
                    self.role = "leecher"
            else:
                self.local_path = os.path.join(os.getenv("HOME") , ".cache/huggingface/")
                self.ipfs_path = os.path.join(os.getenv("HOME") , ".cache/ipfs/")
                self.s3cfg = None
                self.role = "leecher"
                meta = {
                    "local_path": self.local_path,
                    "ipfs_path": self.ipfs_path,
                    "s3_cfg": self.s3cfg,
                    "role": self.role
				}
        from ipfs_datasets.model_manager import model_manager as model_manager
        self.model_manager = model_manager(collection, meta)
        self.model_manager.load_collection_cache()
        self.model_manager.state()
				
    def download(self, **kwargs):
		# NOTE: Add kwarg for output directory where downloads are stored
		# if "local_path" in kwargs:
		# 	self.local_path = kwargs["local_path"]
		# if "ipfs_path" in kwargs:
		# 	self.ipfs_path = kwargs["ipfs_path"]

        model_name = None
        cid = None
        if "model_name" in kwargs:
            if "/" in kwargs["model_name"]:
                model_name = kwargs["model_name"].split("/")[1]
                pass
            elif "https://" in kwargs["model_name"]:
                model_name = kwargs["model_name"].split("/")[-1]
                pass
            else:
                model_name = kwargs["model_name"]
            pass
        elif "cid" in kwargs:
            cid = kwargs["cid"]
        if model_name != None:
            try:
                results = self.model_manager.download_model(model_name, **kwargs)
            except Exception as e:
                raise e
            finally:
                pass
            return os.path.join(self.local_path, model_name)
        else:
            try:
                results = self.model_manager.download_ipfs(cid, os.path.join(self.local_path, cid), **kwargs)
            except Exception as e:
                raise e
            finally:
                pass
            return os.path.join(self.local_path, cid)
        pass

    def query_faiss(self, query_vector, k, index):
        return index.search(query_vector, k)

    def join_ipfs_faiss(self, dataset, folder_pins, file_pins):
        merged_dataset = datasets.Dataset()
        return merged_dataset    

    def test():
        return "test"