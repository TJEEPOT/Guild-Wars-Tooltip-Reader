# What It Does #
This project returns information on items within the MMORPG Guild Wars (2005). 

# What I Learned #
How to integrate image recognition, edge-detection and OCR into a project. It was also another chance to check my ability to scrape web pages, as well as try out basic information caching.

# Usage Notes #
This script is written in Python 3, therefore I recommend installing the latest version of
 [Python](https://www.python.org/downloads/) to run it. Open a terminal / Powershell prompt in the
  folder the script is in and type ```python start.py``` to run. Alternatively, you can start the program via start.bat in Windows (though this feature lacks font colours.)
  Once running, tab into the game, hover over an item and press F5. The script will analyse the item and provide you with information from the wiki - generally the result from salvaging that item. To stop the script, press F6. Debug mode can be enabled by setting ```debug = True``` within ```start.py``` and / or ```grab.py```. This is configured to work only for English copies of the game - this may be able to be changed by modifying the ```lang``` parameter passed into ```pytesseract.image_to_string()``` in ```grab.py```, however this is untested.