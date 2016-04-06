import Tkinter as tk
import numpy as np
import cv2
import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import tkMessageBox
from PIL import Image, ImageTk
import tkFont
import re


class ThresholdAnalysis(): 

    def __init__(self, root, config):
        
        self.config = config
        self.makeTemplateThresh(root)
        
 
    def makeTemplateThresh(self, root):
        
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
        self.filePaths = self.config.tifFiles
        self.index=1
        self.loadCurrentImage()
          
    
    def adaptSubmit(self):
        self.config.CFGadaptThresh = 1
        self.config.CFGmanuThresh = 0
        self.config.AdaptWeighting = self.adapt.weighting.get()
        self.config.AdaptiveBlockSize = self.adaptBlockEntry.get()
        
        self.thresholdWindow.destroy()
          
    def manuSubmit(self):
        self.config.CFGmanuThresh = 1
        self.config.CFGadaptThresh = 0
        self.config.ManuThresholdValue = self.manuThreshEntry.get()
        
        self.thresholdWindow.destroy() 
