__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "3.0"

import cv2
import os
import requests
import sys
from bs4 import BeautifulSoup
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilenames

#Global Set
global SET

# Class RetroAchievementSet:
# param ID = Game ID of the Given Set
# param URL = The URL of the Given Set
# param BADGENUM = The number of Badges of the Given Set
# param BADGELIST = The list of Badges of the Given Set
# param LENGTH = The number of Badges to be shown on each Line
# param BADGENAMES = The list of individual bages used for deletion.
class RetroAchievementSet:
    
    def __init__ (self, ID, URL, BADGENUM, BADGELIST, LENGTH, BADGENAMES, SIZE, MODE):
        self.ID = ID
        self.URL = URL
        self.BADGENUM = BADGENUM
        self.BADGELIST = BADGELIST
        self.LENGTH = LENGTH
        self.BADGENAMES = BADGENAMES
        self.SIZE = SIZE
        self.MODE = MODE


# Function globalSet()
# Constructor for the global. Used to easily clear out the value and make it more re-usable.
# param id = id for the Game Set | NA if for Mode 2
# param url = url for the Game Set | NA if for Mode 2
# param mode = mode for the given program. 1 is Collaging Site Badges. 2 is Collaging New Badges from PC.
def globalSet(id, url, mode):
    global SET
    SET = RetroAchievementSet(id, url, 0, [], 0, [], 64, mode)

# Function start()
# Main Menu of the Program. Asks the user what they would like to use the program for.
# Enters either getURL() for old badges or getIcons() for new badges.
def start():
    print("********************************************************************************")
    print("\nRABADGECOLLAGER: Created By SnowTempest(AdeptTempest on Retroachievements.org)\n")
    print("********************************************************************************")
    question = "\nPlease Choose a Mode To Start:\n" + "1. Collage Old Badges From Site\n" + "2. Collage New Badges From PC\n"

    mode = inputHandler(question)

    while mode not in (1, 2):
        printError("Invalid Input, Please Try Again.", False)
        mode = inputHandler(question)

    if mode == 1: retrieveURL()
    else: retrieveBadges()

# Function retrieveURL()
# Asks the user for the Game ID they want badges from and creates the given URL to the Set.
# The URL is then stored in the class to be used in the next function storeImageLinks()
def retrieveURL():
    id = input("\nWhat is the Game ID of the Game you want to get Badges from:\n")
    url = "https://retroachievements.org/game/"  + id
    globalSet(id, url, mode=1)
    storeImageLinks()

# Function retrieveBadges()
# Asks the user to select their badges from the file explorer.
# Each image has their size checked and is appended to the SET.BADGELIST
# Images with invalid sizes will be removed and given an appropiate error.
def retrieveBadges():
    badgeSize = 64
    globalSet("NA", "NA", mode=2)

    root = tk.Tk()
    root.withdraw()

    print("\nPlease Select Your Badges:")
    files = askopenfilenames(title="Select Badges",filetypes=(("PNG files", "*.png"),))
    
    for file in files:
        image = cv2.imread(file)
        width, height = image.shape[:2]

        if (width == badgeSize and height == badgeSize) :
            print("Selected Icon: ", file)
            SET.BADGELIST.append(file)
            SET.BADGENUM = SET.BADGENUM + 1
        else: 
            print("Selected Icon: ", file + " Error: Does Not Meet Size Requirements (64 x 64).")
    
    if(len(SET.BADGELIST) == 0):
        printError("No Valid Badges Listed. Program will Exit.", True)
    
    collage()

# Function storeImageLinks()
# Asks the user to confirm the given Game ID. Closes if Incorrect ID.
# Searches the Game ID for all badge URLS and stores them into BADGELIST.
# The function then calls the removeLocks() function.
# Afterwards the function then calls downloadBadges().
def storeImageLinks():
    request = requests.get(SET.URL)
    soup = BeautifulSoup(request.text, 'html.parser')
    question = "\nGame ID Correlates to: " + soup.title.text.replace(" · RetroAchievements", "") + "\nContinue: 1 - Yes, 0 - No\n"

    choice = inputHandler(question)

    while choice not in (0,1):
        printError("Invalid Input. Try Again.\n", False)
        choice = inputHandler(question)

    if choice == 0: printError("Program will Exit.", True)

    images = soup.find_all('img')
    
    for image in images:
        if "https://media.retroachievements.org/Badge/" in image['src']:
            SET.BADGELIST.append(image['src'])

    removeLocks()
    downloadBadges()

