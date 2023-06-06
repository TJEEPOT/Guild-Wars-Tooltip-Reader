# What It Does #
This project returns information on items within the MMORPG Guild Wars (2005). 

# What I Learned #
How to integrate image recognition, edge-detection and OCR into a project. It was also another chance to check my ability to scrape web pages, as well as try out basic information caching.

# Usage Notes #
This script is written in Python 3, therefore I recommend installing the latest version of
 [Python](https://www.python.org/downloads/) to run it. Once installed, do the following:
 - Open a Terminal / Command Line / Powershell prompt in the folder the script is in and type ```python3 -m venv .venv``` to build a virtual environment for the scripts to run in. 
 - Activate the virtual environment with ```.\.venv\Scripts\activate.bat``` in Windows Command Line, ```.\.venv\Scripts\activate.ps1``` in Windows Powershell or ```source \.venv\Scripts\activate``` on Linux or Mac.
 - Load the required libraries with ```pip install -r requirements.txt```.
 - type ```python3 start.py``` to run the program. 
 
 Alternatively, you can follow the above steps then run the program using ```start.bat``` or ```start.ps1``` in Windows (though this feature lacks font colours.)

 Once running, tab into the game, hover over an item and press F5. The script will analyse the item and provide you with information from the wiki - generally the result from salvaging that item. To stop the script, press F6. 
 
 This is configured to work only for English copies of the game - this may be able to be changed by modifying the ```lang``` parameter passed into ```pytesseract.image_to_string()``` in ```grab.py```, however this is untested.

 Debug mode can be enabled by setting ```debug = True``` within ```start.py``` and / or ```grab.py```.

# Additional Information #
Information on the structure of stored data can be found in ```/data/readme.md```.