import os
import sys
import datasets
# import ipfs_datasets_py
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)
# from ipfs_embeddings_py import ipfs_embeddings_py
import ipfs_embeddings_py

class test_ipfs_faiss:
    def __init__(self, resources, metadata):
        self.resources = resources
        self.metadata = metadata
        self.datasets = datasets
        # self.ipfs_datasets_py = ipfs_datasets_py
        self.ipfs_embeddings_py = ipfs_embeddings_py.ipfs_embeddings_py(resources, metadata)
        return None
    
    def test_ipfs_faiss(self, dataset, faiss_index, elastic_index, join_column, test_query=None):
        self.ipfs_embeddings_py.add_https_endpoint("BAAI/bge-m3", "62.146.169.111:80/embed",1)
        self.ipfs_embeddings_py.add_https_endpoint("BAAI/bge-m3", "62.146.169.111:8080/embed",1)
        self.ipfs_embeddings_py.add_https_endpoint("BAAI/bge-m3", "62.146.168.111:8081/embed",1)
        if test_query is not None:
            self.test_query = [test_query]
            self.ipfs_embeddings_py.queue_index_knn([test_query])

        selected_endpoint = self.ipfs_embeddings_py.choose_endpoint()
        print(selected_endpoint)
        if (len(self.ipfs_embeddings_py.cid_queue) > 0):
            items_to_index = self.ipfs_embeddings_py.pop_index_knn(1)
        self.dataset = datasets.load_dataset(dataset)
        print(self.dataset)
        self.faiss_index = datasets.load_dataset(faiss_index)
        print(self.faiss_index)
        # self.elastic_index = datasets.load_dataset(elastic_index)
        # print(self.elastic_index)

        # if self.query is not None:
        #     self.ipfs_embeddings_py

        return None
    
if __name__ == "__main__":
    resources = None
    metadata = None
    dataset = "laion/Wikipedia-X"
    faiss_index = "laion/Wikipedia-M3"
    elastic_index = None
    join_column = "Version Control"
    query = "hello world"
    test_ipfs_faiss = test_ipfs_faiss(resources, metadata)
    try:
        test_ipfs_faiss.test_ipfs_faiss(dataset, faiss_index, elastic_index, join_column, query)
        print("test_ipfs_faiss passed")
    except Exception as e:
        print("test_ipfs_faiss failed")
        print(e)
        exit(1)
    exit(0)