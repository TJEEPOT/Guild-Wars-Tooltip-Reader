# !/usr/bin/env python
# -*- coding: utf-8 -*-
""" Wrapper to perform a single lookup
Project : Guild-Wars-Tooltip-Reader
File    : start.py
Date    : Sunday 28 May 2023
History : 2023/05/28 - v0.1 - Create project file
"""

__author__     = "Martin Siddons"
__email__      = "tjeepot@gmail.com"
__status__     = "Prototype"  # "Development" "Prototype" "Production"

import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import grab
import get_wiki_info as wiki_lookup
import transfer_data
import queue
import threading
from colorama import Fore, Back, Style

from pynput import keyboard

def run_process(screenshot):
    # Process the screenshot to extract the tooltip
    if debug:
        print("Performing crop on screenshot")
    try:
        tooltip_image = grab.get_tooltip(screenshot)
    except ValueError as e:
        print(f"{e} Try again.")
        return None
    
    # Process the tooltip image to extract the item name
    if debug:
        print("Performing OCR on screenshot.")    
    tooltip_text = grab.perform_ocr(tooltip_image) # add tesserect install location as parameter, if it's non-standard
    item_name = wiki_lookup.transform_tooltip_to_wiki_name(tooltip_text)

    # Check if the item is in the materials dict (If so, treat it as a material).
    print(f"item name: {item_name}")
    print(f"material: {materials_dict.get('item_name')}")
    if item_name in materials_dict:
        if debug:
            print("Found item in materials dict.")
        material = materials_dict.get(item_name)
        display_material(item_name, material)

    # Check if the item exists in the disambiguation dict
    elif item_name in disambiguation_dict:
        # If it does exist, get the data from the salvage dict
        if debug:
            print("Found item details in disambiguation list.")
        for disambiguated_item in disambiguation_dict[item_name]:
            materials = salvage_dict.get(item_name).get("materials")
            display_results(disambiguated_item, materials) ###
                
    # Check if the item exists in the salvage dict
    elif item_name in salvage_dict:
        if debug:
            print("Found item details in salvage list.")
        materials = salvage_dict.get(item_name).get("materials")
        display_results(item_name, materials)

    else:
        # Look up the item on the Guild Wars Wiki
        if debug:
            print(f"\"{item_name}\" found, checking wiki...")
        try:
            pages = wiki_lookup.get_requested_page(item_name) # returns a list of dicts
        except ValueError as e:
            print(f"Issue with page \"{item_name}\": {e} Try again later.")
            return
        
        # Check if we found a disambiguation page. If so, record the names to the disambiguation dict.
        if len(pages) > 1:
            all_page_names = []
            for page_dict in pages:
                all_page_names.append(page_dict.get("page_name"))
            disambiguation_dict[item_name] = all_page_names
        
        for page in pages:
            materials = wiki_lookup.get_materials_from_page(page["response"])

            # Save the results into the salvage dict
            if debug:
                print("Adding item to salvage list.")
            salvage_dict[page["page_name"]] = materials

            # Display the results (break the "materials" dict out of the variable)
            display_results(page["page_name"], materials["materials"])
    
def display_results(item_name:str, materials:list[dict]):
    display_name = item_name.replace("_", " ")
    print(display_name + Fore.CYAN + " Common materials: " + Style.RESET_ALL, end="") 
    print(*(f"{mat.get('average_count')} {mat.get('item_name')}" for mat in materials if mat.get("type") == "common"), sep=" or ", end=". ")
    print(Fore.MAGENTA + "Rare materials: " + Style.RESET_ALL, end="")
    print(*(f"{mat.get('average_count')} {mat.get('item_name')}" for mat in materials if mat.get("type") == "rare"), sep=" or ")

def display_material(item_name:str, material:dict):
    display_name = item_name.replace("_", " ")
    print(Back.WHITE + Fore.BLACK + display_name, end=" ")
    print("(Common)." if material.get("type") == "common" else Fore.BLUE + "(Rare)." + Fore.BLACK if material.get("type") == "Rare" else "(N/A).", end=" ")
    print(f"Last recorded prices: Buy: {material.get('buy')}G, Sell: {material.get('sell')}G." + Style.RESET_ALL)

def on_key_press(key):
    if key == keyboard.Key.f6:
        # Save the data collected to disk.
        transfer_data.to_json(disambiguation_dict, "data\disambiguation.json", debug)
        transfer_data.to_json(salvage_dict, "data\salvage.json", debug)
        transfer_data.to_json(materials_dict, "data\material.json", debug)

        exit_event.set()
        request_queue.put(False) # Screenshot processor blocks on checking an empty list, so we push this to trigger the exit
        if debug:
            print("Exit event set")
        listener.stop()
        if debug:
            print("Listener Stopped")
        queue_processor.join()
        if debug:
            print("Screenshot Processor thread joined. Exit event complete.")
        exit()
    
    if key == keyboard.Key.f5:
        # Get the item name from in-game
        screenshot = grab.take_screenshot()
        print("Captured screenshot.")
        request_queue.put(screenshot)

def screenshot_processor(queue):
    while not exit_event.is_set():
        screenshot = queue.get()
        if screenshot is False:
            break
        else:
            if debug:
                print(f'Processing captured screenshot')
            run_process(screenshot)

############################################################
# Enable debug to get additional test messages.
debug = False
# Create a queue to store the requests
request_queue = queue.Queue()

# Create an event to signal the threads to exit
exit_event = threading.Event()

# Load the dicts of previously found disambiguation pages, salvages and materials:
disambiguation_dict = transfer_data.from_json("data\disambiguation.json")
salvage_dict =        transfer_data.from_json("data\salvage.json")
materials_dict =      transfer_data.from_json("data\material.json")

# Start listening for the "F5" or "F6" key press
listener = keyboard.Listener(on_press=on_key_press)
listener.start()

print('\033[94m'+"Press F5 to capture the tooltip, F6 to Exit."+'\033[0m')

# Create and start a thread to process the requests
queue_processor = threading.Thread(target=screenshot_processor, args=(request_queue,))
queue_processor.start()

while not exit_event.is_set():
    pass
############################################################