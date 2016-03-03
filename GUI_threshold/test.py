import Tkinter as tk
from tkFileDialog import askdirectory
from PIL import Image, ImageTk


import tkMessageBox

import os

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.controlsArea()		
		self.createWidgets()
		self.loadImages()
		self.createPictureFrame(imagePath="q21notreat_xy01c2.tif")
	
	def showPicName(self):
		index = self.pictureIndex.get(1.0,"end")
		index = int(index.rsplit()[0]) - 1
		image = self.filePaths[index]
		image = image.split("/")[-1]
		print image
		self.pictureLabel = tk.Label(text=image)
		self.pictureLabel.grid(column=0,row=1)


	def controlsArea(self):
		T = tk.Text(self,height=1, width=2)
		T.insert('1.end',"1")
		T.grid(column=1,row=0)
		self.pictureIndex = T
		self.pictureIndex.configure(state='disabled')
		
		LB = tk.Button(self,text="<",command=self.goLeft)
		LB.grid(column=0,row=0)
		self.LB = LB
		
		self.RB = tk.Button(self,text=">",command=self.goRight)
		self.RB.grid(column=2,row=0)	
		
				
	def goLeft(self):
		self.pictureIndex.configure(state='normal')
		index = self.pictureIndex.get(1.0,'end')
		if(len(self.filePaths) == int(index)):
			index = int(index)
		elif(int(index) == 1):
			index=1
		else:
			index = int(index) - 1
		self.pictureIndex.delete(1.0,'end')
		self.pictureIndex.insert(1.0,index)
		self.pictureIndex.configure(state='disabled')
		self.loadCurrentImage()

	def goRight(self):
		self.pictureIndex.configure(state='normal')
		index = self.pictureIndex.get(1.0,'end')
		
		if(len(self.filePaths) == int(index)):
			index = int(index)
		elif(int(index) == 1):
			index= int(index) + 1
		else:
			index = int(index) + 1
		
		self.pictureIndex.delete(1.0,'end')
		self.pictureIndex.insert(1.0,index)
		self.pictureIndex.configure(state='disabled')
		self.loadCurrentImage()

	def loadCurrentImage(self):
		index = self.pictureIndex.get(1.0,"end")
		index = int(index.rsplit()[0]) - 1
		image = self.filePaths[index]
		self.createPictureFrame(image)		

	def loadImages(self):	
		filename = askdirectory()
		
		if(os.path.isdir(filename) == False):
			tkMessageBox.showerror("Not a directory", filename.split("/")[-1] + " is not a directory.")
			self.quit()

		files = os.listdir(filename)

		tifFiles = []

		for file in files:
			if( (file[-4:] == ".tif") or (file[-4:] == ".tiff") ):
				filePath = filename + "/" + file
				tifFiles.append(filePath)

		if(len(tifFiles) == 0):
			tkMessageBox.showerror("No pictures found", "There were not TIF files found in this directory")
		self.filePaths = tifFiles		

	def createPictureFrame(self,imagePath):
		img = Image.open(imagePath)
		img = img.resize((400, 400), Image.ANTIALIAS)
		img = ImageTk.PhotoImage(img)
		imgLoc = "q21notreat_xy01c2.tif"
		text = "q21notreat_xy01c2.tif exists? " + str(os.path.isfile(imgLoc))
		self.pframe = tk.Label(self, image=img)
		self.pframe.image = img
		self.pframe.grid(column=1,row=2)
		self.showPicName()
	
	def createWidgets(self):
		self.quitButton = tk.Button(self, text='Quit',command=self.quit)
		self.quitButton.grid(column=1,row=3)

app = Application()
app.master.title('LOLOLOLOL')
app.mainloop()  
