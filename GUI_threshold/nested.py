import Tkinter as tk
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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
		self.adapt = ttk.Frame(n)
		self.manu = ttk.Frame(n)
		self.otsu = ttk.Frame(n)
		n.add(self.adapt,text="Adaptive")
		n.add(self.manu, text="Manual")
		n.add(self.otsu, text="Otsu's Method")
		self.controlsArea = n
		self.controlsArea.pack(side='top',fill='both',expand='yes')
		
	
		# Creating the controls area for the manual input
		self.manu.controlsFrame = tk.Frame(self.manu)
		self.manu.controlsFrame.pack(side='top')

		ThreshLabel = tk.Label(self.manu.controlsFrame, text="Set threshold value")
		ThreshLabel.pack(side='left',expand=True)	

		checkThresh = self.manu.register(self.validate)	
		self.manuThreshEntry = tk.Entry(self.manu.controlsFrame, validate='key', validatecommand=(checkThresh, '%P'))
		self.manuThreshEntry.pack(side='left',expand=True)
		self.manuThresh = 20

		self.manuThreshButton = tk.Button(self.manu.controlsFrame, text="Preview",state='disabled',command=self.manuPreview)
		self.manuThreshButton.pack(side='left',expand=False, fill='x')


		# Adds a new frame for the description and submission of the job
		self.manu.description = tk.Frame(self.manu)
		self.manu.description.pack(side='top',fill='x',expand=False)

		self.manu.description.text = tk.Text(self.manu.description,bg='lightgrey',height=3,  bd=0, wrap='word')
		
		self.manu.description.text.insert('end',"In this mode, select and preview different threshold values. Once satisfied with your decision, press SUBMIT to threshold all the images in this folder at the value displayed in the box above.")
		
		self.manu.description.text.pack(side="left",fill='x',expand=False)

		self.manu.description.submit = tk.Button(self.manu.description, text="submit")
		self.manu.description.submit.pack(side="left",fill='both',expand=True)
	
		# Creating the histogram template
		self.hist = Figure(figsize=(3,2), dpi=100)
		self.plot = self.hist.add_subplot(111)		
		self.plot.set_yscale('log')
		
		self.canvas = FigureCanvasTkAgg(self.hist, master = self.manu)
		self.canvas.get_tk_widget().pack(side='top', fill=tk.BOTH, expand=1)

		# Special middle frame containing pictureframe and direction buttons
		self.outerFrame.middleFrame = tk.Frame(self.outerFrame)
		self.outerFrame.middleFrame.pack(side='top',fill='both',expand=True)	

		# Right Side
		self.goRight = tk.Frame(self.outerFrame.middleFrame)
		self.goRight.pack(side='right',fill='y',expand='yes')	
		self.goRight.button = tk.Button(self.goRight,text="->",command=self.rightButtonClick)		
		self.goRight.button.pack(side='right',fill='both',expand=True)		

		# Picture Frame
		self.pictureFrame = tk.Frame(self.outerFrame.middleFrame,width=400,height=400)
		self.pictureFrame.pack(side='right',fill='both',expand='yes')
		
		self.pictureFrame.picture = tk.Label(self.pictureFrame)
		self.pictureFrame.picture.place(relx=0.5,rely=0.5,anchor='center')

		self.pictureFrame.transPicture = tk.Label(self.pictureFrame)
		self.pictureFrame.transPicture.place(relx=0.5,rely=0.5, anchor='center')

		# Left Side
		self.goLeft = tk.Frame(self.outerFrame.middleFrame)
		self.goLeft.pack(side='right',fill='y',expand='yes')	
		self.goLeft.button = tk.Button(self.goLeft,text="<-",command=self.leftButtonClick)		
		self.goLeft.button.pack(side='right',fill='both',expand=True)		


		# Picture Information
		self.pictureInfo = tk.Frame(self.outerFrame)
		self.pictureInfo.pack(side='bottom',fill='x',expand='no')

		self.pictureInfo.picName = tk.Label(self.pictureInfo, text = "")
		self.pictureInfo.picName.pack(side='left',fill='both',expand='yes')


		self.pictureInfo.indexText = tk.Label(self.pictureInfo,text="")
		self.pictureInfo.indexText.pack(side='left',fill='both',expand='yes')
	

	def manuPreview(self):
		ret,threshPic = cv2.threshold(self.img,float(self.manuThresh),255,cv2.THRESH_BINARY)	
		#backtorgb = cv2.cvtColor(threshPic,cv2.COLOR_GRAY2RGB)	
		threshPic = Image.fromarray(threshPic,"L")
		self.pictureFrame.transPicture.configure(image=threshPic)
		self.threshPic=threshPic	
		self.loadHist()

	def validate(self,P):
		if(P == ""):
			self.manuThreshButton.config(state='disabled')
			return True
		if(int(P)<256) and(int(P >= 0)):
			self.manuThreshButton.config(state='normal')
			self.manuThresh=P
			return True
		else:
			self.manuThreshButton.config(state='disabled')
			return True

	def loadHist(self):	
		self.plot.clear()
		self.plot.set_yticks([])
		self.plot.set_xticks([])
		self.plot.axvline(self.manuThresh, color='b',linestyle = 'solid', linewidth=2)
		p = self.hist.gca()
		p.hist(self.img.ravel(), 256)
		self.canvas.show()
	
	def loadImageArray(self):
		index = self.index-1
		image = self.filePaths[index]
		img = cv2.imread(image)
		self.img = img

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

	def leftButtonClick(self):
		index = self.index
		if( index == 1):
			index = index
		else:
			index = index-1
		self.index = index
		self.loadCurrentImage()

	def rightButtonClick(self):				
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
		self.loadImageArray()	
		self.loadHist()

	
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


  
