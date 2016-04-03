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



class Config: 
   
    def __init__(self):
        Config.CFGdirectory = 0
        Config.CFGbitConversion = 0
        Config.CFGadaptThresh = 0
        Config.CFGmanuThresh = 0
        Config.CFGtextureAnalysis = 0
        
        # Input Variables - Used to Characterize Profile Setting #
        Config.tifFiles = []
        Config.AdaptiveBlockSize = 0
        Config.AdaptWeighting = ""
        Config.ManuThresholdValue = 0 
        Config.TextureNeighborhoods = []
           
           
    def returnMethod(self):
        configArray = []
        configArray.append(Config.CFGdirectory)
        configArray.append(Config.CFGbitConversion)
        configArray.append(Config.CFGadaptThresh)
        configArray.append(Config.CFGmanuThresh)
        configArray.append(Config.CFGtextureAnalysis)       
        return configArray
     
     
    #def loadProfile(self):

    
    #def saveProfile(self):    
     
    
        
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
        self.runButton = tk.Button(self.runFrame, text="Run!", command=self.runConfigure)
        self.runButton.pack(side="right", padx=20, anchor="e")
        
    
# Methods of Introduction Class - To Enable All Settings Prior to leaving main window#  

    def bitFunction(self,event=None):        
        if(self.bitCheck.get() == 1):
            self.bitImage.pack(in_=self.bitImageFrame)
            Config.CFGbitConversion = 1
        else:
            self.bitImage.pack_forget()
            Config.CFGbitConversion = 0
    
    
    def threshFunction(self, event=None):
        if(self.threshCheck.get() == 1):
            self.threshImage.pack(in_=self.threshImageFrame)
            self.threshButton.configure(state="normal")
        else:
            self.threshImage.pack_forget()
            self.threshButton.configure(state="disabled")
            Config.CFGadaptThresh = 0
            Config.CFGmanuThresh = 0
    
           
    def textureFunction(self, event=None):
        if(self.textureCheck.get() == 1):
            self.textureImage.pack(in_=self.textureImageFrame)
            self.textureButton.configure(state="normal")
        else:
            self.textureImage.pack_forget()
            self.textureButton.configure(state="disabled")
            Config.CFGtextureAnalysis = 0

    
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
                
                
# Methods to launch Settings Windows #

    def textureConfigure(self):
        self.template = TextureAnalysis()
        self.template.makeTemplateTexture()
        
    def threshConfigure(self):
        self.template = ThresholdAnalysis()
        self.template.makeTemplateThresh()
                              
                
# Method to run Selected Settings from Main Window #
   
    def runConfigure(self):
        configArray = self.config.returnMethod()
        directoryChoice, bitChoice, adaptiveThresh, manuThresh, textureAnalysis = configArray
        print "Directory Select? ", directoryChoice, "\n", "bitChoice Select? ", bitChoice, "\n", "manual Thresholding Select? ", manuThresh, "\n", "adaptive Thresholding Select? ", adaptiveThresh, "\n", "Texture Analysis Select? ", textureAnalysis, "\n"
                
        checkArray = ['Directory', 'Bit Conversion', 'Adaptive Thresholding', 'Manual Thresholding', 'Texture Analysis']
        stepsArray = []
        for index in range (1,5):
            if configArray[index] == 1:
                stepsArray.append(checkArray[index]) 
        numofSteps = len(stepsArray)
      
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
            for image in self.tifFiles:
                # Updates Image Counter
                labelImageProcess = tk.Label(self.outerFrame4, text="Processing Image: " + str(imageCount) + " Of " + str(len(self.tifFiles)) + " Images" )
                # First Checks for BitCoversion Selection
                if (Config.CFGbitConversion == 1):
                    img = Image.open(image)
                    # If Image is not already 8 bit will convert
                    if processing.check8bitImage != "False":
                        img = processing.convertTo8bit(image)
                # Check if Adaptive or Manual Thresholding is Selected
                if (Config.CFGadaptThresh == 1):
                    # Updates Label to show Step 1 completed and thresholding commenced if Step 1 was Bit Coversion
                    if (stepsArray[0] == "Bit Conversion"):
                        label[stepsArray[0] + "a"].config(text='Completed')
                        label[stepsArray[1] + "a"].config(text='In Progress')
                    # If bitcoversion not selected img is not yet open! 
                    if (Config.CFGbitConversion == 0):
                        img = Image.open(image)
                    # Checks if Mean or Gaussian selected and performs thresholding
                    if (Config.AdaptWeighting == "mean" ):
                        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,Config.AdaptiveBlockSize,5)
                    else:
                        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,Config.AdaptiveBlockSize,5)
                elif (Config.CFGmanuThresh == 1):
                    # Updates Label to show Step 1 completed and thresholding commenced if Step 1 was Bit Coversion
                    if (stepsArray[0] == "Bit Conversion"):
                        label[stepsArray[0] + "a"].config(text='Completed')
                        label[stepsArray[1] + "a"].config(text='In Progress')
                    # If bitcoversion not selected img is not yet open!   
                    if (Config.CFGbitConversion == 0):
                        img = Image.open(image)
                    # Performs thresholding
                    ret,img = cv2.threshold(img,float(Config.ManuThresholdValue),255,cv2.THRESH_BINARY)
                # Check if Texture Analysis was selected
                if (Config.CFGtextureAnalysis = 1):
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
                        img = Image.open(image)
                    # Will save values into a row in a file named by filepath of dataset for each neighborhood size 
                    # ###### Would defintely be faster if all calculated and stored then file opened only once file IO is a heavy strain! ###### #
                    for nhood in Config.TextureNeighborhoods:
                        coMAT = processing.GLCM(img,nhood)
                        imageTextureFeature = processing.haralickALL(coMAT)
                        outputPath = self.config.directory.split("/")
                        filename = outputPath[-1]
                        filename = "Features" + filename
                        numpy.savetxt(filename, a, delimiter=",")
                # Resets Labels and updates Image Counter
                for counter in range (0,len(stepsArray)):
                    label[stepsArray[counter] + "a"].config(text='Pending')
                label[stepsArray[0] + "a"].config(text='In Progress')
                imageCount +=1              

                

