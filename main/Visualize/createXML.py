import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import xml.etree.ElementTree as ET # Creating an XML file
from xml.dom import minidom # Formatting the XML file
import sys,os
from shapely.geometry import Polygon
from shapely.ops import cascaded_union,polygonize


def takeInputs(csvfile,grid_size):
	data = pd.read_csv(csvfile)
	fname = []
	truths = []
	for i in range(len(data)):
		fname.append(data['filename'][i][-28:])
		condition = 'TruePositive'
		if(condition in data):
			if(data['TruePositive'][i]==1):
				truths.append(2)
			elif(data['TrueNegative'][i]==1):
				truths.append(3)
			elif(data['FalsePositive'][i]==1):
				truths.append(4)
			elif(data['FalseNegative'][i]==1):
				truths.append(5)
			elif(data['prediction'][i]==0):
				truths.append(0)
			elif(data['prediction'][i]==1):
				truths.append(1)
		else:
			if(data['prediction'][i]==0):
				truths.append(0)
			elif(data['prediction'][i]==1):
				truths.append(1)
	values = []
	for f in fname:
		x = ""
		y = ""
		a = ""
		b = ""
		for i in range(len(f)-2):
			if(f[i]+f[i-1]=="x-"):
				k =i+1
				for i in range(k,len(f)):
					if(f[i]=='-'):
						break
					else:
						x+=f[i]
			if(f[i]+f[i-1]=="y-"):
				k=i+1
				for i in range(k,len(f)):
					if(f[i]=='-'):
						break
					else:
						y+=f[i]
		if(x!="" and y!=""):
			x = int(x) # Row value
			y = int(y) # Coloumn value
			values.append([a,b,x,y])   
	final = []
	j=0	
	for i in range(len(values)):
		temp = []
		grid_size = 256
		actual_x = values[i][2]+grid_size
		actual_y = values[i][3]
		temp.append([actual_x,actual_y])
		temp.append([actual_x-grid_size,actual_y])
		temp.append([actual_x-grid_size,actual_y+grid_size])
		temp.append([actual_x,actual_y+grid_size])        
		temp.append(truths[i])
		final.append(temp)
	return final

def makeAnnotation(final, dest, num):
	"""
		Creating annotations for the XML file
		Args:
			A 2-D array containing the list of tiles to be written into an XML file
			The file path for the XML file
			Denotes the different number of annotations required based of an input i.e
				3 - txt
				4 - CSV
		Returns:
			void
			This method creates an XML file and writes the required annotations from the inputs
	"""

	root = ET.Element("Annotations")
	root.set("MicronsPerPixel","0.500000")

	for j in range(num):
		a1 = ET.Element("Annotation")
		a1.set("Id", str(j+1))
		a1.set("Name","")
		a1.set("ReadOnly","0")
		a1.set("NameReadOnly","0")
		a1.set("LineColorReadOnly","0")
		a1.set("Incremental","0")
		a1.set("Type","6")
			 
		if(j==0):
			a1.set("LineColor","65280")  #green colour
		elif(j==1):
			a1.set("LineColor","255")    #red colour
		elif(j==2):
			a1.set("LineColor","16744448")  #True Positive
		elif(j==3):
			a1.set("LineColor","16776960")  #True Negative
		elif(j==4):
			a1.set("LineColor","65535") #yellow #False Possitive
		elif(j==5):
			a1.set("LineColor","4194368") #black #False -ve

		a1.set("Visible","1")
		a1.set("Selected","1")
		a1.set("MarkupImagePath","")
		a1.set("MacroName","")
		root.append(a1)

		b1 = ET.SubElement(a1,"Attributes")
		b2 = ET.SubElement(b1,"Attribute",{"Name":"Description","Id":"0","Value":"",})

		r1 = ET.SubElement(a1,"Regions")
		r2 = ET.SubElement(r1,"RegionAttributeHeaders")
		r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"9999","Name":"Region","ColumnWidth":"-1",})
		r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"9997","Name":"Length","ColumnWidth":"-1",})
		r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"9996","Name":"Area","ColumnWidth":"-1",})
		r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"9998","Name":"Text","ColumnWidth":"-1",})
		r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"1","Name":"Description","ColumnWidth":"-1",})
		
		# Making the regions to be marked
		for i in range(len(final)):
			if(final[i][4]==j):
				x1 = abs(final[i][0][0]-final[i][1][0])
				x2 = abs(final[i][0][1]-final[i][3][1])
				r = ET.SubElement(r1,"Region",{"Id":str(i+1),
												"Type":"1",
												"Zoom":"1",
												"Selected":"1",
												"ImageLocation":"",
												"ImageFocus":"-1",
												"Length":str(float(2*(x1+x2))),
												"Area":str(float(x1*x2)),
												"LengthMicrons":str(float(x1+x2)),
												"AreaMicrons":str(float((x1*x2)/4)),
												"Text":"",
												"NegativeROA":"0",
												"InputRegionId":"0",
												"Analyze":"0",
												"DisplayId":str(i+1),})
				att = ET.SubElement(r,"Attributes")
				ver = ET.SubElement(r,"Vertices")   
				v1 = ET.SubElement(ver,"Vertex",{"X":str(final[i][0][0]),"Y":str(final[i][0][1]),"Z":"0",})
				v2 = ET.SubElement(ver,"Vertex",{"X":str(final[i][1][0]),"Y":str(final[i][1][1]),"Z":"0",})
				v3 = ET.SubElement(ver,"Vertex",{"X":str(final[i][2][0]),"Y":str(final[i][2][1]),"Z":"0",})
				v4 = ET.SubElement(ver,"Vertex",{"X":str(final[i][3][0]),"Y":str(final[i][3][1]),"Z":"0",})

	tree = ET.ElementTree(root)

	with open(dest, "wb") as files:
		tree.write(files)
	print("XML file created successfully!")


def formatXML(filename):
	"""
		Used to format an XML file to make it more readable
		Args:
			The XML file
		Returns:
			void
			This method formats the XML file after the file has been created
	"""

	with open(filename) as xmldata:
		xml = minidom.parseString(xmldata.read())
		xml_pretty = xml.toprettyxml()
		f = open(filename,"w")
		f.write(xml_pretty)
	print("XML formatted Successfully")

def makeXML(filename,grid_size):
	"""
		Main function that generates the XML file for the sample 003
	
		Args:
			The input file from which the values are read
			The length of the grid
	
		Returns:
			void
			This method calls the appropriate methods to read the values and creates an XML file accordingly
		
		Note: For a CSV file it creates an XML file for the existing dataset
	"""
	f = takeInputs(filename,grid_size)
	#print(f)
	fname = filename[:len(filename)-4]
	makeAnnotation(f,fname + ".xml", 6)
	formatXML(fname + ".xml")
	
if __name__ == "__main__":
	tilesize = 256
	#xmlpath = "I:\\Qupath-WSI\\TimestampsFolder\\2021-03-14_14-48-51\\Sample003_optimized_geoaugmented_CART_roc_auc_jyothidataset_resultsof_prediction_gt_latest_version.csv"
	#makeXML(xmlpath,tilesize)
