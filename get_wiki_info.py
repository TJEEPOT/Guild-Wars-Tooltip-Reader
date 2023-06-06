# !/usr/bin/env python
# -*- coding: utf-8 -*-
""" Takes a given item and looks certain information about it up on the wiki.
Project : Guild-Wars-Tooltip-Reader
File    : get_wiki_info.py
Date    : Sunday 28 May 2023
History : 2023/05/28 - v0.1 - Create project file
"""

__author__     = "Martin Siddons"
__email__      = "tjeepot@gmail.com"
__status__     = "Prototype"  # "Development" "Prototype" "Production"

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup
import re

def transform_tooltip_to_wiki_name(text) -> str:
    item_name = text.partition("\n")[0]  # Extract the first line of the tooltip text
    return format_item_to_wiki_name(item_name)

def format_item_to_wiki_name(item_name):
    # Remove numbers from the beginning of the first line if they exist
    new_item_name = re.sub(r"(.*\d)\s*", "", item_name)

    # Remove 's' characters from the end of each word if a number was found
    if item_name != new_item_name:
        words = new_item_name.split()
        processed_words = [re.sub(r"(s)\b", "", word) for word in words]
        item_name = " ".join(processed_words)

    wiki_name = item_name.replace(" ", "_") # Adjust the item name to be in line with what's expected for the wiki
    return wiki_name


def get_requested_page(pagename) -> list[dict[str:str, str:str]]:
    """Takes the name of a wiki page (e.g. Great_Axe) and returns a list of dicts, where each dict has the fields "page_name" and "response". This function correctly handles disambiguation pages by searching and returning the details of every page linked on the disambiguation page, within that list."""

    url = f"https://wiki.guildwars.com/wiki/{pagename}"
    headers = {"User-Agent": "Guild-Wars-Tooltip-Reader", # good practice to remain contactable with web admins
                     "From": "https://github.com/TJEEPOT/Guild-Wars-Tooltip-Reader"}

    response = requests.get(url, headers=headers, timeout=10)

    # Check if the page returned anything other than status code 200.
    if response.status_code != 200:
        raise ValueError("Page does not exist or could not be contacted.")
    
    # Check if the page is a disambiguation page
    disambiguation_pages = check_for_disambiguation(response)
    if disambiguation_pages is not None:
        responses = []
        # If it was, check all the returned pages in turn and return them all as a list
        for disamb_page in disambiguation_pages:
            requested_page = get_requested_page(disamb_page)[0] # function returns a list, so remove the only element
            responses.append({"page_name":disamb_page, "response":requested_page["response"]})
        return responses
    else:
        return [{"page_name":pagename, "response":response}]

def check_for_disambiguation(response):
    if 'disambiguation' in response.text.lower():
        # Tell the user what the pages are.
        soup = BeautifulSoup(response.text, 'html.parser')

        item_names = soup.find_all('div', class_="gallerytext")
        print("Disambiguation page found. Items are as follows:")
        page_names = []
        for item in item_names:
            item_name = item.text.replace("\n", "")
            page_names.append(item_name)
        print(page_names)

        # Transform the names into wiki page names and return them
        processed_names = [format_item_to_wiki_name(name) for name in page_names]
        return processed_names
    return None

def get_materials_from_page(page) -> dict[list[dict]]:
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find the table containing the desired information
    table = soup.find('tbody')

    # Find the rows (<tr>) in the table
    rows = table.find_all('tr')

    # Find the common and rare crafting materials:
    materials = []
    for row in rows:
        if "common salvage" in row.text.lower():
            materials.extend(_get_materials(row, "common"))
        elif "rare salvage" in row.text.lower():
            materials.extend(_get_materials(row, "rare"))

    return {"materials": materials}

def _get_materials(row, material_type) -> list[dict]:
    materials = []
    item = row.find_next('td')
    if item:
        mats = item.find_all('a')
        for mat in mats:
            if (mat.text != None) and (mat.text != "") and (mat.text != " "):
                count = 0 # TODO: grab the average count from the page around here.
                materials.append({"item_name":mat.text, "type":material_type, "average_count":count}) # Get the text content of the <a> tag
    return materials

if __name__ == "__main__":
    pages = get_requested_page("Great_Axe")[0] # Great_Axe / Water_Staff
    materials = get_materials_from_page([page for page in pages])
    print(materials)