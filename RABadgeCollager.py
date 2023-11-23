__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "4.0"

import cv2
import os
import requests
import sys
import numpy as np
import tkinter as tk
from dotenv import load_dotenv
from tkinter.filedialog import askopenfilenames


#4.0 Changelog
# Added the Retroachivements API
# Removed the Need of URL in Set Class Object
# Removed the Need of BADGENAMS in Set Class Object
# Removed Deprecated Function retrieveURL()
# Removed Deprecated Function storeImageLinks()
# Removed Deprecated Function removeLocks()
# Removed BeautifulSoup as it was No Longer Needed
# Converted most functions and variables to proper snake case.
# Added User Required Input to Exit Cases so Users can actually read the Errors before they Close.

#Global Set
global SET

# Class RetroAchievementSet:
# param ID = Game ID of the Given Set
# param BADGENUM = The number of Badges of the Given Set
# param BADGES = The list of Badges of the Given Set
# param LENGTH = The number of Badges to be shown on each Line
# param MODE = The given mode the program will run in
class RetroAchievementSet:
    
    def __init__ (self, ID, BADGENUM, BADGES, LENGTH, SIZE, MODE):
        self.ID = ID
        self.BADGENUM = BADGENUM
        self.BADGES = BADGES
        self.LENGTH = LENGTH
        self.SIZE = SIZE
        self.MODE = MODE


# Function global_set()
# Constructor for the global. Used to easily clear out the value and make it more re-usable.
# Would Potentially be Used in the Future to Download Multiple Sets in a Session.
# param id = id for the Game Set | NA if for Mode 2
# param mode = mode for the given program. 1 is Collaging Site Badges. 2 is Collaging New Badges from Users Computer.
def global_set(id, mode):
    global SET
    SET = RetroAchievementSet(id, 0, [], 0, 64, mode)

# Function start()
# Main Menu of the Program. Asks the user what they would like to use the program for.
# Enters either get_set_badges() for old badges or user_badges() for new badges.
def start():
    print("********************************************************************************")
    print("\nRABADGECOLLAGER: Created By SnowTempest (AdeptTempest on Retroachievements.org)\n")
    print("********************************************************************************")
    question = "\nPlease Choose a Mode To Start:\n" + "1. Collage Old Badges From Site\n" + "2. Collage New Badges From Computer\n"
    mode = input_handler(question)

    while mode not in (1, 2):
        print_error("Invalid Input, Please Try Again.", False)
        mode = input_handler(question)

    if mode == 1: 
        get_set_badges()
    else: 
        user_badges()


# Function get_set_badges()
# First properly stores env credentials into its equivalent values.
# Then the Retroachievements API is called with the credentials and then starts the set info process.
# If any errors occur when the API is called the user is prompted with an ERROR with the status code that they can give the developer.
# Calls get_achievement_data() once API call is successful to parse achievement data with the given API key for the indicated Achievement Set.
def get_set_badges():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    username = os.getenv("RAUSERNAME")

    id = input("\nWhat is the Game ID of the Game you want to get Badges from:\n")
    api_url = f'https://retroachievements.org/API/API_GetGameExtended.php?z={username}&y={api_key}&i={id}'
    response = requests.get(api_url)

    if response.status_code == 200:
        raset_data = response.json()
        global_set(id, mode=1)
        get_achievement_data(raset_data)
    else:
        print_error(f"Retroachievements API Fetch Failed. Status Code: {response.status_code}. Please Contact Developer For Help / More Information.", True)


# Function get_achievement_data()
# param raset_data = The JSON Data returned by the RetroAchievements API which includes set information such as Game Information and Achievement information for the given Set.
# Parses the JSON data for the badge names for each published achievement in the set and stores it into the SET Class Objects Badge List.
# The function calls download_badges once complete to move forward with the download process.
def get_achievement_data(raset_data):
    if len(raset_data) == 0:
        print_error("No Game Data Found for Given Game ID. Program will close.", True)
    elif 'Achievements' in raset_data and not raset_data['Achievements']:
        print_error(f"No Achievement Data Found for {raset_data['Title']}. Program will close.", True)

    print(f"\nSuccessfully Parsed Achievement Data for: {raset_data['Title']}")
    for _, achievement_details in raset_data['Achievements'].items():
            SET.BADGES.append("https://media.retroachievements.org/Badge/" + achievement_details.get('BadgeName') + ".png")

    download_badges()

# Function user_badges()
# Asks the user to select their badges from the file explorer.
# Each image has their size checked and is appended to the SET.BADGES
# Images with invalid sizes will be removed and given an appropiate error.
def user_badges():
    badgeSize = 64
    global_set(id="NA", mode=2)

    root = tk.Tk()
    root.withdraw()

    print("\nPlease Select Your Badges:")
    files = askopenfilenames(title="Select Badges",filetypes=(("PNG files", "*.png"),))
    
    for file in files:
        image = cv2.imread(file)
        width, height = image.shape[:2]

        if (width == badgeSize and height == badgeSize) :
            print("Selected Icon: ", file)
            SET.BADGES.append(file)
            SET.BADGENUM = SET.BADGENUM + 1
        else: 
            print("Selected Icon: ", file + " Error: Does Not Meet Size Requirements (64 x 64).")
    
    if(len(SET.BADGES) == 0):
        print_error("No Valid Badges Listed. Program will Exit.", True)
    
    collage()