class TextureAnalysis():                
    def makeTemplateTexture(self):
        self.textureWindow = tk.Toplevel(root)
        self.textureWindow.wm_title("Texture Analysis")
        self.textureWindow.grab_set()
        
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


        # REGEX GUIDELINE ROW ###
        self.guideline = tk.Frame(self.outerFrame3)
        self.guideline.pack(side='top',fill='x',expand=False)

        self.guideline.text = tk.Text(self.guideline,bg="lightgrey",height=10,bd=0, wrap='word')
        self.guideline.text.insert ('end',"\n      Guidelines:      \n\n 1) Seperate each entry with a comma\n 2) Do not end list with a comma"
                                    "\n 3) All enteries must be valid digits between 0-99\n 4) Do not use leading 0's e.x 09\n\n    Invalid Enteries will disable the Submit option")
        self.guideline.text.pack(side="left",fill='none',expand=False, padx=10, pady=10)
        self.guideline.text.configure(state='disabled')
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

    def OnClearClick(self):
        self.entryVariable.set("")

    def OnSubmitClick(self):
        input_string = self.entryVariable.get()
        self.input_array = [x.strip() for x in input_string.split(',')]
        Config.TextureNeighborhoods = self.input_array
        Config.CFGtextureAnalysis = 1
        self.textureWindow.destroy()        
 


class ThresholdAnalysis(): 
 
    def makeTemplateThresh(self):
        self.thresholdWindow = tk.Toplevel(root)
        self.thresholdWindow.wm_title("Image Thresholding")
        self.thresholdWindow.grab_set()
        
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
        
        self.loadImages()

        self.thresholdWindow.bind('<Left>', self.leftButton)
        self.thresholdWindow.bind('<Right>', self.rightButton)


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


    def validateAdaptRadio(self,*args):
        print "radio changed: ",self.adapt.weighting.get(),self.blockSize
        self.validateBlock(self.adaptBlockEntry.get())


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

    def loadHist(self):
        self.plot.clear()
        self.plot.set_yticks([])
        self.plot.set_xticks([])
        self.plot.axvline(self.manuThresh, color='b',linestyle = 'solid', linewidth=2)
        self.plot.set_xlim(xmin=0,xmax=255)
        p = self.hist.gca()
        p.hist(self.img.ravel(), range=[0,255],bins=256,rwidth=1, color='gray')
        self.canvas.show()

    def loadImageArray(self):
        index = self.index-1
        image = self.filePaths[index]
        img = cv2.imread(image,0)
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
        pictureName = pictureName.split(os.path.sep)[-1]
        self.pictureInfo.picName.configure(text=pictureName)
    
        indexText = str(self.index) + os.path.sep  + str(len(self.filePaths))
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
        self.filePaths = Config.tifFiles
        self.index=1
        self.loadCurrentImage()
          
    
    def adaptSubmit(self):
        Config.CFGadaptThresh = 1
        Config.CFGmanuThresh = 0
        Config.AdaptWeighting = self.adapt.weighting.get()
        Config.AdaptiveBlockSize = self.adaptBlockEntry.get()
        
        self.thresholdWindow.destroy()
          
    def manuSubmit(self):
        Config.CFGmanuThresh = 1
        Config.CFGadaptThresh = 0
        Config.ManuThresholdValue = self.manuThreshEntry.get()
        
        self.thresholdWindow.destroy() 
 



