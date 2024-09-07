import datasets
import ipfs_datasets_py
from ..ipfs_embeddings_py import ipfs_embeddings_py

class test_ipfs_faiss:
    def __init__(self, resources, metadata):
        self.resources = resources
        self.metadata = metadata
        self.datasets = datasets
        self.ipfs_datasets_py = ipfs_datasets_py
        self.ipfs_embeddings_py = ipfs_embeddings_py
        return None
    
    def test_ipfs_faiss(self, dataset, faiss_index, elastic_index, join_column):
        self.dataset = datasets.load_dataset("laion/Wikipedia-X")
        self.faiss_index = datasets.load_faiss_index("laion/Wikipedia-M3")
        print(self.faiss_index.columns)
        self.elastic_index = datasets.load_elastic_index()
        self.faiss_index.get_nearest_examples
        return None
    
if __name__ == "__main__":
    test_ipfs_faiss = test_ipfs_faiss()
    try:
        test_ipfs_faiss.test_ipfs_faiss()
        print("test_ipfs_faiss passed")
    except:
        print("test_ipfs_faiss failed")
        exit(1)
    exit(0)