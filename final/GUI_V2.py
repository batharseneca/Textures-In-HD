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
from tqdm import tqdm
import time


## Import our classes!!
from config import Config
from texture import TextureAnalysis
from threshold import ThresholdAnalysis
from process import ProcessingFunctions

        
class Introduction(Config):

    def __init__(self,parent):
        self.myParent = parent
        self.makeTemplate()
        self.config = Config()          
          

    def makeTemplate(self):
        # Outer parent frame (OuterFrame)
        self.outerFrame = tk.Frame(self.myParent,borderwidth=2, relief="ridge", width=1000, height=700)
        self.outerFrame.pack(expand=False)
      

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
        infoLabel.pack(side="top", expand=0, fill="none")

        
# Choosing Directory Setup #
        self.dirFrame = tk.Frame(self.outerFrame)
        self.dirFrame.pack(side="top",expand=1, fill="x", pady=[0,20])
        self.dirButton = tk.Button(self.dirFrame, text="Choose Picture Directory", command=self.chooseDirectory)
        self.dirButton.pack(side="top",expand=1, fill="none")
        # Make a label to display directory location for user
        self.dirLabel = tk.Label(self.dirFrame, text="")
        self.dirLabel.pack(side="top")
        
        
# Divider Line #
        tk.Frame(self.outerFrame, relief="solid", borderwidth=2, bg="darkgrey").pack(side="top", fill="x")       
        
        
        # Convert to bit section #
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
    
        
# Thresholding section #
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
    
    
# Texture Analysis Section #
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
    
    
# Divider Line #
        tk.Frame(self.outerFrame, relief="sunken", borderwidth=1, bg="black").pack(side="top", fill="x")
    

# Creates a run button #
        self.runFrame = tk.Frame(self.outerFrame)
        self.runFrame.pack(fill="x", pady=20)        
               
        self.runButton = tk.Button(self.runFrame, text="Run!", width=20, command=self.runConfigure)
        self.runButton.pack(side="right", padx=20, expand=1, anchor="e")
        
        self.savefileLabel = tk.Label(self.runFrame, text="Please Select the Analysis Steps From Which You Wish To Retain Data Files: ")
        self.savefileLabel.pack(side="left", padx=20, expand=1, anchor="w")
        
        self.bitOutput = tk.IntVar()
        self.bitOutputCK = tk.Checkbutton(self.runFrame, text="Bit Coversion", variable=self.bitOutput, command=self.bitOutputFunction, padx=10)
        self.bitOutputCK.configure(state="disabled")
        self.bitOutputCK.pack(side="left",expand=1, fill="none", anchor="w")
        
        self.thresholdOutput = tk.IntVar()
        self.thresholdOutputCK = tk.Checkbutton(self.runFrame, text="Thresholding", variable=self.thresholdOutput, command=self.thresholdOutputFunction, padx=10)
        self.thresholdOutputCK.configure(state="disabled")
        self.thresholdOutputCK.pack(side="left",expand=1, fill="none", anchor="w")
        
        self.textureOutput = tk.IntVar()
        self.textureOutputCK = tk.Checkbutton(self.runFrame, text="Texture Analysis", variable=self.textureOutput, padx=10)
        self.textureOutputCK.configure(state="disabled")
        self.textureOutputCK.pack(side="left",expand=1, fill="none", anchor="w")
        
    
