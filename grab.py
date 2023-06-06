# !/usr/bin/env python
# -*- coding: utf-8 -*-
""" Takes a screen grab of the screen area near the pointer
Project : Guild-Wars-Tooltip-Reader
File    : grab.py
Date    : Sunday 28 May 2023
History : 2023/05/28 - v0.1 - Create project file
"""

__author__     = "Martin Siddons"
__email__      = "tjeepot@gmail.com"
__status__     = "Prototype"  # "Development" "Prototype" "Production"

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pyautogui
import pytesseract
from PIL import Image
import cv2
import numpy as np

"""Finds the region where the tooltip might be and returns a PIL Image object of that region."""
def take_screenshot():
    mouse_x, mouse_y = pyautogui.position() # Get the mouse pointer position

    # Define the offset for the tooltip region
    max_width = 500  # Width of the tooltip region
    max_height = 200  # Height of the tooltip region
    offset_x = 6 # Offset in the x-axis (nudged right)
    offset_y = -6 - max_height # Offset in the y-axis (nudged up)

    # Calculate the coordinates for the tooltip region
    x = mouse_x + offset_x
    y = mouse_y + offset_y
    
    # Get the image
    image = pyautogui.screenshot(region=(x, y, max_width, max_height))
    if debug:
        save_image(image, "output\\raw_screenshot.png")
        print("Saved the raw screenshot as output\\raw_screenshot.png")
    return image

def get_tooltip(image:Image):
    # Convert the screenshot to a NumPy array
    screenshot_np = np.array(image)  

    # Convert the image to grayscale and run canny edge detection on it.
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 460, 560)

    # Find the contours of the tooltip region
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if debug:
        cv2.imwrite("output\\contours.png", edges)
        print("Saved contours as output\\contours.png")

    # Sort the contours based on their area
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    # Find the contour with the largest area within the expected minimum bounds
    tooltip_contour = None
    min_width = 50
    min_height = 30
    for contour in sorted_contours:
        x_, y_, w_, h_ = cv2.boundingRect(contour)
        if w_ >= min_width and h_ >= min_height:
            tooltip_contour = contour
            break

    # Get the bounding rectangle of the tooltip contour and crop the image slightly smaller than the border
    if tooltip_contour is not None:
        x, y, w, h = cv2.boundingRect(tooltip_contour)
        tooltip_image = image.crop((x+6, y+12, x-5 + w, y-5 + h))
    else:
        raise ValueError("Image doesn't appear to contain a tooltip.")

    if debug:
        save_image(tooltip_image, "output\\tooltip_image.png")
        print("Saved cropped tooltip image as output\\tooltip_image.png")
    return tooltip_image

def perform_ocr(image, tesserect_install_location=r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = tesserect_install_location
    text = pytesseract.image_to_string(image, lang="eng")

    if debug:
        save_text(text, "output\\tooltip.txt")
        print("Saved the OCR'd tooltip text as output\\tooltip.txt")
    return text

def save_text(text, filename):
    text = text.strip()
    with open(filename, 'w') as file:
        file.write(text)

""" Takes a PIL Image object and saves it to disk as a .png"""
def save_image(image, filename):
    image.save(filename,"PNG")

debug = False

if __name__ == "__main__":
    debug = True
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    print(pytesseract.get_languages(config=''))

    screenshot = take_screenshot()
    try:
        tooltip_image = get_tooltip(screenshot)
    except ValueError as e:
        print(f"Error: {e} Exiting.")
        exit(0)
    text = perform_ocr(tooltip_image) # add your tesserect install location as parameter, if it's non-standard