# Function removeLocks()
# This function iterates through the list of badges and removes any locks on the badge URLS (If Any).
# This allows the program to get the "Unlocked" version of the badges which are in color.
# The new URL then replaces the current URL of the badge and the list is returned back to storeImageLinks().
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
        printError("No badges found for Current Game ID. Program will close.", True)

    print("\nDownloading Badges....\n")

    for badge in SET.BADGELIST:

        badgeName = str(SET.BADGENUM + 1) + "_" + SET.ID + ".png"

        with open(badgeName, 'wb') as f:
            im = requests.get(badge).content
            f.write(im)
        
        SET.BADGENAMES.append(badgeName)
        SET.BADGENUM = SET.BADGENUM + 1

    print("Download Complete.\n")

    collage()

# Function collage()
# The main collage creation function.
# Calls createHorizontals() first with the given collection of images to create the rows.
# Calls combineHorizontals() afterwards to combine the rows together.
def collage():
    imageCollection = []
    question = "\nWould you like the images have padding to make them easier to see?" + "\nContinue: 1 - Yes, 0 - No\n"
    choice = inputHandler(question)

    while choice not in (0,1):
        printError("Invalid Input, Please Try Again.", False)
        choice = inputHandler(question)

    for i in range(SET.BADGENUM):
        if SET.MODE == 1:
            image = cv2.imread(f'{i + 1}_' + SET.ID + '.png')
        else:
            image = cv2.imread(SET.BADGELIST[i])
        if choice == 1:
            SET.SIZE = 66
            image = cv2.copyMakeBorder(image, 1,1,1,1, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        image = cv2.resize(image, (SET.SIZE,SET.SIZE))
        imageCollection.append(image)
    
    setColumns()
    horizontals = createHorizontals(imageCollection)
    vertical = combineHorizontals(horizontals)

    if SET.MODE == 1:
        removeBadges()
        cv2.imwrite("OLD.png", vertical)
        final = "OLD.png"
    else:
        cv2.imwrite("NEW.png", vertical)
        final = "NEW.png"

    print("\nCollage has been saved at: " + os.path.dirname(__file__) + " called", final)


# Function setColumns()
# This function asks the user for the number of columns they want per row.
# Forces re-input until number given is either not 0 or not greater than the number of badges available.
def setColumns():
    question = "\nHow many badges/cheevos do you want per line: \n"
    SET.LENGTH = inputHandler(question)

    while SET.LENGTH == 0 or SET.LENGTH > SET.BADGENUM:
        printError("Number of Columns can not be 0 and Number of Columns can not be greater than the number of Badges.\n", False)
        SET.LENGTH = inputHandler(question)

# Function createHorizontals()
# param collection = The current collection of images to be used for creating the rows.
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

# Function changeDirectory()
# Changes the current working directory to be where the executable is located.
# The script directory only matters for my end.
def changeDirectory():
    if sys.argv[0].endswith('.exe'):
        dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(dir)

# Function removeBadges()
# This function removes the individually downloaded badges from the directory. 
# The function compares the badgesNames to those listed in the SET object and removes them.
# If the file directory is missing badgeNames an error may have occurred.
def removeBadges():
    question = "\nWould you like to delete the individual badge icons you downloaded?" + "\nContinue: 1 - Yes, 0 - No\n"
    deleteChoice = inputHandler(question)

    while SET.MODE == 1 and deleteChoice not in (0,1):
        printError("Invalid Input. Try again.\n", False)
        deleteChoice = inputHandler(question)

    if deleteChoice == 1:
        filelist = [ f for f in os.listdir(os.getcwd()) if f in SET.BADGENAMES ]
        for f in filelist:
            if os.path.isfile(f):
                os.remove(f)
                SET.BADGENAMES.remove(f)
            else:
                print("Error: %s file not found" % f)
    
        if len(SET.BADGENAMES) == 0: print("\nImages Deleted Successfully!\n")
        else: printError("Some of the files may have not been deleted correctly. Please check the directory for any anomalies.", False)


# Function printError()
# param error = The error message to be printed.
# param close = A flag which indicates if the error should cause the program to close for safety.
def printError(error, close):
    print("Error: " + error)
    if close: exit()

# Function inputHandler()
# param question = The given question.
# The function asks for user input until a real value is given then is returned to the previously called function.
def inputHandler(question):
    while True:
        try:
            choice = int(input(question))
            return choice
        except ValueError:
            print("Invalid Input. Please Enter a Number.")

# Function main()
# The main function of the Program. Calls start() and is only used when program is complete.
def main():
    start()
    input("Process Complete! Press any key to close...\n")

main()