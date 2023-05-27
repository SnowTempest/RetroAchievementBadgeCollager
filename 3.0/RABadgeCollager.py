__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "3.0"

import tkinter as tk
from tkinter import ttk
from tkinter import font


#The Achievement Set
global SET
global ROOT

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

def window():
    global ROOT
    ROOT = tk.Tk()
    ROOT.title("RABadgeCollager")
    ROOT.geometry("500x500")
    ROOT.configure(bg="black")
    ROOT.resizable(False, False)

    blackBackground = ttk.Style()
    blackBackground.configure('MainFrame.TFrame', background="black")

    frame = ttk.Frame(ROOT, style="MainFrame.TFrame")
    frame.grid(pady=10, padx=15)

    fontStyle = font.Font(size=15, family="Times New Roman")
    ttk.Label(frame, text="Enter Game ID: ", font=fontStyle, foreground="white", background="black").grid(column=1, row=1)

    game_validation = (ROOT.register(validateGameID), '%P')
    game = tk.Entry(frame, font=fontStyle, width=10, validate="key", validatecommand=game_validation)
    submit = tk.Button(frame, text="Submit", width=10, command=lambda: initializeSet(game.get())).grid(column=3, row=1, padx=20)
    game.grid(column=2, row=1)

    ROOT.mainloop()

def initializeSet(game):

    if len(game) == 0:
        createError("Please Enter a Game ID Before Submitting!")
    elif int(game) == 0:
        createError("Game ID 0 is Not Valid! Please Enter A Different Game ID!")
    else: print("Submitted Value:", game)

def createError(errorText):
    fontStyle = font.Font(size=15, family="Times New Roman")
    errorWindow = tk.Toplevel(ROOT)
    errorWindow.configure(bg="black")
    errorWindow.resizable(False, False)
    errorWindow.grab_set()
    errorWindow.title("Error")
    errorLabel = ttk.Label(errorWindow, text=errorText, foreground="white", font=fontStyle, background="black",padding=20)
    labelWidth = errorLabel.winfo_reqwidth()
    labelHeight = errorLabel.winfo_reqheight()
    errorWindow.geometry(f"{labelWidth}x{labelHeight + 50}")
    ok = ttk.Button(errorWindow, text="OK", command=lambda: errorWindow.destroy())

    errorLabel.pack()
    ok.pack()

    errorWindow.wait_window()

def validateGameID(gameID):
    if len(gameID) <= 10: return True
    else: return False

def main():
    window()


main()