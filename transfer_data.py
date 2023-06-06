# !/usr/bin/env python
# -*- coding: utf-8 -*-
""" Functions to load and save data to/from disk.
Project : Guild-Wars-Tooltip-Reader
File    : transfer_data.py
Date    : Monday 05 June 2023
History : 2023/06/05 - v0.1 - Create project file
"""

""" Copyright Martin Siddons - All Rights Reserved
    Unauthorized copying of this file, via any medium is strictly prohibited
    Proprietary and confidential
    Written by Martin Siddons <tjeepot@gmail.com>, June 2023
"""

__author__     = "Martin Siddons"
__email__      = "tjeepot@gmail.com"
__status__     = "Development"  # "Development" "Prototype" "Production"

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json

def from_json(filename):
    f = None
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print(f"\nError attempting to get file: \'{filename}\'.")
    data = json.load(f)
    f.close()
    return data

def to_json(data, filename, debug=False):
    try:
        # Rename the current file in case this screws up (and override the old .old file silently).
        os.replace(filename, f"{filename}.old")
        if debug:
            print(f"Copied existing file to {filename}.old")
    except FileNotFoundError:
        print("Existing file not found, moving on.")

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
        if debug:
            print(f"Written data to {filename}")

if __name__ == "__main__":
    pass