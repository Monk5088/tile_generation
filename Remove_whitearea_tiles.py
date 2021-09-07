import cv2
import numpy as np
import glob
import shutil

def copy_images_into_folder(txtfile_path,tiles_directory_path,destination_path):
	## copy files from one folder to another by reading .txt file
	with open(txtfile_path,'r') as file:
		for line in file:		
			f = os.path.join(tiles_directory_path,line)
			f = f.strip('\n')
			shutil.copy(f,destination_path)


def white_area_removal(path_to_directory):
    for file in glob.glob(path_to_directory+'/*.png'):
        img = cv2.imread(file)
        sensitivity = 30
        lower= np.array([0,0,255-sensitivity])
        upper = np.array([255,sensitivity,255])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        white = cv2.countNonZero(mask)
        all=mask.size
        #print("Total pixels: %d" % all)
        #print("White pixels: %d (%5.2f%%)" % (white, 100.0*white/all))
        thresholdvalue = 100.0*white/all
        #Based on the threshold here we will eliminate blank tiles.This threshold denotes the tissue area
        #print(thresholdvalue)
        if(thresholdvalue<97):#Eliminates tiles which has <=3% tissue
            print(file) #Based on your use-case change the code here

if __name__=="__main__":
    path_to_directory="//path//to//tiles//directory"
    white_area_removal(path_to_directory)