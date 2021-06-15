# WikiScrapeGui
A GUI for scraping Wikipedia made with PySimpleGui.  
Note: This project is still a work in progress and many features are sure to be added. I'm also planning to release a .exe with PyInstaller every time the code has changed a significant amount.

# Usage
**Note: This has only been tested on Windows 10 with Python 3.9.2.**  
Download and extract the zip file of this repository.  
Type this into the command prompt to install the needed libraries:  
`pip install wikipedia pysimplegui`  
Run `wikiscrapegui.py`  
Enjoy!  

If you have any problems with using the program, please [open an issue.](https://github.com/TetrisKid48/WikiScrapeGui/issues)  

# Screenshots
**Screenshots might not always be perfectly up to date.**  
![image](https://user-images.githubusercontent.com/67118737/112740764-b19c5b00-8f4d-11eb-87c9-7919fd3b56bb.png)
![image](https://user-images.githubusercontent.com/67118737/112740772-c678ee80-8f4d-11eb-91d6-35cc2129cee0.png)
![image](https://user-images.githubusercontent.com/67118737/112740796-e6101700-8f4d-11eb-80b6-25299ae5a6ef.png)
![image](https://user-images.githubusercontent.com/67118737/112740804-f922e700-8f4d-11eb-9c2c-017dc6ff208a.png)

# More Information
In "one output file" mode, all scraped data will be saved to an output.txt file in the outputs folder in the same directory as the program. Scraping another page will overwrite the other text while in this mode.  
In "mutlifile" mode, a new text file will be made in the outputs folder each time data is scraped. The title will specify what is in the file, e.g. "Fish-content.txt" would be the content of the wikipedia page for fish.
User settings are saved to the settings.ini file.  
The default theme is Material1.  

### Planned features, sorted by priority:
Ability to scrape multi-page categories  
Compatibility with all special symbols in urls  
Menu to choose a page when a disambiguation error occurs  
Infobox scraping  
Better OSX/Linux support  
Big menu for scraping tons of pages in a category with tons of options  
Option to scrape the "Page Information" page of a wikipedia page  
Improved and/or animated logo  
