import Tkinter as tk
import re

from config import *

class TextureAnalysis():                
    def makeTemplateTexture(self,root):
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
 
