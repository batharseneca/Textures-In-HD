from tkFileDialog import askdirectory
import Tkinter as tk
import ttk as ttk
import os
import tkMessageBox
from PIL import Image, ImageTk
import tkFont
import re


class Config:    
    def __init__(self):
          Config.CFGdirectory = 0
          Config.CFGbitConversion = 0
    
    def returnMethod(self):
        configArray = []
        configArray.append(Config.CFGdirectory)
        configArray.append(Config.CFGbitConversion)
        return configArray

class Introduction(Config):

     def __init__(self,parent):
          self.myParent = parent
          self.makeTemplate()
          self.config = Config()          
          

     def makeTemplate(self):
          # Outer parent frame (OuterFrame)
          self.outerFrame = tk.Frame(self.myParent,borderwidth=2, relief="ridge", width=1000, height=700)
          self.outerFrame.pack(expand=False)

          # self.outerFrame.pack_propagate(0)

          # Make a frame label for introduction
          self.infoFrame = tk.Frame(self.outerFrame)
          font = tkFont.Font(family="Helvetica", size=10)
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

     def runConfigure(self):
          directoryChoice, bitChoice = self.config.returnMethod()
          print "Directory Select? ", directoryChoice, "\n", "bitChoice Select? ", bitChoice, "\n"

     def textureConfigure(self):
          print "Hello"

     def textureFunction(self, event=None):
          if(self.textureCheck.get() == 1):
               self.textureImage.pack(in_=self.textureImageFrame)
               self.textureButton.configure(state="normal")
          else:
               self.textureImage.pack_forget()
               self.textureButton.configure(state="disabled")

     def threshConfigure(self):
          print "Hello"          

     def threshFunction(self, event=None):
          if(self.threshCheck.get() == 1):
               self.threshImage.pack(in_=self.threshImageFrame)
               self.threshButton.configure(state="normal")
          else:
               self.threshImage.pack_forget()
               self.threshButton.configure(state="disabled")

     def bitFunction(self,event=None):
          print "Checkbox is: " + str(self.bitCheck.get())
          if(self.bitCheck.get() == 1):
               self.bitImage.pack(in_=self.bitImageFrame)
               Config.CFGbitConversion = 1
          else:
               self.bitImage.pack_forget()
               Config.CFGbitConversion = 0


     def chooseDirectory(self):
          self.config.directory = askdirectory()

          files = os.listdir(self.config.directory)
          tifFiles = []

          regex = re.compile("\.tif|\.tiff",re.IGNORECASE)

          for file in files:
               if( regex.search(file) ):
                    tifFiles.append(file)

          self.dirLabel.configure(text=self.config.directory + "\n" + str(len(tifFiles)) + " TIF file(s) found")
          if (len(tifFiles) != 0):
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



root = tk.Tk()
app = Introduction(root)
app.myParent.title("Textures in HD")
root.mainloop()
