__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "2.0"

import requests
import sys
import os
from bs4 import BeautifulSoup
import cv2
import numpy as np

#The Achievement Set
global SET

# Class RetroAchievementSet:
# param ID = Game ID of the Given Set
# param URL = The URL of the Given Set
# param BADGENUM = The number of Badges of the Given Set
# param BADGELIST = The list of Badges of the Given Set
# param LENGTH = The number of Badges to be shown on each Line
# param BADGENAMES = The list of individual bages used for deletion.
class RetroAchievementSet:
    
    def __init__ (self, ID, URL, BADGENUM, BADGELIST, LENGTH, BADGENAMES, SIZE):
        self.ID = ID
        self.URL = URL
        self.BADGENUM = BADGENUM
        self.BADGELIST = BADGELIST
        self.LENGTH = LENGTH
        self.BADGENAMES = BADGENAMES
        self.SIZE = SIZE

# Function getUrl()
# Asks the user for the Game ID they want badges from and creates the given URL to the Set.
# The URL is then stored in the class to be used in the next function getImageLink()
def getURL():
    global SET

    id = input("What is the Game ID of the Game you want to get Badges from:\n")

    url = "https://retroachievements.org/game/"  + id
    SET = RetroAchievementSet(id, url, 0, [], 0, [], 64)
    getImageLink()

# Function getImageLink()
# Asks the user to confirm the given Game ID. Closes if Incorrect ID.
# Searches the Game ID for all badge URLS and stores them into BADGELIST.
# The function then calls the removeLocks() function.
# Afterwards the function then calls downloadBadges().
def getImageLink():
    request = requests.get(SET.URL)
    soup = BeautifulSoup(request.text, 'html.parser')

    while True:
        print("\nGame ID Correlates to: " + soup.title.text.replace(" · RetroAchievements", ""))
        choice = input("Continue: 1 - Yes, 0 - No\n")

        if choice == "1" or choice == "0": break
        else: print("ERROR: Invalid Input. Try again.\n")

    if choice == "0":
        print("Program will exit.")
        exit()

    images = soup.find_all('img')
    
    for image in images:
        if "https://media.retroachievements.org/Badge/" in image['src']:
            SET.BADGELIST.append(image['src'])

    removeLocks()
    downloadBadges()

# Function removeLocks()
# This function iterates through the list of badges and removes any locks on the badge URLS (If Any).
# This allows the program to get the "Unlocked" version of the badges which are in color.
# The new URL then replaces the current URL of the badge and the list is returned back to getImageLink().
def removeLocks():
    for badge in SET.BADGELIST:
        cur = SET.BADGELIST.index(badge)
        badge = badge.replace("_lock", "")
        SET.BADGELIST[cur] = badge

    return SET.BADGELIST

# Function downloadBadges()
# This function downloads all the badges from the list. 
# Closes program if the list is empty.

def downloadBadges():

    changeDirectory()

    if(len(SET.BADGELIST) == 0):
        print("No badges found for Current Game ID. Program will close.")
        exit()

    print("\nDownloading Badges....\n")

    for badge in SET.BADGELIST:

        badgeName = str(SET.BADGENUM + 1) + "_" + SET.ID + ".png"

        with open(badgeName, 'wb') as f:
            im = requests.get(badge).content
            f.write(im)
        
        SET.BADGENAMES.append(badgeName)
        SET.BADGENUM = SET.BADGENUM + 1

    print("Download Complete.\n")

    getCollage()

# Function getCollage()
# The main collage creation function.
# Calls createHorizontals() first with the given collection of images to create the rows.
# Calls combineHorizontals() afterwards to combine the rows together.
#
def getCollage():
    imageCollection = []

    while True:
        print("\nWould you like the images have padding to make them easier to see?")
        choice = input("Continue: 1 - Yes, 0 - No\n")

        if choice == "1" or choice == "0": break
        else: print("ERROR: Invalid Input. Try again.\n")


    for i in range(SET.BADGENUM):
        image = cv2.imread(f'{i + 1}_' + SET.ID + '.png')
        if choice == "1":
            SET.SIZE = 66
            image = cv2.copyMakeBorder(image, 1,1,1,1, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        image = cv2.resize(image, (SET.SIZE,SET.SIZE))
        imageCollection.append(image)

    while True:
        SET.LENGTH = int(input("\nHow many badges/cheevos do you want per line: "))
        
        if SET.LENGTH <= SET.BADGENUM:
            break
        else:
           print("ERROR: Cannot have number of columns greater than the number of badges.\n")

    horizontals = createHorizontals(imageCollection)
    vertical = combineHorizontals(horizontals)

    while True:
        print("\nWould you like to delete the individual badge icons you downloaded?")
        choice = input("Continue: 1 - Yes, 0 - No\n")

        if choice == "1" or choice == "0": break
        else: print("ERROR: Invalid Input. Try again.\n")

    if int(choice): removeBadges()
    cv2.imwrite("OLD.png", vertical)

# Function changeDirectory()
# Changes the current working directory to be where the executable is located.
# The script directory only matters for my end.
def changeDirectory():

    if sys.argv[0].endswith('.exe'):
        dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(dir)


# Function createHorizontals()
# Creates each of the rows and stores them in the collection of images.
# Once horizontals are created the list is returned to getCollage().
def createHorizontals(collection):
    paddedImage = 255 * np.ones(shape=[SET.SIZE, SET.SIZE, 3], dtype=np.uint8)
    newHorizontals = []
    curHori = collection[0]

    for cur in range(1, SET.BADGENUM):
        if cur % SET.LENGTH != 0:
            curHori = np.hstack([curHori, collection[cur]])
        else:
            newHorizontals.append(curHori)
            curHori = collection[cur]

    if SET.BADGENUM % SET.LENGTH != 0:
        for i in range(SET.BADGENUM % SET.LENGTH, SET.LENGTH):
            curHori = np.hstack([curHori, paddedImage])

    newHorizontals.append(curHori)

    return newHorizontals

# Function combineHorizontals()
# Combines the horizontals together to create the final collage.
# Returns the result to getCollage()
def combineHorizontals(horizontals):
    if len(horizontals) == 1:
        return horizontals[0]
    elif len(horizontals) == 2:
        return np.vstack([horizontals[0], horizontals[1]])
    else:
        curHori = None
        for index, horizontal in enumerate(horizontals):
            if index == 0:
                curHori = horizontals[0]
            else: 
                curHori = np.vstack([curHori, horizontal])

    return curHori

# Function removeBadges()
# This function removes the individually downloaded badges from the directory. 
# The function compares the badgesNames to those listed in the SET object and removes them.
# If the file directory is missing badgeNames an error may have occurred.
def removeBadges():
    filelist = [ f for f in os.listdir(os.getcwd()) if f in SET.BADGENAMES ]
    for f in filelist:
        if os.path.isfile(f):
            os.remove(f)
            SET.BADGENAMES.remove(f)
        else:
            print("Error: %s file not found" % f)
    
    if len(SET.BADGENAMES) == 0: print("\nImages Deleted Successfully!\n")
    else: print("Some of the files may have not been deleted correctly. Please check the directory for any anomalies.")

#The main function of the Program. Calls getURL() and prints the resulting file of the Collage.
def main():
    getURL()
    print("Collage has been saved at: " + os.path.dirname(__file__) + " called OLD.png.")
    input("Process Complete! Press any key to close...\n")

main()