# Methods of Introduction Class - To Enable All Settings Prior to leaving main window#  

    def bitFunction(self,event=None):        
        if(self.bitCheck.get() == 1):
            self.bitImage.pack(in_=self.bitImageFrame)
            Config.CFGbitConversion = 1
            self.bitOutputCK.configure(state="normal")
        else:
            self.bitImage.pack_forget()
            Config.CFGbitConversion = 0
            self.bitOutputCK.deselect()
            self.bitOutputCK.configure(state="disabled")
            Config.bitO = 0
    
    
    def threshFunction(self, event=None):
        if(self.threshCheck.get() == 1):
            self.threshImage.pack(in_=self.threshImageFrame)
            self.threshButton.configure(state="normal")
            self.thresholdOutputCK.configure(state="normal")
            
        else:
            self.threshImage.pack_forget()
            self.threshButton.configure(state="disabled")
            Config.CFGadaptThresh = 0
            Config.CFGmanuThresh = 0
            self.thresholdOutputCK.deselect()
            self.thresholdOutputCK.configure(state="disabled")
            Config.threshO = 0
    
           
    def textureFunction(self, event=None):
        if(self.textureCheck.get() == 1):
            self.textureImage.pack(in_=self.textureImageFrame)
            self.textureButton.configure(state="normal")
            self.textureOutputCK.configure(state="normal")
            self.textureOutputCK.select()
            self.textureOutputCK.configure(state="disabled")
        else:
            self.textureImage.pack_forget()
            self.textureButton.configure(state="disabled")
            Config.CFGtextureAnalysis = 0
            self.textureOutputCK.deselect()
            self.textureOutputCK.configure(state="disabled")

    
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
	    Config.tifFiles = self.tifFiles
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
        
    def bitOutputFunction(self,event=None):        
        if(self.bitOutput.get() == 1):
            Config.bitO = 1            
        else:
            Config.bitO = 0
    
    
    def thresholdOutputFunction(self, event=None):
        if(self.thresholdOutput.get() == 1):
            Config.threshO = 1
        else:
            Config.threshO = 0
      
                
# Methods to launch Settings Windows #

    def textureConfigure(self):
        self.template = TextureAnalysis()
        self.template.makeTemplateTexture(root)
        
    def threshConfigure(self):
        self.template = ThresholdAnalysis()
        self.template.makeTemplateThresh(root)
                              
                
# Method to run Selected Settings from Main Window #
   
    def runConfigure(self):
        configArray = self.config.returnMethod()
        directoryChoice, bitChoice, adaptiveThresh, manuThresh, textureAnalysis = configArray
        print "Directory Select? ", directoryChoice, "\n", "bitChoice Select? ", bitChoice, "\n", "manual Thresholding Select? ", manuThresh, "\n", "adaptive Thresholding Select? ", adaptiveThresh, "\n", "Texture Analysis Select? ", textureAnalysis, "\n"
        print "Neighborhood Size: ", Config.TextureNeighborhoods
        print "bitO: ", Config.bitO
        print "threshO: ", Config.threshO
        checkArray = ['Directory', 'Bit Conversion', 'Adaptive Thresholding', 'Manual Thresholding', 'Texture Analysis']
        stepsArray = []
        for index in range (1,5):
            if configArray[index] == 1:
                stepsArray.append(checkArray[index]) 
        numofSteps = len(stepsArray)
      
        if (directoryChoice == 0):
            tkMessageBox.showwarning("Warning - Invalid Parameters", "No Input Image Set Detected")    
        elif ( (Config.threshO == 1) and (Config.CFGadaptThresh == 0 and Config.CFGmanuThresh == 0) ):
            tkMessageBox.showwarning("Warning - Invalid Settings", "Thresholding Parameters Must Be Configured If Selected")
        elif ( (self.textureOutput.get() == 1) and (Config.CFGtextureAnalysis == 0) ):
            tkMessageBox.showwarning("Warning - Invalid Settings", "Texture Analysis Parameters Must Be Configured If Selected")
        elif (Config.CFGbitConversion == 0 and Config.CFGadaptThresh == 0 and Config.CFGmanuThresh == 0 and Config.CFGtextureAnalysis == 0):
            tkMessageBox.showwarning("Warning - Invalid Parameters", "No Analysis Options Specified or Configured!")
        elif (Config.bitO == 0 and Config.threshO == 0 and self.textureOutput.get() == 0):
            tkMessageBox.showwarning("Warning - Invalid Parameters", "No Output Files Specified")
        
        else:            
            self.myParent.withdraw()
            self.runWindow = tk.Toplevel(root)
            self.runWindow.wm_title("Data Analysis in Progress")        
            self.outerFrame4 = tk.Frame(self.runWindow, borderwidth=2, relief="ridge", width=400, height=400)
            self.outerFrame4.pack(padx=20,pady=20)
            imageCount = 1
            labelImageProcess = tk.Label(self.outerFrame4, text="Processing Image: " + str(imageCount) + " Of " + str(len(self.tifFiles)) + " Images" )
            labelImageProcess.grid(row=0, column =0, padx=20, pady=10, sticky="wens")
            label = {}
            h=1
            for step in stepsArray:
                lb = tk.Label(self.outerFrame4, text="Step " + str((stepsArray.index(step) + 1)) + ": " + step)
                lb.grid(row=h, column =0, padx=10, pady=5, sticky="w")
                label[step] = lb           
                lb2 = tk.Label(self.outerFrame4, text="Pending")
                lb2.grid(row=h, column=1, padx=10, pady=5, sticky="w")
                label[step + "a"] = lb2     
                h +=1
            label[stepsArray[0] + "a"].config(text='In Progress')
            
