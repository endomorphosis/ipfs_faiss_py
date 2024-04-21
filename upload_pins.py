from pinning_apis import PinningApis
from pinata import pinata
from web3storage import web3storage
from filebase import filebase
from lighthouse import lighthouse

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

def filterFileByFolderPins(folder_names, pins):
    folders = {}
    for pin in pins:
        this_path = pin['path']
        found = False
        for folder_name in folder_names:
            if folder_name in this_path:
                if folder_name not in folders:
                    folders[folder_name] = []
                folders[folder_name].append(pin)
                found = True
                break
        if found == False:
            if 'other' not in folders:
                folders['other'] = []
            folders['other'].append(pin)
    return folders


def test():
    pin_chunks = ingest_pins('./ipfs_pins/')
    folder_pins = filterFolderPins(pin_chunks)
    folder_names = []
    for folder_pin in folder_pins:
        this_folder_pin = folder_pin
        path = this_folder_pin['path']
        folder_name = path.split('/')[-1]
        folder_names.append(folder_name)        
    file_pins = filterFilePins(pin_chunks)
    files_by_folder = filterFileByFolderPins(folder_names, file_pins)
    all_pins = []
    push_results = {}
    this_pinning_apis = PinningApis()
    for pin_list in pin_chunks:
        for pin in pin_list:
            pin_cid = None
            if "hash" in pin:
                pin_cid = pin['hash']
            else:
                print('No hash in pin')
                pin_cid = None
                
            path = pin['path']
            push_pin_results = this_pinning_apis.pin_push_one_every(
                pin_cid,
                path=path,
                file_by_folder_pins=files_by_folder,
                folder_pins=folder_pins,
                file_pins=file_pins
            )
            print(push_pin_results)
            push_results[pin_cid] = push_pin_results

    print("Push Results")
    print(len(push_results))
    with open('push_results.json', 'w') as f:
        json.dump(push_results, f)
    allpins = list(pin_chunks)
    folder_pins = list(folder_pins)
    file_pins = list(file_pins)
    print("File Pins")
    print(len(file_pins))
    print("Folder Pins")
    print(len(folder_pins))
    return folder_pins, file_pins, allpins

if __name__ == '__main__':
    test()