from math import e
from Visualize.parseXML import *
from Visualize.genTilesForRoi import *
from Visualize.labelStatus import *
from Visualize.createXML import *
from Visualize.extractDetails import *
import pyvips
import numpy as np

class VisualizeTiles(object):

	def __init__(self, filename):
		"""
		Constructor

		Args:
			filename: input filename

		Returns:
			void
			However it uses the extractDetailsFromFile function to extract information from the input file in relevant formats
		"""
		arr = extractDetailsFromFile(filename)
		self.imgname = arr[0]
		self.xmlname = arr[1]
		self.roi_coords = arr[2]
		self.tilesize = arr[3]


	def parseXMLContents(self,output_path):
		"""
		Wrapper function for parseXML function
		"""
		self.roi_filename,self.labels = parseXML(self.xmlname, self.roi_coords,output_path)

	def getROITiles(self):
		"""
		Wrapper function for getTiles function
		"""
		x1, y1, x2, y2 = self.roi_coords
		roi = getROI(x1, y1, x2, y2)
		return getTiles(roi, self.tilesize)

	def getAnnotationDict(self):
		"""
		Creates a dictionary mapping labels to their corresponding annotations

		Returns: A dictionary mapping labels to their corresponding polygons (representing the annotation)
		"""
		annotations = makeAnnotations(self.roi_filename)
		dicti = {}
		for annotation in annotations:
			label = annotation.getLabel()
			dicti[label] = annotation
		return dicti

	def updateTileStatus(self, tiles, dicti):
		"""
		Updates the status of all the tiles wrt all the labels that are asked for

		Args:
			tiles: 2-D array of tile objects
			dicti: dictionary mapping labels of annotations to the polygons of the annotations in question
		"""
		self.out_filenames = []
		for label in self.labels:
			poly = dicti[label]
			#print(label)
			#print("poly",poly)
			#output_file = self.roi_filename[:-4] + "_label_" + label + ".txt"
			updateStatus(tiles, poly)
			#self.out_filenames.append(output_file)

	def generateXML(self, filename):
		"""
		Wrapper for genXML function
		"""
		genXML(filename, self.tilesize) 

	def generateXMLs(self):
		"""
		Wrapper around generateXML function to generate xml files for all the labels that are asked for
		"""
		self.parseXMLContents()
		tiles = self.getROITiles()
		annotations = self.getAnnotationDict()
		self.updateTileStatus(tiles, annotations)
		for filename in self.out_filenames:
			self.generateXML(filename)

	def getTileImages(self, output_path):
		"""
		Crop out tile images with an accompanying info.txt file that has information like the label, status and percentage overlap for each tile

		Args:
			output_path: The path to the directory into which the info.txt file and all the cropped out tile images will be outputted to
		"""
		collectnames = []
		outtiles=[]
		unlabelledtiles=[]
		"""
		my_dict = {
		"filename":[],
		"image_array":[]
		}

		format_to_dtype = {
			'uchar': np.uint8,
			'char': np.int8,
			'ushort': np.uint16,
			'short': np.int16,
			'uint': np.uint32,
			'int': np.int32,
			'float': np.float32,
			'double': np.float64,
			'complex': np.complex64,
			'dpcomplex': np.complex128,
		}
		"""
		info_file = output_path + "/master_info.txt" 
		self.parseXMLContents(output_path)
		tiles = self.getROITiles()
		annotations = self.getAnnotationDict()
		self.updateTileStatus(tiles, annotations)
		slide = pyvips.Image.new_from_file(self.imgname,autocrop=True).rot90()
		with open(info_file, "w") as file:
			file.write(self.imgname + "\n")
			file.write(self.xmlname + "\n")
			roi = str(self.roi_coords[0]) + " " + str(self.roi_coords[1]) + " " + str(self.roi_coords[2]) + " " + str(self.roi_coords[3])
			file.write(roi + "\n")
			for row in tiles:
				for tile in row:
					x, y = tile.getVertices()[0]
					#.copy()
					image = slide.crop(x, y, self.tilesize, self.tilesize)
					#print(image)
					#image_array =np.ndarray(buffer=image.write_to_memory(),
					#  dtype=format_to_dtype[image.format],
					#  shape=[image.height, image.width, image.bands])
					#print(image_array)					  
					name = "".join([output_path,"/","Samplefile","-tile-r100-c100-x",str(int(x)),"-y",str(int(y)),"-w",str(int(self.tilesize)),"-h",str(int(self.tilesize)),".png"])
					#my_dict["filename"].append(name)
					name1="".join([output_path,"/","Samplefile","-tile-r100-c100-x",str(int(x)),"-y",str(int(y)),"-w",str(int(self.tilesize)),"-h",str(int(self.tilesize)),'_masked.png'])
					#my_dict["image_array"].append(image_array)

					#image.write_to_file(name)
					#print(self.labels)
					#0 - indicates the annotation is completely inside the tile
					#1 - indicates the boundary (meaning the annoation will be covering some area w.r.t  tile)
					#3 - for detecting the cell regions(small areas like mitosis)
					#2 - unlabelled tiles
					for label in self.labels:
						label_collection = tile.getLabelStatus()
						try:
							if(label in label_collection):
								#image.write_to_file(name)
								print(name1)
								file.write("".join([name[(len(output_path)+1):]," ",label," ",str(tile.getLabelStatus()[label][0])," ",str(tile.getLabelStatus()[label][1])," "]))
								file.write("".join([name1[(len(output_path)+1):],"\n"]))
								 #collectnames.append(name[(len(output_path)+1):])
							#else:
								#outtiles.append(name[(len(output_path)+1):])
						except Exception as e:
							print(e)		
			#unlabelledtiles = set(outtiles)-set(collectnames)
			#for i in unlabelledtiles:
				#file.write("".join([i," ","Unlabelled"," ",'2'," "," ","\n"]))
			#df = pd.DataFrame(my_dict)
			#df.to_csv(output_path+"info_image_numpy.csv")
			

	def getTilesAndXMLs(self, output_path):
		"""
		Combines the functionality of generateXMLs and getTileImages functions
		"""
		self.parseXMLContents()
		tiles = self.getROITiles()
		annotations = self.getAnnotationDict()
		self.updateTileStatus(tiles, annotations)
		for filename in self.out_filenames:
			self.generateXML(filename)
		
		slide = pyvips.Image.new_from_file(self.imgname, autocrop=True).rot90()
		info_file = output_path + "/info.txt"
		with open(info_file, "w") as file:
			file.write(self.imgname + "\n")
			file.write(self.xmlname + "\n")
			roi = str(self.roi_coords[0]) + " " + str(self.roi_coords[1]) + " " + str(self.roi_coords[2]) + " " + str(self.roi_coords[3])
			file.write(roi + "\n")
			for row in tiles:
				for tile in row:
					x, y = tile.getVertices()[0]
					image = slide.crop(x, y, self.tilesize, self.tilesize)
					#print(image)
					name = output_path + "/" + self.imgname + "_" + str(x) + "_" + str(y) + "_" + str(self.tilesize) + ".png"
					image.write_to_file(name)
					for label in self.labels:
						file.write(name[(len(output_path)+1):] + " " + label + " " + str(tile.getLabelStatus()[label][0]) + " " + str(tile.getLabelStatus()[label][1]) + "\n")
	

	


	

	


	