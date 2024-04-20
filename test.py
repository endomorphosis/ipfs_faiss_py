from datasets import *
from ipfs_faiss import *
from ipfs_faiss import ipfs_faiss_dataset
import ipfs_datasets
import ipfs_faiss
import datasets
import urllib3
import requests
import subprocess
import sys
import json
import os

def ingest_pins(filepath):
    pinlist = []
    thisdir = os.getcwd()
    filepath = os.path.join(thisdir, filepath)
    filepath = os.path.normpath(filepath)
    is_file = os.path.isfile(filepath)
    is_dir = os.path.isdir(filepath)
    if is_file == True:
        if filepath.endswith('.json'):
            with open(filepath) as f:
                data = json.load(f)
                pinlist.append(data)
        return
    elif is_dir == True:
        files_in_folder = os.listdir(filepath)
        for file in files_in_folder:
            if file.endswith('.json'):
                with open(os.path.join(filepath , file)) as f:
                    data = json.load(f)
                    pinlist.append(data)
    else:
        print('Filepath is not a file or directory')
        print('Filepath: ' + filepath)
        return

    return pinlist

def filterFolderPins(pins):
    return [pin for pin in pins if pin['path'].endswith("json") != True]

def filterFilePins(pins):
    return [pin for pin in pins if pin['path'].endswith("json") == True]

def test():
    pin_chunks = ingest_pins('./ipfs_pins/')
    all_pins = []
    for pin_list in pin_chunks:
        all_pins.extend(pin_list)

    for pin in all_pins:
        len_pin = len(pin.keys())
        if len_pin > 3:
            print(pin)
        if len_pin < 3:
            print(pin)
            del pin

    folderPins = filterFolderPins(all_pins)
    filePins = filterFilePins(all_pins)
    query = ipfs_faiss_dataset("Caselaw_Access_Project_FAISS_index",folderPins, filePins)
    
    return folderPins, filePins

if __name__ == '__main__':
    test()