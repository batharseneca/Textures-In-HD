
class Config: 
   
    def __init__(self):
        Config.CFGdirectory = None
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
