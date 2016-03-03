

from Tkinter import *
from tkFileDialog import askdirectory

import PIL

from PIL import Image
from PIL import ImageTk

import os


import tkMessageBox

app = Tk()

app.title("Threshold")

filename = askdirectory()

if(os.path.isdir(filename) == False):
	tkMessageBox.showerror("Not a directory", filename.split("/")[-1] + " is not a directory.")
	exit()

files = os.listdir(filename)

tifFiles = []

for file in files:
	if( (file[-4:] == ".tif") or (file[-4:] == ".tiff") ):
		tifFiles.append(file)
		continue
	else:

if(len(tifFiles) == 0):
	tkMessageBox.showerror("No pictures found", "There were not TIF files found in this directory")
	exit()




exit()


picPaths = []
#Get all of the paths
for line in f:
	path = line.split(",")[5].rstrip()
	picPaths.append(path)

length = len(picPaths)


def displayimg(lineNumber):	
	img1 = Image.open(picPaths[lineNumber])
	img1 = img1.resize((250, 250), Image.ANTIALIAS)
	img1 = ImageTk.PhotoImage(img1)
	panel = Label(app,image=img)
	panel.pack(side="bottom",fill="both",expand="yes")


def on_closing():
	exit()

app.protocol("WM_DELETE_WINDOW", on_closing)



app.mainloop()

