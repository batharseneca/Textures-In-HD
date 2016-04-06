#from colorama import init

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
        
        # Input Variables - Used to determine Output Files Necessary to Create #
        Config.bitO = 0
        Config.threshO = 0       
           
           
    def returnMethod(self):
        configArray = []
        configArray.append(Config.CFGdirectory)
        configArray.append(Config.CFGbitConversion)
        configArray.append(Config.CFGadaptThresh)
        configArray.append(Config.CFGmanuThresh)
        configArray.append(Config.CFGtextureAnalysis)       
        return configArray
     
     
    # def returnVars(self):
        # configVarsArray = []
        # configVarsArray.append(Config.AdaptiveBlockSize)
        # configVarsArray.append(Config.AdaptiveBlockSize)
        # configVarsArray.append(Config.AdaptiveBlockSize)
        

    
    #def saveProfile(self):    