# Main Processing Code # - ADDITIONAL NOTE : IF at any time something is the only step or last step its easy to check by checking if stepsArray[-1] = w.e you are doing!!!!!
            
            proccessing = ProcessingFunctions()
            for image in tqdm(self.tifFiles):
                # Updates Image Counter
                labelImageProcess.config(text="Processing Image: " + str(imageCount) + " Of " + str(len(self.tifFiles)) + " Images")
                # First Checks for BitCoversion Selection
                if (Config.CFGbitConversion == 1):
                    img = cv2.imread(image,0)
                    # If Image is not already 8 bit will convert
                    if proccessing.check8bitImage(img) != "False":
                        img = proccessing.convertTo8bit(img)                    
                        
                        if (Config.bitO == 1):
                            date = time.strftime("%d_%m_%Y")    
                            filepath = os.path.dirname(os.path.abspath(__file__))
                            
                            imageName = image.replace("/","*")
                            imageName = imageName.replace("\\","*")                        
                            name_Array = imageName.split("*")
                            imageName = name_Array[-1]
                            
                            filepath = filepath + os.path.sep + "8BIT_Converted_Images" + os.path.sep + date + "_8BIT_" 
                            try: 
                                os.makedirs(filepath)
                            except OSError:
                                if not os.path.isdir(filepath):
                                    raise
                            print imageName
                            cv2.imwrite(os.path.join(filepath, imageName), img)
                    
                # Check if Adaptive or Manual Thresholding is Selected
                if (Config.CFGadaptThresh == 1):
                    # Updates Label to show Step 1 completed and thresholding commenced if Step 1 was Bit Coversion
                    if (stepsArray[0] == "Bit Conversion"):
                        label[stepsArray[0] + "a"].config(text='Completed')
                        label[stepsArray[1] + "a"].config(text='In Progress')
                    # If bitcoversion not selected img is not yet open! 
                    if (Config.CFGbitConversion == 0):
                        img = cv2.imread(image,0)
                    # Checks if Mean or Gaussian selected and performs thresholding
                    if (Config.AdaptWeighting == "mean" ):
                        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,int(Config.AdaptiveBlockSize),5)
                    else:
                        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,int(Config.AdaptiveBlockSize),5)
                        
                    
                    if (Config.threshO == 1): 
                        date = time.strftime("%d_%m_%Y")
                        filepath = os.path.dirname(os.path.abspath(__file__))
                        
                        imageName = image.replace("/","*")
                        imageName = imageName.replace("\\","*")                        
                        name_Array = imageName.split("*")
                        imageName = name_Array[-1]
                       
                        
                        filepath = filepath + os.path.sep + "Thresholded_Images" + os.path.sep + date + "_Adaptive_" + str(Config.AdaptWeighting) + "_" + str(Config.AdaptiveBlockSize)
                        try: 
                            os.makedirs(filepath)
                        except OSError:
                            if not os.path.isdir(filepath):
                                raise                        
                        cv2.imwrite(os.path.join(filepath, imageName), img)
                    
                    
                elif (Config.CFGmanuThresh == 1):
                    # Updates Label to show Step 1 completed and thresholding commenced if Step 1 was Bit Coversion
                    if (stepsArray[0] == "Bit Conversion"):
                        label[stepsArray[0] + "a"].config(text='Completed')
                        label[stepsArray[1] + "a"].config(text='In Progress')
                    # If bitcoversion not selected img is not yet open!   
                    if (Config.CFGbitConversion == 0):
                        img = cv2.imread(image,0)
                    # Performs thresholding
                    ret,img = cv2.threshold(img,float(Config.ManuThresholdValue),255,cv2.THRESH_BINARY)
                    
                    
                    if (Config.threshO == 1): 
                        date = time.strftime("%d_%m_%Y")
                        filepath = os.path.dirname(os.path.abspath(__file__))
                        
                        imageName = image.replace("/","*")
                        imageName = imageName.replace("\\","*")                        
                        name_Array = imageName.split("*")
                        imageName = name_Array[-1]
                                                
                        filepath = filepath + os.path.sep + "Thresholded_Images" + os.path.sep + date + "_Manual_" + str(Config.ManuThresholdValue) 
                        try: 
                            os.makedirs(filepath)
                        except OSError:
                            if not os.path.isdir(filepath):
                                raise                        
                        cv2.imwrite(os.path.join(filepath, imageName), img)
                                            
                    
                # Check if Texture Analysis was selected
                if (Config.CFGtextureAnalysis == 1):
                    # Updates Labels
                    if (stepsArray[0] == "Manual Thresholding" or stepsArray[0] == "Adaptive Thresholding"):
                        label[stepsArray[0] + "a"].config(text='Completed')
                        label[stepsArray[1] + "a"].config(text='In Progress')
                    if (stepsArray[0] == "Bit Conversion"):                        
                        if (stepsArray[1] == "Manual Thresholding" or stepsArray[1] == "Adaptive Thresholding"):
                            label[stepsArray[1] + "a"].config(text='Completed')
                            label[stepsArray[2] + "a"].config(text='In Progress')
                        else:
                            label[stepsArray[0] + "a"].config(text='Completed')
                            label[stepsArray[1] + "a"].config(text='In Progress')                 
                    # If nothing was done previously image is not yet open!   
                    if (Config.CFGbitConversion == 0 and Config.CFGadaptThresh == 0 and Config.CFGmanuThresh == 0):
                        img = cv2.imread(image,0)
                    # Will save values into a row in a file named by filepath of dataset for each neighborhood size 
                    # ###### Would defintely be faster if all calculated and stored then file opened only once file IO is a heavy strain! ###### #
                    for nhood in Config.TextureNeighborhoods:
                        coMAT = proccessing.GLCM(img,int(nhood))                                               
                        imageTextureFeature = proccessing.haralickALL(coMAT)
 #                      #print imageTextureFeature
                        outputPath = self.config.directory.split("/")
                        if (outputPath == self.config.directory):
                            outputPath = self.config.directory.split("\\")
                        filename = outputPath[-1]
                        date = time.strftime("%d_%m_%Y")
                        filename = date + "_" + filename + ".csv"   
                        f = open(filename, 'a')                                        
                        imageName = image                        
                        name_Array = imageName.split("/")
                        if (name_Array == imageName):
                            name_Array = imageName.split("\\")
                        imageName = name_Array[-1]   
                        imageName = imageName + "_nhood_" + nhood
                        for features in imageTextureFeature:
                            modFeature = str(features)
                            imageTextureFeature[imageTextureFeature.index(features)] = modFeature                            
                        imageTextureFeature = [imageName] + imageTextureFeature 
                        f.write(",".join(imageTextureFeature) + "\n")
                        f.close                        
                # Resets Labels and updates Image Counter
                for counter in range (0,len(stepsArray)):
                    label[stepsArray[counter] + "a"].config(text='Pending')
                label[stepsArray[0] + "a"].config(text='In Progress')
                imageCount +=1
            #Testing in STDOUT
            print "TASK IS DONE!"
            for counter in range (0,len(stepsArray)):
                label[stepsArray[counter] + "a"].config(text='Completed')
            self.myParent.deiconify()
            self.runWindow.destroy()

 
 
 
 
root = tk.Tk()
app = Introduction(root)
app.myParent.title("Textures in HD")
root.mainloop()        