# Function download_badges()
# This function downloads all the badges from the list. 
# Closes program if the list is empty.
def download_badges():
    change_directory()

    print("\nDownloading Badges....\n")
    badges_data_bytes = []

    for badge in SET.BADGES:
        badge_name = str(SET.BADGENUM + 1) + "_" + SET.ID + ".png"

        with open(badge_name, 'wb') as f:
            im = requests.get(badge).content
            f.write(im)
            badges_data_bytes.append(badge_name)
        
        SET.BADGENUM = SET.BADGENUM + 1

    SET.BADGES = badges_data_bytes

    print("Download Complete.\n")
    collage()

# Function collage()
# The main collage creation function.
# Calls createHorizontals() first with the given collection of images to create the rows.
# Calls combineHorizontals() afterwards to combine the rows together.
def collage():
    image_collection = []
    question = "\nWould you like the images have padding to make them easier to see?" + "\nContinue: 1 - Yes, 0 - No\n"
    choice = input_handler(question)

    while choice not in (0,1):
        print_error("Invalid Input, Please Try Again.", False)
        choice = input_handler(question)

    for i in range(SET.BADGENUM):
        if SET.MODE == 1:
            image = cv2.imread(f'{i + 1}_' + SET.ID + '.png')
        else:
            image = cv2.imread(SET.BADGES[i])
        if choice == 1:
            SET.SIZE = 66
            image = cv2.copyMakeBorder(image, 1,1,1,1, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        image = cv2.resize(image, (SET.SIZE,SET.SIZE))
        image_collection.append(image)
    
    set_columns()
    horizontals = create_horizontals(image_collection)
    vertical = combine_horizontals(horizontals)

    if SET.MODE == 1:
        remove_badges()
        cv2.imwrite("OLD.png", vertical)
        final = "OLD.png"
    else:
        cv2.imwrite("NEW.png", vertical)
        final = "NEW.png"
    
    if sys.argv[0].endswith('.exe'):
        print("\nCollage has been saved at: " + os.path.dirname(sys.executable) + " called", final)
    else:
        print("\nCollage has been saved at: " + os.path.dirname(__file__) + " called", final)


# Function set_columns()
# This function asks the user for the number of columns they want per row.
# Forces re-input until number given is either not 0 or not greater than the number of badges available.
def set_columns():
    question = "\nHow many badges/cheevos do you want per line: \n"
    SET.LENGTH = input_handler(question)

    while SET.LENGTH <= 0 or SET.LENGTH > SET.BADGENUM:
        print_error("Number of Columns can not be <= 0 and Number of Columns can not be greater than the number of Badges.\n", False)
        SET.LENGTH = input_handler(question)

# Function create_horizontals()
# param collection = The current collection of images to be used for creating the rows.
# Creates each of the rows and stores them in the collection of images.
# Once horizontals are created the list is returned to getCollage().
def create_horizontals(collection):
    padded_image = 255 * np.ones(shape=[SET.SIZE, SET.SIZE, 3], dtype=np.uint8)
    new_horizontals = []
    cur_hori = collection[0]

    for cur in range(1, SET.BADGENUM):
        if cur % SET.LENGTH != 0:
            cur_hori = np.hstack([cur_hori, collection[cur]])
        else:
            new_horizontals.append(cur_hori)
            cur_hori = collection[cur]

    if SET.BADGENUM % SET.LENGTH != 0:
        for i in range(SET.BADGENUM % SET.LENGTH, SET.LENGTH):
            cur_hori = np.hstack([cur_hori, padded_image])

    new_horizontals.append(cur_hori)

    return new_horizontals

# Function combine_horizontals()
# Combines the horizontals together to create the final collage.
# Returns the result to getCollage()
def combine_horizontals(horizontals):
    if len(horizontals) == 1:
        return horizontals[0]
    elif len(horizontals) == 2:
        return np.vstack([horizontals[0], horizontals[1]])
    else:
        cur_hori = None
        for index, horizontal in enumerate(horizontals):
            if index == 0:
                cur_hori = horizontals[0]
            else: 
                cur_hori = np.vstack([cur_hori, horizontal])

    return cur_hori

# Function change_directory()
# Changes the current working directory to be where the executable is located.
# The script directory only matters for my end.
def change_directory():
    if sys.argv[0].endswith('.exe'):
        dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(dir)

# Function removeBadges()
# This function removes the individually downloaded badges from the directory. 
# The function checks if the files in the directory match the files listed in BADGES.
# If the file directory is missing BADGES during deletion an error may have occurred.
def remove_badges():
    question = "\nWould you like to delete the individual badge icons you downloaded?" + "\nContinue: 1 - Yes, 0 - No\n"
    delete_choice = input_handler(question)

    while SET.MODE == 1 and delete_choice not in (0,1):
        print_error("Invalid Input. Try again.\n", False)
        delete_choice = input_handler(question)

    if delete_choice == 1:
        filelist = [ f for f in os.listdir(os.getcwd()) if f in SET.BADGES ]
        for f in filelist:
            if os.path.isfile(f):
                os.remove(f)
                SET.BADGES.remove(f)
            else:
                print("Error: %s file not found" % f)
    
        if len(SET.BADGES) == 0: print("\nImages Deleted Successfully!\n")
        else: print_error("Some of the files may have not been deleted correctly. Please check the directory for any anomalies.", False)


# Function print_error()
# param error = The error message to be printed.
# param close = A flag which indicates if the error should cause the program to close for safety.
def print_error(error, close):
    print("Error: " + error)
    if close:
        input("Press any key to exit...")
        sys.exit()

# Function input_handler()
# param question = The given question.
# The function asks for user input until a real value is given then is returned to the previously called function.
def input_handler(question):
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