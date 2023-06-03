# !/usr/bin/env python
# -*- coding: utf-8 -*-
""" Handles the caching of data into and out of the in-memory-db
Project : Guild-Wars-Tooltip-Reader
File    : db_cache.py
Date    : Sunday 04 June 2023
History : 2023/06/04 - v0.1 - Create project file
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

import sqlite3

def connect_to_db():
    return sqlite3.connect(':memory:')

def create_initial_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE disambiguation (disamb_page_name TEXT, target_page TEXT)""")
    cursor.execute("""INSERT INTO employees VALUES (1, "John Doe", 30)""")
    conn.commit()


if __name__ == "__main__":
    pass