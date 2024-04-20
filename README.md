# Scaling Ethereum Hackathon Presents
IPFS Huggingface Bridge:

for huggingface datasets python library visit:
https://github.com/endomorphosis/ipfs_datasets

for huggingface transformers python library visit:
https://github.com/endomorphosis/ipfs_transformers

for transformers.js visit:
https://github.com/endomorphosis/ipfs_transformers_js

for orbitdbkit nodejs library visit:
https://github.com/endomorphosis/orbitdb-benchmark/

for python model manager library visit: 
https://github.com/endomorphosis/ipfs_model_manager/

for nodejs model manager library visit: 
https://github.com/endomorphosis/ipfs_model_manager_js/

for nodejs ipfs huggingface scraper with pinning services visit:
https://github.com/endomorphosis/ipfs_huggingface_scraper/


Author - Benjamin Barber
QA - Kevin De Haan

# About

This is a model manager and wrapper for huggingface, looks up a index of models from an collection of models, and will download a model from either https/s3/ipfs, depending on which source is the fastest.

# How to use
~~~shell
pip install .
~~~

look run ``python3 example.py`` for examples of usage.

this is designed to be a drop in replacement, which requires only 2 lines to be changed

In your python script
~~~shell
import datasets
from datasets import load_dataset
from datasets import FaissIndex
from transformers import AutoModel
from ipfs_transformers import AutoModel
from datasets import load_dataset
from ipfs_datasets import ipfs_load_dataset
from ipfs_datasets import auto_download_dataset
from ipfs_faiss import IpfsFaissDataset

model = AutoModel.from_auto_download("bge-small-en-v1.5")
dataset = auto_download_dataset('Caselaw_Access_Project_JSON')
knnindex = auto_download_faiss_index('Caselaw_Access_Project_FAISS_index')
index = FaissIndex(dimension=512)
embeddings = dataset['embeddings']
query = "What is the capital of France?"
query_vector = model.encode(query)
scores, neighbors = index.search(query_vectors, k=10)
~~~

or 

~~~shell
import datasets
from datasets import load_dataset
from datasets import FaissIndex
from transformers import AutoModel
from ipfs_transformers import AutoModel
from datasets import load_dataset
from ipfs_datasets import ipfs_load_dataset
from ipfs_datasets import auto_download_dataset
from ipfs_faiss import IpfsFaissDataset

model = AutoModel.from_ipfs("QmccfbkWLYs9K3yucc6b3eSt8s8fKcyRRt24e3CDaeRhM1")
dataset = ipfs_download_dataset('QmccfbkWLYs9K3yucc6b3eSt8s8fKcyRRt24e3CDaeRhM1')
knnindex = ipfs_download_faiss_index('QmccfbkWLYs9K3yucc6b3eSt8s8fKcyRRt24e3CDaeRhM1')
index = FaissIndex(dimension=512)
embeddings = dataset['embeddings']
query = "What is the capital of France?"
query_vector = model.encode(query)
scores, neighbors = index.search(query_vectors, k=10)
~~~

or to use with with s3 caching 
~~~shell
import datasets
from datasets import load_dataset
from datasets import FaissIndex
from transformers import AutoModel
from ipfs_transformers import AutoModel
from datasets import load_dataset
from ipfs_datasets import ipfs_load_dataset
from ipfs_datasets import auto_download_dataset
from ipfs_faiss import IpfsFaissDataset
s3cfg = {
        "bucket": "cloud",
        "endpoint": "https://storage.googleapis.com",
        "secret_key": "",
        "access_key": ""
    }

model = AutoModel.from_auto_download(
    "bge-small-en-v1.5",
    s3cfg=s3cfg
)
dataset = load_dataset.from_auto_download(
    dataset_name="Caselaw_Access_Project_JSON",
    s3cfg=s3cfg
)
knnindex = ipfs_download_faiss_index.from_auto_download(
    dataset_name="Caselaw_Access_Project_FAISS_index",
    s3cfg=s3cfg
)
index = FaissIndex(dimension=512)
embeddings = dataset['embeddings']
query = "What is the capital of France?"
query_vector = model.encode(query)
scores, neighbors = index.search(query_vectors, k=10)

~~~