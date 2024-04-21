import datasets
from datasets import load_dataset
# from transformers import AutoModel
# from ipfs_transformers import AutoModel
# from ipfs_datasets import ipfs_load_dataset
# from ipfs_datasets import auto_download_dataset
from ipfs_faiss import IpfsFaissDataset
from datasets import *
from ipfs_faiss import *
from ipfs_faiss import IpfsFaissDataset
import datasets
import urllib3
import requests
import subprocess
import sys
import json
import os

def ingest_pins(filepath):
    thisdir = os.getcwd()
    filepath = os.path.join(thisdir, filepath)
    filepath = os.path.normpath(filepath)
    is_file = os.path.isfile(filepath)
    is_dir = os.path.isdir(filepath)
    if is_file == True:
        if filepath.endswith('.json'):
            with open(filepath) as f:
                data = json.load(f)
                yield data
        return
    elif is_dir == True:
        files_in_folder = os.listdir(filepath)
        for file in files_in_folder:
            if file.endswith('.json'):
                with open(os.path.join(filepath , file)) as f:
                    data = json.load(f)
                    yield data
    else:
        print('Filepath is not a file or directory')
        print('Filepath: ' + filepath)
        return

def filterFolderPins(pins):
    if type(pins) == dict:
        if pins['path'].endswith("json"):
            yield pins
    elif type(pins) == list:
        for pin in pins:
            if not pin['path'].endswith("json"):
                yield pin
    elif type(pins) == object:
        print('Object')
        print(dir(pins))

def filterFilePins(pins):
    if type(pins) == dict:
        if pins['path'].endswith("json"):
            yield pins
    elif type(pins) == list:
        for pin in pins:
            if pin['path'].endswith("json"):
                yield pin
    elif type(pins) == object:
        print('Object')
        print(dir(pins))


def test():
    pin_chunks = ingest_pins('./ipfs_pins/')
    folder_pins = filterFolderPins(pin_chunks)
    file_pins = filterFilePins(pin_chunks)
    all_pins = []
    
    allpins = list(pin_chunks)
    folder_pins = list(folder_pins)
    file_pins = list(file_pins)
    print("File Pins")
    print(len(file_pins))
    print("Folder Pins")
    print(len(folder_pins))

    # folder_pins = []
    # file_pins = []
    # for pin_list in ingest_pins('./ipfs_pins/'):
    #     for pin in pin_list:
    #         len_pin = len(pin.keys())
    #         if len_pin > 3:
    #             print(pin)
    #         elif len_pin < 3:
    #             print(pin)
    #             del pin
    #         else:
    #             all_pins.append(pin)
    #             folder_pins.append(filterFolderPins(pin))
    #             file_pins.append(filterFilePins(pin))
    # folderPins = filterFolderPins(all_pins)
    # filePins = filterFilePins(all_pins)
    faiss_dataset = datasets.load_dataset('/teraflopai/Caselaw_Access_Project_FAISS_index/')
    embeddings = datasets.load_dataset('/teraflopai/Caselaw_Access_Project_embeddings/')
    faiss_index = faiss_dataset.load_faiss_index('embeddings', 'my_index.faiss')
    #dataset = ipfs_faiss_dataset.auto_download('Caselaw_Access_Project_FAISS_index')
    merged_dataset = ipfs_faiss_dataset.join_ipfs_faiss(faiss_dataset, folderPins, filePins)
    embeddings = merged_dataset['embeddings']


    
    # model = AutoModel.from_auto_download("bge-small-en-v1.5")
    # dataset = auto_download_dataset('Caselaw_Access_Project_JSON')
    # knnindex = auto_download_faiss_index('Caselaw_Access_Project_FAISS_index')
    # index = FaissIndex(dimension=512)
    # embeddings = dataset['embeddings']
    # query = "What is the capital of France?"
    # query_vector = model.encode(query)
    # scores, neighbors = index.search(query_vectors, k=10)
    return folderPins, filePins

if __name__ == '__main__':
    test()