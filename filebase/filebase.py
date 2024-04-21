class Filebase():
    def __init__( self, collection=None, meta=None):
        if meta is not None:
            if "api_key" in meta:
                self.api_key = meta["api_key"]
            if "config" in meta:
                self.config = meta["config"]
            if "local_path" in meta:
                self.local_path = meta["local_path"]
        self.filebase_test(self.config)

    def filebase_test(self, config, **kwargs):
        
        return False
    
    def filebase_push(self, pin, **kwargs):
        config = self.config
        return False
    
    def filebase_pull(self, pin, **kwargs):
        config = self.config
        return False