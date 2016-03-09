from Tkinter import *
import Tkinter as tk
import ttk as ttk
import Tkinter
import re
#from GLCMv3 import GLCM

NORM_FONT= ("Verdana", 10)
LARGE_FONT= ("Arial", 14)

class matrix_Menu(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.outerFrame = tk.Frame(self.parent,borderwidth=2, relief="ridge", width=100, height=400)
        self.outerFrame.pack(padx=20,pady=20)

        # INSTRUCTIONS ROW ####
        self.instructions = tk.Frame(self.outerFrame)
        self.instructions.pack(side='top',fill='x',expand=False)

        self.instructions.text = tk.Text(self.instructions,bg="lightgrey",height=3,bd=0, wrap='word')
        self.instructions.text.insert ('end',"In the following Textbox please input the neighborhood values you would like to see the IGLCM constructed around. Please format the values as a list of numbers seperated by ',' e.g 1,2,3")
        self.instructions.text.pack(side="left",fill='none',expand=False, padx=10, pady=10)

        # INPUT ROW ###
        self.inputbox = tk.Frame(self.outerFrame)
        self.inputbox.pack(side='top',fill='x',expand=False)

        self.entryVariable = Tkinter.StringVar()
        checkSizes = self.outerFrame.register(self.validate)
        self.entry = Tkinter.Entry(self.inputbox, textvariable=self.entryVariable, validate='key', validatecommand=(checkSizes, '%P'))
        self.entry.pack(side='left',padx=100, pady=10)

        self.clearInput = tk.Button(self.inputbox, text="Clear Values",font=NORM_FONT,state='disabled',command=self.OnClearClick)
        self.clearInput.pack(side='left', fill='x', expand=True)

        self.submitInput = tk.Button(self.inputbox, text="Submit", font=NORM_FONT, state='disabled', command=self.OnSubmitClick)
        self.submitInput.pack(side='left', padx=50, fill='x', expand=True)


        # REGEX GUIDELINE ROW ###
        self.guideline = tk.Frame(self.outerFrame)
        self.guideline.pack(side='top',fill='x',expand=False)

        self.guideline.text = tk.Text(self.guideline,bg="lightgrey",height=10,bd=0, wrap='word')
        self.guideline.text.insert ('end',"\n      Guidelines:      \n\n 1) Seperate each entry with a comma\n 2) Do not end list with a comma"
                                    "\n 3) All entries must be valid digits between 0-99\n 4) Do not use leading 0's ex. 09\n\n    Invalid Entries will disable the Submit option")
        self.guideline.text.pack(side="left",fill='none',expand=False, padx=10, pady=10)

    def validate(self,P):
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
        input_array = [x.strip() for x in input_string.split(',')]
        self.loadImages()
        indexfiles = 0
        indexvalues = 0


     #   while indexvalues < len(input_array):
      #      while indexfiles < len(self.filePaths):



     #   image = self.filePaths[index]
     #  img = Image.open(image)


    #def loadImages(self):
		#filename = askdirectory()
		#if(os.path.isdir(filename) == False):
		#	tkMessageBox.showerror("Not a directory", filename.split(os.path.sep)[-1] + " is not a directory.")
		#	exit()
		#files = os.listdir(filename)
		#tifFiles = []
		#for file in files:
		#	if( (file[-4:] == ".tif") or (file[-5:] == ".tiff") ):
		#		filePath = filename + os.path.sep + file
		#		tifFiles.append(filePath)
		#if(len(tifFiles) == 0):
		#	tkMessageBox.showerror("No pictures found", "There were no TIF files found in this directory")
		#	exit()
		#self.filePaths = tifFiles



        #print input_array
       # self.entryVariable.set(input_string)
   #     self.popupmsg("You are about to proceed with your Input")

   # def popupmsg(self, msg):
   #     popup = tk.Tk()
   #     popup.wm_title("Submission Alert")
   #     label = ttk.Label(popup, text=msg, font=NORM_FONT)
   #     label.pack(side="top", fill="x", pady=10)
   #     B1 = ttk.Button(popup, text=self.entryVariable, command = popup.destroy)
   #     B1.pack(side='left')
   #     B2 = ttk.Button(popup, text="Not Okay", command = popup.destroy)
   #     B2.pack(side='right')
   #     popup.mainloop()

app = matrix_Menu(None)
app.title('Constructing IGLCM')
app.mainloop()
