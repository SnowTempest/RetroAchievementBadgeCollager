# RetroAchievement Badge Collager
RetroAchievements Badge Scraper. Scrapes the given game ID for its badges and automatically collages them with the given number of columns.

# Usage
You enter in a valid game ID from the site. 

Example : 

If the user enters 985 they will be given the badges for https://retroachievements.org/game/985.
In this case. The game is Kirby's Avalanche | Kirby's Ghost Trap.
Once correct ID is confirmed the badges are downloaded from the site.
Once Downloads are complete the user is asked for how many badges they would like per line.
Afterwards the images are then collaged into one file and the downloaded images are deleted.

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
5. Once Closed the downloaded badges will be deleted and the user will be left with a collaged image called OLD.png.

# Notes:
The program must be in an empty folder to ensure safe deletion of images. Note: Only badge images will be deleted.



