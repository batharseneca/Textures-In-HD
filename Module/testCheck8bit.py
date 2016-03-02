import scipy as sp
import scipy.misc

import os

from functions import check8bit

f = open("/home/nmerwin/Documents/IGPProject/ImageAnalysis-IGP/dataMunging/formatting.csv","r")

out = open("./8bit.csv","w")


for line in f:
	lineArray = line.rstrip().split(",");
	print lineArray
	
	template = sp.misc.imread(lineArray[0])	
	p53 = sp.misc.imread(lineArray[4])
	
	if(check8bit.check8bitImage(template) != True):
		template = check8bit.convertTo8bit(template)	
	
	print check8bit.check8bitImage(template)
	
	name = lineArray[0]
	
	picturePath = name.split("/")[0:-2]
	
	picturePath = "/".join(picturePath)
	
	print "Picture path is: " + picturePath	

	name =  picturePath + "/8bitTemplate/"  + name.split("/")[-1]
	
	print name	
	
	filename = name
	if not os.path.exists(os.path.dirname(filename)):
	    try:
		os.makedirs(os.path.dirname(filename))
	    except OSError as exc: # Guard against race condition
		if exc.errno != errno.EEXIST:
		    raise
	with open(filename, "w") as f:
	    sp.misc.imsave(name,template)
	
	lineArray.append(name)

	out.write(",".join(lineArray) + "\n")
	
	print ",".join(lineArray)