# All the Processing Code - Need to Ensure All Latest Versions Used # 
class ProcessingFunctions():

    def check8bitImage(image):
        if(image.dtype == np.dtype("uint8")):
            return True
        else:
            return False


            
    def convertTo8bit(image):	
        image = image.astype(np.uint8)
        return image
        
        
    
    def GLCM(Img,nhood):
        CoMatDim=(np.amax(Img)+1,np.amax(Img)+1) 
        CoMat=np.zeros(CoMatDim,dtype=np.int) #Initialize CoMat as matrix of zeros

        #First Direction
        ImgCopy1RowKeep=np.arange(nhood,Img.shape[0])
        ImgCopy2RowKeep=np.arange(0,Img.shape[0]-nhood)
        ImgCopy1=Img[ImgCopy1RowKeep,:]
        ImgCopy2=Img[ImgCopy2RowKeep,:]

        ImgCopy1ColKeep=np.arange(nhood,Img.shape[1])
        ImgCopy2ColKeep=np.arange(0,Img.shape[1]-nhood)
        ImgCopy1=ImgCopy1[:,ImgCopy1ColKeep]
        ImgCopy2=ImgCopy2[:,ImgCopy2ColKeep]

        ImgFlat1=np.ndarray.flatten(ImgCopy1)
        ImgFlat2=np.ndarray.flatten(ImgCopy2)


        for d in range(0,ImgFlat1.shape[0]):
            CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1

        #Second Direction
        ImgCopy1RowKeep=np.arange(nhood,Img.shape[0])
        ImgCopy2RowKeep=np.arange(0,Img.shape[0]-nhood)
        ImgCopy1=Img[ImgCopy1RowKeep,:]
        ImgCopy2=Img[ImgCopy2RowKeep,:]

        ImgFlat1=np.ndarray.flatten(ImgCopy1)
        ImgFlat2=np.ndarray.flatten(ImgCopy2)

        for d in range(0,ImgFlat1.shape[0]):
            CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1

        #Third Direction
        ImgCopy1RowKeep=np.arange(0,Img.shape[0]-nhood)
        ImgCopy2RowKeep=np.arange(nhood,Img.shape[0])
        ImgCopy1=Img[ImgCopy1RowKeep,:]
        ImgCopy2=Img[ImgCopy2RowKeep,:]

        ImgCopy1ColKeep=np.arange(nhood,Img.shape[1])
        ImgCopy2ColKeep=np.arange(0,Img.shape[1]-nhood)
        ImgCopy1=ImgCopy1[:,ImgCopy1ColKeep]
        ImgCopy2=ImgCopy2[:,ImgCopy2ColKeep]

        ImgFlat1=np.ndarray.flatten(ImgCopy1)
        ImgFlat2=np.ndarray.flatten(ImgCopy2)

        for d in range(0,ImgFlat1.shape[0]):
            CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1

        #Fourth Direction
        ImgCopy1ColKeep=np.arange(nhood,Img.shape[1])
        ImgCopy2ColKeep=np.arange(0,Img.shape[1]-nhood)
        ImgCopy1=Img[:,ImgCopy1ColKeep]
        ImgCopy2=Img[:,ImgCopy2ColKeep]

        ImgFlat1=np.ndarray.flatten(ImgCopy1)
        ImgFlat2=np.ndarray.flatten(ImgCopy2)

        for d in range(0,ImgFlat1.shape[0]):
            CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1

        CoMat = np.delete(CoMat,(0),axis=0)
        CoMat = np.delete(CoMat(0),axis=1) 		
        
        CoMat=np.divide(CoMat,np.sum(CoMat)) #Normalize CoMat#
        
        return(CoMat)
 
 
 
 
    def haralickALL(CoMat):
        np.array([
            ASM(CoMat),
            contrast(CoMat),
            IDM(CoMat),
            entropy(CoMat),
            xmean(CoMat),
            ymean(CoMat),
            xstdev(CoMat),
            ystdev(CoMat),
            CORR(CoMat),
            mean(CoMat),
            variance(CoMat),
            xPlusY(CoMat),
            sumAverage(CoMat),
            sumEntropy(CoMat),
            difEntropy(CoMat),
            inertia(CoMat),
            clusterShade(CoMat),
            clusterProm(CoMat),
        ])
        return np.array


    ## Angular Second Moment(ASM) / Energy is a measure of homogeneity in an image
    def ASM(CoMat):
        val=0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (CoMat[i][j])**2
        return val
	
    ## Contrast adds the comatrival, but favours when values are away from the diagonal
    def contrast(CoMat):
        val=0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (CoMat[i][j]) * (abs(i-j)**2)
        return val

    ## Local homogeneity (Inverse Difference Moment)
    def IDM(CoMat):
        val=0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (CoMat[i][j]) * 1/(1+(i-j)**2)
        return val
        
    ## Entropy (Log function had to have a +1 to ensure that values are not zero)
    def entropy(CoMat):
        val=0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (CoMat[i][j]) * mt.log(CoMat[i][j]+1)
        return val * (-1)

    ## Horizontal Mean
    def xmean(CoMat):
        val = 0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += i * CoMat[i][j]
        return val

    ## Vertical Mean
    def ymean(CoMat):
        val = 0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += j * CoMat[i][j]
        return val

    ## Horizontal Standard Deviation
    def xstdev(CoMat):
        val = 0
        xmeanVal = xmean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += ((i-xmeanVal)**2) * CoMat[i][j]
        return val	
            
    # Vertical Standard Deviation	
    def ystdev(CoMat):
        val = 0
        ymeanVal = ymean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += ((j-ymeanVal)**2) * CoMat[i][j]
        return val

    ## The actual correlation function, requires the above calculations
    def CORR(CoMat):
        val = 0
        xmeanVal = xmean(CoMat)
        ymeanVal = ymean(CoMat)
        
        xStdVal = xstdev(CoMat)
        yStdVal = ystdev(CoMat)
        
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += ((i*j) * CoMat[i][j] - (xmeanVal-ymeanVal))/(xStdVal*yStdVal)
        return val	

    # Total Mean
    def mean(CoMat):
        val = 0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += CoMat[i][j]
        num = CoMat.shape[0] * CoMat.shape[1]
        mean = val / num
        return mean

    # Sum of Squares, Variance
    def variance(CoMat):
        val = 0
        meanVal = mean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (i-meanVal)**2 * CoMat[i][j]
        return val

    # P(x+y) is the diagonal sum of the matrix.
    def xPlusY(CoMat,kValue):
        val = 0
        if(kValue < CoMat.shape[0]):
            i=kValue
            j=0
            while(i!=0):
                val += CoMat[i][j]
                i -= 1
                j += 1
            return val
        if(kValue >= CoMat.shape[0]):
            i=CoMat.shape[0]-1
            j= kValue - CoMat.shape[0]-1
            while(j != CoMat.shape[0]):
                val += CoMat[i][j]
                i -= 1
                j += 1
            return val

    # Sum Average	
    def sumAverage(CoMat):
        val = 0
        for k in range(0,CoMat.shape[0]*2-2):
            val += xPlusY(CoMat,k) * k
        return val

    # Sum Entropy (Log function had to have a +1 to ensure that values are not zero)
    def sumEntropy(CoMat):
        val = 0
        for k in range(0,CoMat.shape[0]*2-2):
            val += xPlusY(CoMat,k)* mt.log(xPlusY(CoMat,k)+1)
        return val*(-1)
        
    # Differencce Entropy (Log function had to have a +1 to ensure that values are not zero)
    def difEntropy(CoMat):
        val = 0
        for k in range(0,CoMat.shape[0]-1):
            val += xPlusY(CoMat,k)* mt.log(xPlusY(CoMat,k)+1)
        return val*(-1)

    # Inertia
    def inertia(CoMat):
        val = 0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += ((i-j)**2) * CoMat[i][j]
        return val
       
    # Cluster Shade
    def clusterShade(CoMat):
        val = 0
        ux = xmean(CoMat)
        uy = ymean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (i + j - ux - uy)**3 * CoMat[i][j]
        return val        

    # Cluster Prominance
    def clusterProm(CoMat):
        val = 0
        ux = xmean(CoMat)
        uy = ymean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (i + j - ux - uy)**4 * CoMat[i][j]
        return val
    
 
 
 
 
root = tk.Tk()
app = Introduction(root)
app.myParent.title("Textures in HD")
root.mainloop()        
        
        
        
        
        
        

        