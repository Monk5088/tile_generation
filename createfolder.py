import errno
import os,sys
from datetime import datetime
from pathlib import Path

"""
This file is to create dynamic folders based on the timestamps

Preprocessing:

	Tiles folder - All the generated tiles from WSI will be stored into this folder.
				An info.txt file will also be generated.It consists of following information.
				-SCN file name
				-XML name 
				-tilename REGION+id In/On Percentage_Area_of_the_tile_covering_the_REGION

	Output_txt_files folder - It consists of text/csv files of necrosis and other files.
							Necrosis file - In/On tiles
							Others file - Out tiles
							These files are generated from the info.txt file which is generated at the time of tile generation.
							(The info.txt file will be present in tiles folder)
"""

def foldercreation():

	filename = os.path.join("C:\Digital_Histopathology\Tile_generation","filename.txt")
	tilesfolder = "tiles"
	timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	mydir = os.path.join(
		"C:\Digital_Histopathology\Tile_generation",'TimestampsFolder',timestamp) 
	try:
		os.makedirs(mydir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise  # This was not a "directory exist" error..
	with open(filename, 'w') as file:		
		file.write(mydir)
		file.write("\n"+os.path.join(mydir,tilesfolder))
		try:
			os.makedirs(os.path.join(mydir,"outputtextfiles"))
			os.makedirs(os.path.join(mydir,tilesfolder))
			file.write("\n"+ os.path.join(mydir,"outputtextfiles"))
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise  # This was not a "directory exist" error..

if __name__=='__main__':
	foldercreation()
