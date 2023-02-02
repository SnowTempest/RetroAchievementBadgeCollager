__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "1.0"

import requests
import os
from bs4 import BeautifulSoup
import cv2
import numpy as np

class RetroAchievementSet:
    
    def __init__ (self, ID, URL, BADGENUM, BADGELIST, LENGTH):
        self.ID = ID
        self.URL = URL
        self.BADGENUM = BADGENUM
        self.BADGELIST = BADGELIST
        self.LENGTH = LENGTH

global SET

def getURL():
    global SET

    id = input("What is the Game ID of the Game you want to get Badges from:\n")
    url = "https://retroachievements.org/game/"  + id
    SET = RetroAchievementSet(id, url, 0, [], 0)
    getImageLink()

def getImageLink():
    request = requests.get(SET.URL)
    soup = BeautifulSoup(request.text, 'html.parser')

    print("Game ID Correlates to: " + soup.title.text.replace(" · RetroAchievements", ""))
    choice = input("Continue: 1 - Yes, 0 - No\n")

    if int(choice) == 0:
        print("Program will exit.")
        exit()

    images = soup.find_all('img')
    
    for image in images:
        if "https://media.retroachievements.org/Badge/" in image['src']:
            SET.BADGELIST.append(image['src'])

    removeLocks()
    downloadBadges()

def removeLocks():
    for badge in SET.BADGELIST:
        cur = SET.BADGELIST.index(badge)
        badge = badge.replace("_lock", "")
        SET.BADGELIST[cur] = badge

    return SET.BADGELIST

def downloadBadges():
    changeDirectory()

    print("\nDownloading Badges....\n")

    for badge in SET.BADGELIST:

        with open(str(SET.BADGENUM + 1) + ".png", 'wb') as f:
            im = requests.get(badge).content
            f.write(im)
        SET.BADGENUM = SET.BADGENUM + 1

    print("Download Complete.\n")

    if SET.BADGENUM == 0:
        print("No badges found for Current Game ID. Program will close.")
        exit()

    getCollage()

def getCollage():
    imageCollection = []

    for i in range(SET.BADGENUM):
        image = cv2.imread(f'{i + 1}.png')
        image = cv2.resize(image, (64,64))
        imageCollection.append(image)

    SET.LENGTH = int(input("How many badges/cheevos do you want per line: "))

    if SET.LENGTH > SET.BADGENUM:
        print("Cannot have number of columns greater than the number of badges. Please Restart.")
        exit()

    horizontals = createHorizontals(imageCollection)
    vertical = combineHorizontals(horizontals)

    removeBadges()

    cv2.imwrite("OLD.png", vertical)

def changeDirectory():
    os.chdir(os.path.join(os.path.dirname(__file__)))

def createHorizontals(collection):
    paddedImage = 255 * np.ones(shape=[64, 64, 3], dtype=np.uint8)
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

def removeBadges():
    filelist = [ f for f in os.listdir(os.getcwd()) if f.endswith(".png") ]
    for f in filelist:
        if os.path.isfile(f):
            os.remove(f)
        else:
            print("Error: %s file not found" % f)

def main():
    getURL()
    print("Collage has been saved at: " + os.path.dirname(__file__) + " called OLD.png.")

main()





