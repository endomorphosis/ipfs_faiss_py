class Lighthouse():
    def __init__( self, collection=None, meta=None):
        if meta is not None:
            if "api_key" in meta:
                self.api_key = meta["api_key"]
            if "config" in meta:
                self.config = meta["config"]
            if "local_path" in meta:
                self.local_path = meta["local_path"]
        self.lighthouse_test(self.config)

    def lighthouse_test(self, config, **kwargs):

        return False
    
    def lighthouse_push(self, pin, **kwargs):
        config = self.config
        return False
    
    def lighthouse_pull(self, pin, **kwargs):
        config = self.config
        return False