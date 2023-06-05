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
import queue
import threading
import pickle

from pynput import keyboard

def run_process(screenshot):
    # Process the screenshot to extract the tooltip
    
    try:
        tooltip_image = grab.get_tooltip(screenshot)
    except ValueError as e:
        print(f"{e} Try again.")
        return None
    
    if debug:
        print("Got tooltip. Performing crop and OCR...")

    # Process the tooltip to extract the item name
    text = grab.perform_ocr(tooltip_image) # add your tesserect install location as parameter, if it's non-standard
    item_name = wiki_lookup.transform_tooltip_to_wiki_name(text)

    # Check if the item exists in the disambiguation dict
    if item_name in disambiguation_dict:
        # If it does exist, get the data from the salvage dict
        if debug:
            print("Found item details in disambiguation list.")
        for disambiguated_item in disambiguation_dict[item_name]:
            [common_mats, rare_mats] = salvage_dict.get(disambiguated_item)
            display_results(disambiguated_item, common_mats, rare_mats)
                
    # Check if the item exists in the salvage dict
    elif item_name in salvage_dict:
        if debug:
            print("Found item details in salvage list.")
        [common_mats, rare_mats] = salvage_dict.get(item_name)
        display_results(item_name, common_mats, rare_mats)

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
                # Ensure the page name is in the correct format
                corrected_name = wiki_lookup.format_item_to_wiki_name(page_dict["page_name"])
                all_page_names.append(corrected_name)
            disambiguation_dict[item_name] = all_page_names
        
        for page in pages:
            common_mats, rare_mats = wiki_lookup.get_materials_from_page(page["response"])

            # Save the results into the salvage dict
            if debug:
                print("Adding items to salvage list.")
            salvage_dict[page["page_name"]] = [common_mats, rare_mats]

            # Display the results
            display_results(page["page_name"], common_mats, rare_mats)
    
def display_results(item_name, common_mats, rare_mats):
    print(f"{item_name} " + "\033[96m" + "Common materials: " + "\033[00m", end="") 
    print([mat for mat in common_mats], end=". ")
    print("\033[95m" + "Rare materials: " + "\033[00m", end="")
    print([mat for mat in rare_mats])

def on_key_press(key):
    if key == keyboard.Key.f6:
        # Save the disambiguation dict
        if debug:
            print("Saving disambiguation dict.")
        save_dict(disambiguation_dict, "saved_disambiguation_pages.pkl")

        # Save the salvage dict
        if debug:
            print("Saving salvages dict.")
        save_dict(salvage_dict, "saved_salvages.pkl")

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
        print("Got screenshot.")
        request_queue.put(screenshot)

def screenshot_processor(queue):
    while not exit_event.is_set():
        screenshot = queue.get()
        if screenshot is False:
            break
        else:
            if debug:
                print(f'Processing Screenshot')
            run_process(screenshot)

def load_dict(filename):
    if not os.path.isfile(filename):
        return {"test":[["test"],["test"]]}
    
    with open(filename, 'rb') as file:
        loaded_dict = pickle.load(file)
    return loaded_dict

def save_dict(my_dict, filename):
    with open(filename, 'wb') as file:
        pickle.dump(my_dict, file)

############################################################
# Enable debug to get additional test messages.
debug = False

# Create a queue to store the requests
request_queue = queue.Queue()

# Create an event to signal the threads to exit
exit_event = threading.Event()

# Load the dict of previously found disambiguation pages
disambiguation_dict = load_dict("saved_disambiguation_pages.pkl")

# Load the dict of previous searches
salvage_dict = load_dict("saved_salvages.pkl")

# Start listening for the "F5" key press
listener = keyboard.Listener(on_press=on_key_press)
listener.start()

print('\033[94m'+"Press F5 to capture the tooltip, F6 to Exit."+'\033[0m')

# Create and start a thread to process the requests
queue_processor = threading.Thread(target=screenshot_processor, args=(request_queue,))
queue_processor.start()

while not exit_event.is_set():
    pass
############################################################