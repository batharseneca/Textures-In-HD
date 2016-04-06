

class Config:    
    
    def __init__(self):
        
        self.CFGdirectory = 0
        self.CFGbitConversion = 0
        self.CFGadaptThresh = 0
        self.CFGmanuThresh = 0
        self.CFGtextureAnalysis = 0                 
        
        # Input Variables - Used to Characterize Profile Setting #
        self.tifFiles = []
        self.AdaptiveBlockSize = 0
        self.AdaptWeighting = ""
        self.ManuThresholdValue = 0 
        self.TextureNeighborhoods = []
        
        # Input Variables - Used to determine Output Files Necessary to Create #
        self.bitO = 0
        self.threshO = 0                  
           
    def returnMethod(self):
        self.configArray = []
        self.configArray.append(self.CFGdirectory)
        self.configArray.append(self.CFGbitConversion)
        self.configArray.append(self.CFGadaptThresh)
        self.configArray.append(self.CFGmanuThresh)
        self.configArray.append(self.CFGtextureAnalysis)       
        return self.configArray
     
 
