import Tkinter as tk


import ttk as ttk

from tkFileDialog import askdirectory
from PIL import Image, ImageTk


import tkMessageBox

import os




class Application:
	def __init__(self, parent):
		
		self.myParent = parent
		self.makeTemplate()	
		self.loadImages()
			
		self.myParent.bind('<Left>', self.leftButton)
		self.myParent.bind('<Right>', self.rightButton)
	
	def makeTemplate(self):
		
		# Outer parent frame (OuterFrame)
		self.outerFrame = tk.Frame(self.myParent,borderwidth=2, relief="ridge", width=200, height=100)
		self.outerFrame.pack()

		# Controls Area Frame
		n  = ttk.Notebook(self.outerFrame)
		adapt = ttk.Frame(n)
		manu = ttk.Frame(n)
		otsu = ttk.Frame(n)
		n.add(adapt,text="Adaptive")
		n.add(manu, text="Manual")
		n.add(otsu, text="Otsu's Method")
		self.controlsArea = n
		self.controlsArea.pack(side='top',fill='both',expand='yes')


		
		# Special middle frame containing pictureframe and direction buttons
		self.outerFrame.middleFrame = tk.Frame(self.outerFrame)
		self.outerFrame.middleFrame.pack(side='top',fill='both',expand=True)	




		# Right Side
		self.goRight = tk.Frame(self.outerFrame.middleFrame)
		self.goRight.pack(side='right',fill='y',expand='yes')	
		self.goRight.button = tk.Button(self.goRight,text="->",command=self.rightButton)		
		self.goRight.button.pack(side='right',fill='both',expand=True)		

		# Picture Frame
		self.pictureFrame = tk.Frame(self.outerFrame.middleFrame)
		self.pictureFrame.pack(side='right',fill='both',expand='yes')
		
		self.pictureFrame.picture = tk.Label(self.pictureFrame)
		self.pictureFrame.picture.pack(side='right',fill='both',expand='yes')

		# Left Side
		self.goLeft = tk.Frame(self.outerFrame.middleFrame)
		self.goLeft.pack(side='right',fill='y',expand='yes')	
		self.goLeft.button = tk.Button(self.goLeft,text="<-",command=self.leftButton)		
		self.goLeft.button.pack(side='right',fill='both',expand=True)		


		# Picture Information
		self.pictureInfo = tk.Frame(self.outerFrame)
		self.pictureInfo.pack(side='bottom',fill='x',expand='no')

		self.pictureInfo.picName = tk.Label(self.pictureInfo, text = "")
		self.pictureInfo.picName.pack(side='bottom',fill='both',expand='yes')

		self.pictureInfo.indexText = tk.Label(self.pictureInfo,text="")
		self.pictureInfo.indexText.pack(side='bottom',fill='both',expand='yes')


	def leftButton(self,event):
		index = self.index
		if( index == 1):
			index = index
		else:
			index = index-1
		self.index = index
		self.loadCurrentImage()

	def rightButton(self,event):				
		index = self.index
		if(len(self.filePaths) == int(index)):
			index = int(index)
		else:
			index = int(index) + 1
		self.index = index
		self.loadCurrentImage()


	def loadPictureInfo(self):
		pictureName = self.filePaths[self.index-1]
		pictureName = pictureName.split("/")[-1]	
		self.pictureInfo.picName.configure(text=pictureName)
			
		indexText = str(self.index) + "/" + str(len(self.filePaths))
		self.pictureInfo.indexText.configure(text=indexText)	

	
	def loadCurrentImage(self):
		index = self.index
		image = self.filePaths[index-1]
		
		img = Image.open(image)
		img = img.resize((500,500), Image.ANTIALIAS)
		img = ImageTk.PhotoImage(img)
		self.pictureFrame.picture.configure(image=img)
		self.pictureFrame.picture.picRef = img	
		
		self.loadPictureInfo()
		
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
			self.quit()
		self.filePaths = tifFiles		
		self.index=1
		self.loadCurrentImage()	

root = tk.Tk()
app = Application(root)
app.myParent.title("Image Thresholding")
root.mainloop()


  
