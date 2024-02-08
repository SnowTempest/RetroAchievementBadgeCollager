# RetroAchievement Badge Collager
RetroAchievements Badge Scraper. Scrapes the given game ID for its badges and automatically collages them with the given number of columns.

NEW **
Now has the ability to collage your own badges straight from your computer into a collage that can be used for the Icon-Gauntlet.

## Setup

1. **Download**: Download the RABadgeCollager.zip file from the [Releases](https://github.com/SnowTempest/RetroAchievementBadgeCollager/releases/) section of this repository.

2. **Unzip**: Unzip the downloaded zip file to receive the executable for the program and the config file.

3. **Get API Key**: Go to [Retroachievements Control Panel](https://retroachievements.org/controlpanel.php) and copy your Web API key from the Keys section.

4. **Open Config File**: Open the `config.json` file with any text editor of your choice.

5. **Update Configurations**:
   - Replace the placeholder `"YOUR_API_KEY"` with your copied API key inside the quotes for the `"api_key"` field.
   - Replace the placeholder `"YOUR_USERNAME"` with your Retroachievements username inside the quotes for the `"username"` field.
   - Ensure not to delete the quotes accidentally. The updated fields should look like `"your_actual_api_key"` and `"your_username"`.

6. **Save Config File**: Save the changes to the `config.json` file.

7. **Run Program**: Now, run the `RABadgeCollager.exe` program normally.

8. **Troubleshooting**: If you encounter issues with API fetch, double-check that you have pasted your Web API Key correctly into the `config.json` file. If you're unsure about the file's layout, feel free to contact AdeptTempest on RA's Discord.

## Support

If you encounter any difficulties during setup or usage, please don't hesitate to open an issue in this repository or contact AdeptTempest on RA's Discord for assistance.


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
## CV2
Link - https://pypi.org/project/opencv-python/
## Numpy
Link - https://numpy.org/install/

# Usage

1. Download the Executable (RABadgeCollager.exe) from the Releases page.
2. Move the Executable into any empty Folder.
3. Double click and Execute the program.
4. Follow the prompts on the screen.
5. Depending on the Mode the user will be left an image in the program directory with their desired collage.

# Notes:
The program must be in an empty folder to ensure safe deletion of images. Note: Only badge images will be deleted.



