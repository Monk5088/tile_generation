#from Visualize.visualizeTiles import *
import time
import sys
#print(sys.path)
sys.path.append("C:\Digital_Histopathology\Tile_generation\main")
from Visualize.visualizeTiles import *
#import Visualize

if __name__ == "__main__":
	
	path_to_input_file = r"C:/Digital_Histopathology/Tile_generation/inputfile.txt"
	processing = VisualizeTiles(path_to_input_file)  ##Here VisualizeTiles is a class and we are creating an object named processing
	#print(processing)	
	start = time.time()
	print(start)
	l =[]
	f = open(r"C:/Digital_Histopathology/Tile_generation/filename.txt","r")
	for i in f:
		l.append(i.strip())
	tilesfolder = l[1]
	#print(tilesfolder)

	processing.getTileImages(tilesfolder)
	end = time.time()
	print(end)
	print("Time elapsed:", (end-start))