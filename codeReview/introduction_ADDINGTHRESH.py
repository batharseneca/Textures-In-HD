# Authors: Nishanth Merwin, Bilal Athar, Tyler Murphy
# Purpose: A GUI tool for image manipulation and extraction of texture features from 


from tkFileDialog import askdirectory
import Tkinter as tk
import ttk as ttk
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import tkMessageBox
from PIL import Image, ImageTk
import tkFont
import re

'''
- Need to add more variables for config (otsus when finished ex.) 
- Need to set proper holders and write big IF loop for run button processing.
'''


"""
The config class stores the user options that are recorded through the GUI. It is passed into the final function so that
the program knows what type of analysis to do.
"""
class Config:	
	def __init__(self):
		Config.CFGdirectory = 0
		Config.CFGbitConversion = 0
		Config.CFGadaptThresh = 0
		Config.CFGmanuThresh = 0
		Config.CFGtextureAnalysis = 0
	
	def returnMethod(self):
		configArray = []
		configArray.append(Config.CFGdirectory)
		configArray.append(Config.CFGbitConversion)
		configArray.append(Config.CFGadaptThresh)
		configArray.append(Config.CFGmanuThresh)
		configArray.append(Config.CFGtextureAnalysis)
		
		return configArray


"""
This class holds the main GUI. It takes in a Config object and asks users for settings before running the analysis.
"""
class Introduction(Config):

	"""
	Initializes the class
	"""
	def __init__(self,parent):
		self.myParent = parent
		self.makeTemplate()
		self.config = Config()		
		
	"""
	This class actually creates all the buttons and layout for the base GUI. 
	"""
	def makeTemplate(self):
		# Outer parent frame (OuterFrame)
		self.outerFrame = tk.Frame(self.myParent,borderwidth=2, relief="ridge", width=1000, height=700)
		self.outerFrame.pack(expand=False)

		# self.outerFrame.pack_propagate(0)

		# Make a frame label for introduction
		self.infoFrame = tk.Frame(self.outerFrame)
		font = tkFont.Font(family="Helvetica", size=8)
		self.infoFrame.pack(side="top" ,expand=1 ,fill="x" ,pady=0)
		infoLabel = tk.Text(self.infoFrame,bg=self.myParent.cget("bg"), font=font, height=12,width=110, wrap="word",bd=0)
		infoLabel.insert("end", '''
This software enables extraction of texture features within image sets. This involves four main steps as described below.
1. Ensure that all images are placed within the same directory and selected with the 'Choose Directory' button below. The selected directory should not contain any sub-directories.
2. It is strongly suggested to convert images to 8 bit format prior to further analysis.
3. Several algorithms have been proposed to efficiently threshold images. Enable thresholding and configure according to the directions to adjust the settings to best suit the image dataset provided.
4. The final step in extracting texture features involves constructing a grey level co-occurence matrix (GLCM) from each image according to the configurations provided. From here, 13 haralick features will be created and outputted into a CSV file within the same directory.
Each step can be completed on its own. However, we suggest following the guidelines above to ensure the most efficient and optimized processing.
Designed for the Ray Truant research lab.
'''.strip())
		infoLabel.configure(state="disabled")
		# infoLabel.tag_configure("center",justify="center")
		# infoLabel.tag_add("center", 1.0, "end")
		infoLabel.pack(side="top", expand=0, fill="none")


		# Make a button for choosing directories
		self.dirFrame = tk.Frame(self.outerFrame)
		self.dirFrame.pack(side="top",expand=1, fill="x", pady=[0,20])
		self.dirButton = tk.Button(self.dirFrame, text="Choose Picture Directory", command=self.chooseDirectory)
		self.dirButton.pack(side="top",expand=1, fill="none")

		self.dirLabel = tk.Label(self.dirFrame, text="")
		self.dirLabel.pack(side="top")



		tk.Frame(self.outerFrame, relief="solid", borderwidth=2, bg="darkgrey").pack(side="top", fill="x")

		# Convert to bit section
		self.bitFrame = tk.Frame(self.outerFrame)
		self.bitFrame.pack(side="top",expand=0,fill="x",ipady=30)


		# Creates the checkbox
		self.bitCheck = tk.IntVar()
		self.bitCheckBox = tk.Checkbutton(self.bitFrame, text="Enable", variable=self.bitCheck, command=self.bitFunction, padx=70)
		self.bitCheckBox.configure(state="disabled")
		self.bitCheckBox.pack(side="left",expand=1, fill="none", anchor="w")



		# Creates the frame which holds the label for the checkmark image
		self.bitImageFrame = tk.Frame(self.bitFrame, width=30, height=30)
		self.bitImageFrame.pack(side="right", expand=0, fill="none",ipadx=20, anchor="e")
		# Makes it so that the frame stays the same size
		self.bitImageFrame.pack_propagate(0)

		# Creates the label for the description
		bitLabel = tk.Text(self.bitFrame,height=2,width=75,bg=self.myParent.cget("bg"), bd=0, wrap="word")
		bitLabel.insert("end", "8 bit images are ideal for image analysis. If your images are not already in this format, this option will convert them to 8bit format.")
		bitLabel.configure(state="disabled")
		bitLabel.tag_configure("center",justify="center")
		bitLabel.tag_add("center", 1.0, "end")
		bitLabel.pack(side="right")

		# Opens the image file and displayes it within the frame
		image = Image.open("check.png")
		image = image.resize((30,30), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(image)
		self.bitImage = tk.Label(self.bitImageFrame,image=photo)
		self.bitImage.photo = photo
		self.bitImage.pack(in_=self.bitImageFrame)
		self.bitImage.pack_forget()



		# Convert to bit section
		self.threshFrame = tk.Frame(self.outerFrame)
		self.threshFrame.pack(side="top",expand=0,fill="x", ipady=30)


		# Creates the checkbox
		self.threshCheck = tk.IntVar()
		self.threshCheckBox = tk.Checkbutton(self.threshFrame, text="Enable", variable=self.threshCheck, command=self.threshFunction, padx=70)
		self.threshCheckBox.configure(state="disabled")
		self.threshCheckBox.pack(side="left",expand=1, fill="none", anchor="w")


		# Creates the button
		self.threshButton = tk.Button(self.threshFrame, text="Configure Thresholding", command=self.threshConfigure, width=20)
		self.threshButton.pack(side="left",fill="none")
		self.threshButton.configure(state="disabled")


		# Creates the frame which holds the label for the checkmark image
		self.threshImageFrame = tk.Frame(self.threshFrame, width=30, height=30)
		self.threshImageFrame.pack(side="right", expand=0, fill="none",ipadx=20)
		# Makes it so that the frame stays the same size
		self.threshImageFrame.pack_propagate(0)

		self.threshImage = tk.Label(self.threshImageFrame, image=photo)
		self.threshImage.photo = photo
		self.threshImage.pack(in_=self.threshImageFrame)
		self.threshImage.pack_forget()



		# Creates the text description
		threshText = tk.Text(self.threshFrame, height=4,width=75,bd=0, bg=self.myParent.cget("bg"), wrap="word")
		threshText.insert("end","Thresholding selects portions of the image to analyse using various algorithms. Unless already thresholded, use this option to select your thresholding configuration.")
		threshText.configure(state="disabled")
		threshText.tag_configure("center",justify="center")
		threshText.tag_add("center", 1.0, "end")
		threshText.pack(side="right", padx=[20,0])


		# Convert to bit section
		self.textureFrame = tk.Frame(self.outerFrame)
		self.textureFrame.pack(side="top",expand=0,fill="x", ipady=30)


		# Creates the checkbox
		self.textureCheck = tk.IntVar()
		self.textureCheckBox = tk.Checkbutton(self.textureFrame, text="Enable", variable=self.textureCheck, command=self.textureFunction, padx=70)
		self.textureCheckBox.configure(state="disabled")
		self.textureCheckBox.pack(side="left",expand=1, fill="none", anchor="w")


		# Creates the button
		self.textureButton = tk.Button(self.textureFrame, text="Configure GLCM", command=self.textureConfigure, width=20)
		self.textureButton.pack(side="left",fill="none")
		self.textureButton.configure(state="disabled")


		# Creates the frame which holds the label for the checkmark image
		self.textureImageFrame = tk.Frame(self.textureFrame, width=30, height=30)
		self.textureImageFrame.pack(side="right", expand=0, fill="none",ipadx=20)
		# Makes it so that the frame stays the same size
		self.textureImageFrame.pack_propagate(0)

		self.textureImage = tk.Label(self.textureImageFrame, image=photo)
		self.textureImage.photo = photo
		self.textureImage.pack(in_=self.textureImageFrame)
		self.textureImage.pack_forget()



		# Creates the text description
		textureText = tk.Text(self.textureFrame, height=4,width=75,bd=0, bg=self.myParent.cget("bg"), wrap="word")
		textureText.insert("end","This step takes the images and constructs a GLCM. From here, it calculates statistical values describing the textures within each image.")
		textureText.configure(state="disabled")
		textureText.tag_configure("center",justify="center")
		textureText.tag_add("center", 1.0, "end")
		textureText.pack(side="right", padx=[20,0])


		tk.Frame(self.outerFrame, relief="sunken", borderwidth=1, bg="black").pack(side="top", fill="x")


		# Creates a run button
		self.runFrame = tk.Frame(self.outerFrame)
		self.runFrame.pack(fill="x", pady=20)

		self.runButton = tk.Button(self.runFrame, text="Run!", command=self.runConfigure)
		self.runButton.pack(side="right", padx=20, anchor="e")



	"""
	This method validates the parameters the users submit when they hit run. If all the settings are valid, it starts the run and shows a progress menu.
	"""
	def runConfigure(self):

		# Returns all the parameters from the config object
		configArray = self.config.returnMethod()
		directoryChoice, bitChoice, adaptiveThresh, manuThresh, textureAnalysis = configArray
		print "Directory Select? ", directoryChoice, "\n", "bitChoice Select? ", bitChoice, "\n", "manual Thresholding Select? ", manuThresh, "\n", "adaptive Thresholding Select? ", adaptiveThresh, "\n", "Texture Analysis Select? ", textureAnalysis, "\n"
		

		# Configures the labels according to the name of the steps chosen
		checkArray = ['Directory', 'Bit Conversion', 'Adaptive Thresholding', 'Manual Thresholding', 'Texture Analysis']
		stepsArray = []
		for index in range (1,5):
			if configArray[index] == 1:
				stepsArray.append(checkArray[index])
		
		numofSteps = len(stepsArray)
		
		# Checks for validity, and then displays the progress bar 
		if (directoryChoice == 0):
			tkMessageBox.showwarning("Warning - Invalid Parameters", "No Input Image Set Detected")
		elif (numofSteps == 0):
			tkMessageBox.showwarning("Warning - Invalid Parameters", "No Analysis Options Specified")
		else:			
			self.myParent.withdraw()
			self.runWindow = tk.Toplevel(root)
			self.runWindow.wm_title("Data Analysis in Progress")
			
			self.outerFrame4 = tk.Frame(self.runWindow, borderwidth=2, relief="ridge", width=400, height=400)
			self.outerFrame4.pack(padx=20,pady=20)
			
			labelImageProcess = tk.Label(self.outerFrame4, text="Processing Image: (Holder For Index Variable)" + " Of " + str(len(self.tifFiles)) + " Images" )
			labelImageProcess.grid(row=0, column =0, padx=20, pady=10, sticky="wens")
			if "Texture Analysis" in stepsArray:
				labelImageProcess.config(text = "Processing Image: (Holder For Index Variable)" + " Of " + str(len(self.tifFiles)) + " Images   Neighbourhood Block: " + "(Holder for index) Of " + str(len(self.input_array)))
			
			h=1
			label = {}
			for step in stepsArray:
			lb = tk.Label(self.outerFrame4, text="Step " + str((stepsArray.index(step) + 1)) + ": " + step)
			lb.grid(row=h, column =0, padx=10, pady=5, sticky="w")
			label[step] = lb		
			lb2 = tk.Label(self.outerFrame4, text="Pending")
			lb2.grid(row=h, column=1, padx=10, pady=5, sticky="w")
			label[step + "a"] = lb2	
			h +=1
			
			h+=1
			### TEMP EXIT PLACED BELOW FOR TESTING ###
			self.returnWindow = tk.Button(self.outerFrame4, text="Return Window", command=self.OnClickReturn)
			self.returnWindow.grid(row=h, column =0, padx=20, pady=10, sticky="wens")

"""	
		
			## BELOW CODE TO CHANGE THE DISPLAY AS ONE STEP COMPLETES - STILL NEED TO DEAL WITH MULTIPLE N values for texture analysis currentStep = 1
	#			if (currentStep < numofSteps):
	#				currentStep+1
	#			label[stepsArray[currentStep] + "a"].config(text = "In Progress")
	#	- IF STATEMENT AND ACTUAL CODE EXECUTION WILL GO HERE -
	#		
		#	can use time import http://stackoverflow.com/questions/3620943/measuring-elapsed-time-with-the-time-module

"""	
	
	
	### TEMP EXIT PLACED BELOW FOR TESTING ### 
	def OnClickReturn(self):
		self.myParent.deiconify()
		self.runWindow.destroy()
		

	"""
	This opens the texture configuration menu, allowing users to preview their code as they go along.
	"""		
	def textureConfigure(self):
		print "Hello"
		self.textureWindow = tk.Toplevel(root)
		self.textureWindow.wm_title("Texture Analysis")
		self.textureWindow.grab_set()
		
		self.makeTemplateTexture()
		
################################################################# TEXTURE ANALYSIS CODE 


	"""
	Creates the layout for the texture analysis GUI
	"""
	def makeTemplateTexture(self):
		self.outerFrame3 = tk.Frame(self.textureWindow, borderwidth=2, relief="ridge", width=100, height=400)
		self.outerFrame3.pack(padx=20,pady=20)

		# INSTRUCTIONS ROW ####
		self.instructions = tk.Frame(self.outerFrame3)
		self.instructions.pack(side='top',fill='x',expand=False)

		self.instructions.text = tk.Text(self.instructions,bg="lightgrey",height=3,bd=0, wrap='word')
		self.instructions.text.insert ('end',"In the following Textbox please input the neighborhood values you would like to see the IGLCM constructed around. Please format the values as a list of numbers seperated by ',' e.g 1,2,3")
		self.instructions.text.pack(side="left",fill='none',expand=False, padx=10, pady=10)
		self.instructions.text.configure(state='disabled')

		# INPUT ROW ###
		self.inputbox = tk.Frame(self.outerFrame3)
		self.inputbox.pack(side='top',fill='x',expand=False)

		self.entryVariable = tk.StringVar()
		checkSizes = self.outerFrame3.register(self.validate2)
		self.entry = tk.Entry(self.inputbox, textvariable=self.entryVariable, validate='key', validatecommand=(checkSizes, '%P'))
		self.entry.pack(side='left',padx=100, pady=10)

		self.clearInput = tk.Button(self.inputbox, text="Clear Values",state='disabled',command=self.OnClearClick)
		self.clearInput.pack(side='left', fill='x', expand=True)

		self.submitInput = tk.Button(self.inputbox, text="Submit", state='disabled', command=self.OnSubmitClick)
		self.submitInput.pack(side='left', padx=50, fill='x', expand=True)


		# REGEX GUIDELINE ROW
		self.guideline = tk.Frame(self.outerFrame3)
		self.guideline.pack(side='top',fill='x',expand=False)

		self.guideline.text = tk.Text(self.guideline,bg="lightgrey",height=10,bd=0, wrap='word')
		self.guideline.text.insert ('end',"\n	Guidelines:	\n\n 1) Seperate each entry with a comma\n 2) Do not end list with a comma"
									"\n 3) All enteries must be valid digits between 0-99\n 4) Do not use leading 0's e.x 09\n\n	Invalid Enteries will disable the Submit option")
		self.guideline.text.pack(side="left",fill='none',expand=False, padx=10, pady=10)
		self.guideline.text.configure(state='disabled')


	"""
	Dynamic validation of the entry field to activate / disable the submit button
	"""
	def validate2(self,P):
		if(P==""):
			self.clearInput.config(state='disabled')
			self.submitInput.config(state='disabled')
			return True
		else:
			self.clearInput.config(state='normal')

			my_string = [x.strip() for x in P.split(',')]
			check =[]
			zy =""
			pattern = re.compile("^([1-9]{1}[0-9]{0,1})$")
			for x in range (0,len(my_string)):
				if (pattern.match(my_string[x])):
					check.append("a")
				else:
					check.append("b")

			zy = "".join(check)

			if (bool(re.search("b",zy))):
				self.submitInput.config(state='disabled')
			else:
				self.submitInput.config(state='normal')
			return True

	"""
	Clears user input
	"""
	def OnClearClick(self):
		self.entryVariable.set("")

	"""
	When users submit, it saves the user settings and returns to the previous screen
	"""
	def OnSubmitClick(self):
		input_string = self.entryVariable.get()
		self.input_array = [x.strip() for x in input_string.split(',')]
		Config.CFGtextureAnalysis = 1
		self.textureWindow.destroy()
		
#################################################################

	"""
	Responds to the checkbox to turn on/off the button for texture analysis
	"""
	def textureFunction(self, event=None):
		if(self.textureCheck.get() == 1):
			self.textureImage.pack(in_=self.textureImageFrame)
			self.textureButton.configure(state="normal")
		else:
			self.textureImage.pack_forget()
			self.textureButton.configure(state="disabled")
			Config.CFGtextureAnalysis = 0

	"""
	Opens the thresholding window and adds button bindings 
	"""
	def threshConfigure(self):
		print "Hello"		
		self.thresholdWindow = tk.Toplevel(root)
		self.thresholdWindow.wm_title("Image Thresholding")
		self.thresholdWindow.grab_set()
		
		self.makeTemplateThresh()
		self.loadImages()

		self.thresholdWindow.bind('<Left>', self.leftButton)
		self.thresholdWindow.bind('<Right>', self.rightButton)
					
################################################################# THRESHOLDING CODE 
	

	"""
	Creates the layout of the thresholding GUI. Buttons, images, etc.
	"""
	def makeTemplateThresh(self):
		# Outer parent frame (OuterFrame2)
		self.outerFrame2 = tk.Frame(self.thresholdWindow, borderwidth=2, relief="ridge", width=200, height=100)
		self.outerFrame2.pack()

		# Controls Area Frame
		n  = ttk.Notebook(self.outerFrame2)
		self.adapt = ttk.Frame(n)
		self.manu = ttk.Frame(n)
		self.otsu = ttk.Frame(n)
		n.add(self.adapt,text="Adaptive")
		n.add(self.manu, text="Manual")
		n.add(self.otsu, text="Otsu's Method")
		self.controlsArea = n
		self.controlsArea.pack(side='top',fill='both',expand='yes')


		# Creates the adaptive thresholding controls area for block size
		self.adapt.controlsFrame = tk.Frame(self.adapt)
		self.adapt.controlsFrame.pack(side='top')

		n_hoodLabel = tk.Label(self.adapt.controlsFrame, text= "Set block size (must be odd integer): ")
		n_hoodLabel.pack(side='left',expand=True,ipady=30)

		checkBlock = self.adapt.register(self.validateBlock)
		self.adaptBlockEntry = tk.Entry(self.adapt.controlsFrame, validate='key', validatecommand=(checkBlock,'%P'))
		self.adaptBlockEntry.pack(side='left',expand=True)
		self.blockSize=0

		# Creates the radio buttons for mean or gaussian adaptive weighting and the submit button
		self.adapt.radioFrame = tk.Frame(self.adapt)
		self.adapt.radioFrame.pack(side='top',ipady=30)

		self.adapt.weighting = tk.StringVar()
		self.adapt.weighting.set("")

		self.adapt.weighting.trace("w",self.validateAdaptRadio)


		tk.Radiobutton(self.adapt.radioFrame, text="Mean Weighting", variable=self.adapt.weighting, value="mean").pack(side='left')
		tk.Radiobutton(self.adapt.radioFrame, text="Gaussian Weighting", variable=self.adapt.weighting, value="gaussian").pack(side='left')


		self.adaptPreview = tk.Button(self.adapt.radioFrame, text="Preview", state='disabled', command=self.adaptPreview)
		self.adaptPreview.pack(side='left',padx=100,ipadx=40)


		# Adds a new frame for the description and submission of the job
		self.adapt.description = tk.Frame(self.adapt)
		self.adapt.description.pack(side='top',fill='x',expand=False)

		self.adapt.description.text = tk.Text(self.adapt.description,bg='lightgrey',height=5,  bd=0, wrap='word')

		self.adapt.description.text.insert('end',"Adaptive thresholding uses pixel neighbourhoods to threshold according to small regions of the image. This technique is especially useful when different regions of the image contain varying brightness. The pixel neighbourhoods can either be measured simply as the mean or using a gaussian weighted sum.")

		self.adapt.description.text.pack(side="left",fill='x',expand=False)

		self.adapt.description.submit = tk.Button(self.adapt.description, text="submit",state='disabled', command=self.adaptSubmit)
		self.adapt.description.submit.pack(side="left",fill='both',expand=True)

				## ADDING TO CLOSE WINDOW #
		
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

		self.manu.description.submit = tk.Button(self.manu.description, text="submit",state='disabled', command=self.manuSubmit)
		self.manu.description.submit.pack(side="left",fill='both',expand=True)
		
				## ADDING TO CLOSE WINDOW ##

		# Creating the histogram template
		self.hist = Figure(figsize=(3,2), dpi=100)
		self.plot = self.hist.add_subplot(111)
		self.plot.set_yscale('log')

		self.canvas = FigureCanvasTkAgg(self.hist, master = self.manu)
		self.canvas.get_tk_widget().pack(side='top', fill=tk.BOTH, expand=1)

		# Special middle frame containing pictureframe and direction buttons
		self.outerFrame2.middleFrame = tk.Frame(self.outerFrame2)
		self.outerFrame2.middleFrame.pack(side='top',fill='both',expand=True)

		# Right Side
		self.goRight = tk.Frame(self.outerFrame2.middleFrame)
		self.goRight.pack(side='right',fill='y',expand='yes')
		self.goRight.button = tk.Button(self.goRight,text="->",command=self.rightButtonClick)
		self.goRight.button.pack(side='right',fill='both',expand=True)

		# Picture Frame
		self.pictureFrame = tk.Frame(self.outerFrame2.middleFrame,width=1000,height=500)
		self.pictureFrame.pack(side='right',expand=False)

		self.pictureFrame.pack_propagate(0)

		self.pictureFrame.raw = tk.LabelFrame(self.pictureFrame,text="Raw Image", padx=5, pady=5, height=500,width=500)
		self.pictureFrame.raw.pack(side='right',fill='both',expand=True)
		self.pictureFrame.picture = tk.Label(self.pictureFrame.raw)
		self.pictureFrame.picture.pack(side='right')


		self.pictureFrame.raw.pack_propagate(0)

		self.pictureFrame.thresh = tk.LabelFrame(self.pictureFrame,text="Thresholded Region (included areas in blue)", padx=5, pady=5, height=500,width=500)
		self.pictureFrame.thresh.pack(side='right',expand=True,fill='both')

		self.pictureFrame.thresh.pack_propagate(0)

		self.pictureFrame.transPicture = tk.Label(self.pictureFrame.thresh)
		self.pictureFrame.transPicture.pack(side='right',fill='both',expand=True)


		# Left Side
		self.goLeft = tk.Frame(self.outerFrame2.middleFrame)
		self.goLeft.pack(side='right',fill='y',expand='yes')
		self.goLeft.button = tk.Button(self.goLeft,text="<-",command=self.leftButtonClick)
		self.goLeft.button.pack(side='right',fill='both',expand=True)


		# Picture Information
		self.pictureInfo = tk.Frame(self.outerFrame2)
		self.pictureInfo.pack(side='bottom',fill='x',expand='no')

		self.pictureInfo.picName = tk.Label(self.pictureInfo, text = "")
		self.pictureInfo.picName.pack(side='right',fill='y',expand=0,ipadx='100')


		self.pictureInfo.indexText = tk.Label(self.pictureInfo,text="")
		self.pictureInfo.indexText.pack(side='right',fill='y',expand=0,ipadx="100")


	"""
	Creates the preview for the adapt thresholding
	"""
	def adaptPreview(self):
		if (self.adapt.weighting.get() == "mean"):
			threshPic = cv2.adaptiveThreshold(self.img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,self.blockSize,5)
		else:
			threshPic = cv2.adaptiveThreshold(self.img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.blockSize,5)

		colorPic = np.zeros((2048,2048,4), dtype = 'uint8' )
		colorPic[:,:,0:1]=0
		colorPic[:,:,2] = threshPic
		colorPic[:,:,3] = 255
		threshPic = Image.fromarray(colorPic)
		threshPic.convert("RGBA")
		img = threshPic.resize((500,500), Image.ANTIALIAS)
		img = ImageTk.PhotoImage(img)
		self.threshPic = img
		self.pictureFrame.transPicture.configure(image=self.threshPic)


	"""
	Creates the preview for the manual thresholding
	"""
	def manuPreview(self):
		ret,threshPic = cv2.threshold(self.img,float(self.manuThresh),255,cv2.THRESH_BINARY)
		colorPic = np.zeros((2048,2048,4), dtype = 'uint8' )
		colorPic[:,:,0:1]=0
		colorPic[:,:,2] = threshPic
		colorPic[:,:,3] = 255
		threshPic = Image.fromarray(colorPic)
		threshPic.convert("RGBA")
		img = threshPic.resize((500,500), Image.ANTIALIAS)
		img = ImageTk.PhotoImage(img)
		self.threshPic = img
		self.pictureFrame.transPicture.configure(image=self.threshPic)
		self.loadHist()


	"""
	Validates that the radio button is clicked
	"""
	def validateAdaptRadio(self,*args):
		print "radio changed: ",self.adapt.weighting.get(),self.blockSize
		self.validateBlock(self.adaptBlockEntry.get())



	"""
	Checkes whether the user input for the adaptive thresholding is correct, enables buttton if it is
	"""
	def validateBlock(self,P):
		if(P==""):
			self.adapt.description.submit.config(state='disabled')
			self.adaptPreview.config(state='disabled')
			return True
		elif(not P.isdigit()):
			self.adapt.description.submit.config(state='disabled')
			self.adaptPreview.config(state='disabled')
			return True
		elif((int(P) % 2 == 1)  and (self.adapt.weighting.get() != "")):
			self.adapt.description.submit.config(state='normal')
			self.adaptPreview.config(state='normal')
			self.blockSize = int(P)
			print "weighting is: ------",self.adapt.weighting.get(),"------"
			return True
		else:
			self.adapt.description.submit.config(state='disabled')
			self.adaptPreview.config(state='disabled')
			return True


	"""
	Validates whether the user input for the manual input is correct. Dynamically controls submit button
	"""
	def validate(self,P):
		if(P == ""):
			self.manuThreshButton.config(state='disabled')
			self.manu.description.submit.config(state='disabled')
			return True
		elif(not P.isdigit()):
			self.manuThreshButton.config(state='disabled')
			self.manu.description.submit.config(state='disabled')
			return True
		elif(int(P)<256) and(int(P >= 0)):
			self.manuThreshButton.config(state='normal')
			self.manuThresh=P
			self.manu.description.submit.config(state='normal')
			return True
		else:
			self.manuThreshButton.config(state='disabled')
			self.manu.description.submit.config(state='disabled')
			return True


	"""
	Uses matplotlib to load the histogram depending on the manual threshold value that is set.
	"""
	def loadHist(self):
		self.plot.clear()
		self.plot.set_yticks([])
		self.plot.set_xticks([])
		self.plot.axvline(self.manuThresh, color='b',linestyle = 'solid', linewidth=2)
		self.plot.set_xlim(xmin=0,xmax=255)
		p = self.hist.gca()
		p.hist(self.img.ravel(), range=[0,255],bins=256,rwidth=1, color='gray')
		self.canvas.show()

	"""
	Loads the image from disk into memory
	"""
	def loadImageArray(self):
		index = self.index-1
		image = self.filePaths[index]
		img = cv2.imread(image,0)
		self.img = img

	"""
	Configures the left button to press left button
	"""
	def leftButton(self,event):
		index = self.index
		if( index == 1):
			index = index
		else:
			index = index-1
		self.index = index
		self.loadCurrentImage()


	"""
	Configures the right button to press right button
	"""
	def rightButton(self,event):
		index = self.index
		if(len(self.filePaths) == int(index)):
			index = int(index)
		else:
			index = int(index) + 1
		self.index = index
		self.loadCurrentImage()

	"""
	Configures the left button to click
	"""
	def leftButtonClick(self):
		index = self.index
		if( index == 1):
			index = index
		else:
			index = index-1
		self.index = index
		self.loadCurrentImage()


	"""
	Configures the right button to click
	"""
	def rightButtonClick(self):
		index = self.index
		if(len(self.filePaths) == int(index)):
			index = int(index)
		else:
			index = int(index) + 1
		self.index = index
		self.loadCurrentImage()

	"""
	Loads filename of the current image and displays it
	"""
	def loadPictureInfo(self):
		pictureName = self.filePaths[self.index-1]
		pictureName = pictureName.split(os.path.sep)[-1]
		self.pictureInfo.picName.configure(text=pictureName)

		indexText = str(self.index) + os.path.sep  + str(len(self.filePaths))
		self.pictureInfo.indexText.configure(text=indexText)


	"""
	Loads and displays the current image
	"""
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


	"""
	Gets the filepaths of all the TIF files in the chosen directory
	"""
	def loadImages(self):		
		self.filePaths = self.tifFiles
		self.index=1
		self.loadCurrentImage()
		
	"""
	Submits the adapt button. Saves the configurations, returns to the intro window.
	"""
	def adaptSubmit(self):
		Config.CFGadaptThresh = 1
		Config.CFGmanuThresh = 0
		self.thresholdWindow.destroy()
	
	"""
	Submits the manual button. Saves the configurations, returns to the intro window.
	"""
	def manuSubmit(self):
		Config.CFGmanuThresh = 1
		Config.CFGadaptThresh = 0
		self.thresholdWindow.destroy()

 ############################### Back to the main window code
		
	"""
	The checkbox for the thresholding row
	"""
	def threshFunction(self, event=None):
		if(self.threshCheck.get() == 1):
			self.threshImage.pack(in_=self.threshImageFrame)
			self.threshButton.configure(state="normal")
		else:
			self.threshImage.pack_forget()
			self.threshButton.configure(state="disabled")
			Config.CFGadaptThresh = 0
			Config.CFGmanuThresh = 0


	"""
	The checkbox for the 8-bit conversion row
	"""
	def bitFunction(self,event=None):
		print "Checkbox is: " + str(self.bitCheck.get())
		if(self.bitCheck.get() == 1):
			self.bitImage.pack(in_=self.bitImageFrame)
			Config.CFGbitConversion = 1
		else:
			self.bitImage.pack_forget()
			Config.CFGbitConversion = 0


	"""
	Allows users to choose a directory. Gets all the file paths of TIFF files in the directory and displays the count.
	"""
	def chooseDirectory(self):
		self.config.directory = askdirectory()

		files = os.listdir(self.config.directory)
		self.tifFiles = []

		regex = re.compile("\.tif|\.tiff",re.IGNORECASE)

		for file in files:
			if( regex.search(file) ):
					filePath = self.config.directory + os.path.sep + file
					self.tifFiles.append(filePath)

		self.dirLabel.configure(text=self.config.directory + "\n" + str(len(self.tifFiles)) + " TIF file(s) found")
		if (len(self.tifFiles) != 0):
			self.textureCheckBox.configure(state="normal")
			self.threshCheckBox.configure(state="normal")
			self.bitCheckBox.configure(state="normal")
			Config.CFGdirectory = 1
		else:
			self.textureCheckBox.deselect()
			self.threshCheckBox.deselect()
			self.bitCheckBox.deselect()
			self.textureCheckBox.configure(state="disabled")
			self.threshCheckBox.configure(state="disabled")
			self.bitCheckBox.configure(state="disabled")
			self.textureButton.configure(state="disabled")
			self.threshButton.configure(state="disabled")
			self.bitImage.pack_forget()
			self.threshImage.pack_forget()
			self.textureImage.pack_forget()
			Config.CFGdirectory = 0
			self.config = Config()


# Actually runs everything, calls the class above
root = tk.Tk()
app = Introduction(root)
app.myParent.title("Textures in HD")
root.mainloop()
