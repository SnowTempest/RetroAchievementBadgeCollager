# RetroAchievement Badge Collager
RetroAchievements Badge Scraper. Scrapes the given game ID for its badges and automatically collages them with the given number of columns.

NEW **
Now has the ability to collage your own badges straight from your computer into a collage that can be used for the Icon-Gauntlet.

# Usage
The user chooses the mode they want to use:
Mode 1 is collaging a badge set from the Retroachievements site.
Mode 2 is collaging a badge set from the users computer.

## Mode 1
The user enters in a valid game ID from the site. 

Example : 
If the user enters 985 they will be given the badges for https://retroachievements.org/game/985.
In this case. The game is Kirby's Avalanche | Kirby's Ghost Trap.
Once correct ID is confirmed the badges are downloaded from the site.
Once Downloads are complete the user is asked if they would like the images to be padded or have an outline to help distinguish badges from eachother.
Then the user is asked how many achievements they would like to see on 1 line.
Afterwards the images are then collaged into one file and the the user confirms whether or not they would like the images downloaded to be deleted.

## Mode 2
The user is asked to select the badges from their computer.
The badges are automatically selected in alphabetical order and currently does not support manual select mode. Please number your achievements accordingly.
The user is then asked if they would like padding added to the collage.
Afterwards the user is lastly asked for the number of columns they would like per row.
The image is then collaged together into one file. 
Note: The badges will be untouched and you can safely be assured nothing will happen to them as no deletion goes on during this mode.

# Libraries
## Requests
Link - https://pypi.org/project/requests/
## OS
Link - https://docs.python.org/3/library/os.html
## BS4
Link - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
## CV2
Link - https://pypi.org/project/opencv-python/
## Numpy
Link - https://numpy.org/install/

# Usage

1. Download the Executable (RABadgeCollager.exe) from the Releases page.
2. Move the Executable into any empty Folder.
3. Double click and Execute the program.
4. Follow the prompts on the screen.
5. Once Closed the user will be left with a collaged image called OLD.png.

# Notes:
The program must be in an empty folder to ensure safe deletion of images. Note: Only badge images will be deleted.



