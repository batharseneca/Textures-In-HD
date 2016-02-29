import re
import os


def formatHoechst(filename,dir1):
	
	nuc_filepath = dir1 + "/" + filename
	
	p = re.compile(r"""
	
^(q\d\d)	# Captures the group type

(.+)xy		# Captures the treatment

(\d\d)		# captures the number

c2		# matches c2

\.tif		# matches the .tif file

""",re.X);
	
	
		
	match = p.search(filename)	
	
	if(match):
		cellType = match.group(1)
		treatment = match.group(2)
		trialNum = match.group(3)
		if(treatment[-1:] == "_"):
			treatment = treatment[0:-1]
	else:
		return "FAILED TO FIND items: " + filename
	
	output = [nuc_filepath, cellType, treatment, trialNum]
	return output
	
def getP53(info,dir2):
	
	regex = r"^" +  re.escape(info[1]) + re.escape(info[2]) + r"_" + re.escape(info[3])
	

	p53Dir = os.listdir(dir2)
	
	for i in range(2, len(p53Dir)):
		match = re.search(regex, p53Dir[i])
		if(match):
			output = dir2 + "/" + p53Dir[i]
			break
		else:
			output = "FAILED"
	info.append(output)
	return info

hoechstDir = os.listdir("/home/nmerwin/Documents/IGPProject/data/hoechst")
p53Dir = os.listdir("/home/nmerwin/Documents/IGPProject/data/p-p53")

dir1 = "/home/nmerwin/Documents/IGPProject/data/hoechst"
dir2 = "/home/nmerwin/Documents/IGPProject/data/p-p53"


row = []
for i in range(2,len(hoechstDir)):
	templatePath = "/home/nmerwin/Documents/IGPProject/data/hoechst/" +  hoechstDir[i]
	p53Path = "/home/nmerwin/Documents/IGPProject/data/p-p53/" + p53Dir[i]	
	start = formatHoechst(hoechstDir[i],dir1)
	info = getP53(start, dir2)
	row.append(','.join(info))
	
f = open("formatting.csv","w")

for i in range(0,len(row)):
	f.write(row[i] + "\n")
f.close
		
	#print templatePath
	#print p53Path



	



