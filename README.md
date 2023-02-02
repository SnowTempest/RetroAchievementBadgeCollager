# RetroAchievement Badge Collager
RetroAchievements Badge Scraper. Scrapes the given game ID for its badges and automatically collages them with the given number of columns.

# Usage
You enter in a valid game ID from the site. 

Example : 

If you enter 985 you will be given the badges for https://retroachievements.org/game/985.
In this case. The game is Kirby's Avalanche | Kirby's Ghost Trap.
Once correct ID is confirmed the badges are downloaded from the site.
Then you are asked for how many achievements you want per line.
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

# Notes:
The program must be in an empty folder to ensure safe deletion of images. The program deletes every image from the folder other than the resulted collage. I am not responsible if you delete an important image by accident via this program's completion. You have been warned. This will be fixed eventually.
I also do not condone using this tool to use the badges for purposes other than collaging them and using them on RetroAchievement's Discord.



