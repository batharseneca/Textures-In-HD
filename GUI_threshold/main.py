

from Tkinter import *
from tkFileDialog import askopenfilename

import PIL

from PIL import Image
from PIL import ImageTk

import os




app = Tk()

filename = askopenfilename()

print filename[-4:]

if(filename[-4:] != ".csv"):
	exit()


f = open(filename,"r")
picPaths = []
# Get all of the paths
for line in f:
	path = line.split(",")[5].rstrip()
	picPaths.append(path)

length = len(picPaths)

img = Image.open(picPaths[0])
img = img.resize((250, 250), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)

panel = Label(app, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")


fname.pack()

def on_closing():
	exit()

app.protocol("WM_DELETE_WINDOW", on_closing)



app.mainloop()

