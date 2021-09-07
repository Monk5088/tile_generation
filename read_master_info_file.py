import itertools
import os
import pandas as pd
import shutil
import numpy as np

def one_hot_encoding_classes(infofile,csv_path,my_dict):
	with open(infofile,'r') as file: 
		# reading each line	
		for line in itertools.islice(file, 3, None): 
			d = line.split()
			li = int(float(d[-1]))
			val = d[-2]
			name_of_the_label = d[-3]
			file_name = str(d[0])
			if(val == '1' or val == '0' or val== "3"):
				if(file_name not in my_dict["filename"]):
					my_dict["filename"].append(file_name)
					my_dict["annotation_based"].append("WSI_Level")
					x = ""
					y= ""
					grid_size =""    
					f = file_name[-35 : -4]
					for i in range(len(f)):
						if(f[i]+f[i-1]=="x-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									x+= f[i]
						if(f[i]+f[i-1]=="y-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									y+=f[i]
						if(f[i]+f[i-1]=="w-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									grid_size+=f[i]
					for label in classes:
						my_dict[label].append(0)
					my_dict["offset"].append(("X:"+x+" "+"Y:"+y))
					my_dict["grid_size"].append(grid_size)    
				name_of_the_label = name_of_the_label.lower()
				name_of_the_label = name_of_the_label.replace(" ", "")
				name_of_the_label = name_of_the_label.split(',')
				label_list =[]

				for label_name in name_of_the_label:
					label_name = ''.join([i for i in label_name if not i.isdigit()])
					label_list.append(label_name)                

				for label in label_list:
					try:
						if(file_name in my_dict["filename"]):    
							count = my_dict["filename"].index(file_name)
							my_dict[label][count] = 1
					except Exception as e:
						#print(e)
						my_dict["unlabelled"][count] = 1
				
			else:
				diff_classes = set(classes)-set(["unlabelled"])
				if(file_name not in my_dict["filename"]):
					my_dict["filename"].append(file_name)
					my_dict["annotation_based"].append("WSI_Level")
					x = ""
					y= ""
					grid_size =""    
					f = file_name[-35 : -4]
					for i in range(len(f)):
						if(f[i]+f[i-1]=="x-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									x+= f[i]
						if(f[i]+f[i-1]=="y-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									y+=f[i]
						if(f[i]+f[i-1]=="w-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									grid_size+=f[i]
					my_dict["offset"].append(("X:"+x+" "+"Y:"+y))
					my_dict["grid_size"].append(grid_size)
					for label in diff_classes:
						my_dict[label].append(0)
					my_dict["unlabelled"].append(1)
				else:
					count = my_dict["filename"].index(file_name)
					my_dict["unlabelled"][count] = 1                       

	df = pd.DataFrame(my_dict)
	df.to_csv(csv_path)

	
def partitionfiles_class_label(root_dir,info_file,classes):
	df = pd.read_csv(info_file)
	for class_name in classes:
		#path = os.path.join(root_dir,root_class,class_name)
		#os.makedirs(path)
		labels=[]
		for i in range(len(df[class_name])):
			if(df[class_name][i]==1):
				labels.append(df["filename"][i])
		label_txt_file = os.path.join(root_dir,class_name +".txt")
		#print(label_txt_file)
		with open(label_txt_file,'w') as file:
			for i in set(labels):
				file.write(i)
				file.write("\n")

def partitionfiles_area_label_multiple(root_dir,info_file,classes,thresholdvalue):
	df = pd.read_csv(info_file)
	for class_name in classes:
		#path = os.path.join(root_dir,root_class,class_name)
		#os.makedirs(path)
		labels=[]
		try:
			for i in range(len(df[class_name])):
				if(df[class_name][i]>=thresholdvalue):  
					labels.append(df["filename"][i])
			label_txt_file = os.path.join(root_dir,class_name +".txt")
			#print(label_txt_file)
			with open(label_txt_file,'w') as file:
				for i in set(labels):
					file.write(i)
					file.write("\n")
		except Exception as e:
			pass

def partitionfiles_area_label_binary(root_dir,info_file,classes,threshold_value,target_class):
	df = pd.read_csv(info_file)
	#root_class ="classes"
	#os.makedirs(os.path.join(root_dir,root_class))
	#path_1 = os.path.join(root_dir,root_class,target_class)
	#path_0 = os.path.join(root_dir,root_class,"non_"+target_class)
	#os.makedirs(path_1)
	#os.makedirs(path_0)
	labels_1=[]
	labels_0=[]
	for i in range(len(df[target_class])):
		# if using threshold use this else change if condition to
		#if(df[target_class][i]==1)
		if(df[target_class][i]>=threshold_value): 
			labels_1.append(df["filename"][i])
		if(df[target_class][i]==0):
			labels_0.append(df["filename"][i])
	label_1_txt_file = os.path.join(root_dir,target_class +".txt")
	label_0_txt_file = os.path.join(root_dir,"non_"+target_class +".txt")
	#print(label_1_txt_file)
	#print(label_0_txt_file)
	with open(label_1_txt_file,'w') as file:
		for i in set(labels_1):
			file.write(i)
			file.write("\n")

	with open(label_0_txt_file,'w') as file:
		for i in set(labels_0):
			file.write(i)
			file.write("\n")

def area_of_regions_class(info_file,csv_path,bucket_file_path):
	classes = ["discard","fascicles","whorls","necrosis","micronecrosis","anisonucleosis","sheeting","nucleoli","mitosis","smallcellchange","none"]
	my_dict = {
		"filename":[],
		"annotation_based":[],
		"offset":[],
		"grid_size":[],
		"discard":[],
		"fascicles":[],
		"whorls":[],
		"necrosis":[],
		"micronecrosis":[],
		"anisonucleosis":[],
		"sheeting":[],
		"nucleoli":[],
		"mitosis":[],
		"smallcellchange":[],
		"none":[]
	}
	bucket_dict={
		"label":[],
		"1-10":[],
		"11-20":[],
		"21-30":[],
		"31-40":[],
		"41-50":[],
		"51-60":[],
		"61-70":[],
		"71-80":[],
		"81-90":[],
		"91-100":[],
		"total_count":[]
	}
	with open(info_file,'r') as file: 
		# reading each line	
		for line in itertools.islice(file, 3, None): 
			d = line.split()
			li = float(d[-1])
			val = d[-2]
			name_of_the_label = d[-3]
			file_name = str(d[0])
			if(val!="Unlabelled"):
				if(file_name not in my_dict["filename"]):
					my_dict["filename"].append(file_name)
					my_dict["annotation_based"].append("WSI_Level")
					x = ""
					y= ""
					grid_size=""    
					f = file_name[-35 : -4]
					for i in range(len(f)):
						if(f[i]+f[i-1]=="x-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									x+= f[i]
						if(f[i]+f[i-1]=="y-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									y+=f[i]
						if(f[i]+f[i-1]=="w-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									grid_size+=f[i]
					for label in classes:
						my_dict[label].append(0)
					my_dict["offset"].append(("X:"+x+" "+"Y:"+y))
					my_dict["grid_size"].append(grid_size)
					name_of_the_label = name_of_the_label.lower()
					name_of_the_label = name_of_the_label.replace(" ", "")
					name_of_the_label = name_of_the_label.split(',')
					label_list =[]
					for label_name in name_of_the_label:
						label_name = ''.join([i for i in label_name if not i.isdigit()])
						label_list.append(label_name)

					for label in label_list:
						try:
							if(file_name in my_dict["filename"]):    
								count = my_dict["filename"].index(file_name)
								my_dict[label][count] = my_dict[label][count]+li
						except Exception as e:
							pass

			else:
				if(file_name not in my_dict["filename"]):
					my_dict["filename"].append(file_name)
					my_dict["annotation_based"].append("WSI_Level")
					x = ""
					y= ""
					grid_size=""    
					f = file_name[-35 : -4]
					for i in range(len(f)):
						if(f[i]+f[i-1]=="x-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									x+= f[i]
						if(f[i]+f[i-1]=="y-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									y+=f[i]
						if(f[i]+f[i-1]=="w-"):
							k=i+1
							for i in range(k,len(f)):
								if(f[i]=='-'):
									break
								else:
									grid_size+=f[i]
					for label in classes:
						my_dict[label].append(0)
					my_dict["offset"].append(("X:"+x+" "+"Y:"+y))
					my_dict["grid_size"].append(grid_size)

	df = pd.DataFrame(my_dict)
	df.to_csv(csv_path)

	for label in classes:
		d = my_dict[label]
		#print(d)
		zero=0
		c1,c2,c3,c4,c5,c6,c7,c8,c9,c10=0,0,0,0,0,0,0,0,0,0
		for i in d:
			#if(i>=1 and i<=29):
			#	zero=zero+1
			if(i>=1 and i<11):
				c1=c1+1
			elif(i>=11 and i<21):
				c2=c2+1
			elif(i>=21 and i<31):
				c3=c3+1
			elif(i>=31 and i<41):
				c4=c4+1
			elif(i>=41 and i<51):
				c5=c5+1
			elif(i>=51 and i<61):
				c6=c6+1
			elif(i>=61 and i<71):
				c7=c7+1
			elif(i>=71 and i<81):
				c8=c8+1
			elif(i>=81 and i<91):
				c9=c9+1
			elif(i>=91 and i<=100):
				c10=c10+1				
		#print(zero)    
		bucket_dict["label"].append(label)
		bucket_dict["1-10"].append(c1)
		bucket_dict["11-20"].append(c2)
		bucket_dict["21-30"].append(c3)
		bucket_dict["31-40"].append(c4)
		bucket_dict["41-50"].append(c5)
		bucket_dict["51-60"].append(c6)
		bucket_dict["61-70"].append(c7)
		bucket_dict["71-80"].append(c8)
		bucket_dict["81-90"].append(c9)
		bucket_dict["91-100"].append(c10)
		bucket_dict["total_count"].append(c1+c2+c3+c4+c5+c6+c7+c8+c9+c10)
	df = pd.DataFrame(bucket_dict)
	df.to_csv(bucket_file_path)
	
def copy_images_into_folder(txtfile_path,tiles_directory_path,destination_path):
	## copy files from one folder to another by reading .txt file
	with open(txtfile_path,'r') as file:
		for line in file:		
			f = os.path.join(tiles_directory_path,line)
			f = f.strip('\n')
			shutil.copy(f,destination_path)

def Extract_x_and_y_values(file_name):
	x = ""
	y= ""    
	f = file_name[-35 : -4]
	for i in range(len(f)):
		if(f[i]+f[i-1]=="x-"):
			k=i+1
			for i in range(k,len(f)):
				if(f[i]=='-'):
					break
				else:
					x+= f[i]
		if(f[i]+f[i-1]=="y-"):
			k=i+1
			for i in range(k,len(f)):
				if(f[i]=='-'):
					break
				else:
					y+=f[i]
	print(x,y)

if __name__ == '__main__':
	f = open("C:/Digital_Histopathology/Tile_generation/inputfile.txt","r")
	l =[]
	for i in f:
		l.append(i.strip())
	infofile = os.path.join(l[2],"info.txt")
	classes = ["discard","fascicles","whorls","necrosis","micronecrosis","sheeting","nucleoli","anisonucleosis","mitosis","smallcellchange","none","unlabelled"]    
	my_dict = {
		"filename":[],
		"annotation_based":[],
		"offset":[],
		"grid_size":[],
		"discard":[],
		"fascicles":[],
		"whorls":[],
		"necrosis":[],
		"micronecrosis":[],
		"sheeting":[],
		"nucleoli":[],
		"anisonucleosis":[],
		"mitosis":[],
		"smallcellchange":[],
		"none":[],
		"unlabelled":[]
	}	
	target_class="necrosis"
	thresholdvalue = 1
	root_dir = l[2]
	wsi_csv_file = os.path.join(l[2],"WSI_Inventory.csv")
	area_region_csv_path = os.path.join(l[2],"WSI_Inventory_regions.csv")
	bucket_csv_file_path = os.path.join(l[2],"WSI_Inventory_buckets.csv")
	one_hot_encoding_classes(infofile,wsi_csv_file,my_dict)
	#partitionfiles_area_label_multiple(root_dir,area_region_csv_path,classes,thresholdvalue)
	area_of_regions_class(infofile,area_region_csv_path,bucket_csv_file_path)
	#thresholdvalue = 30
	partitionfiles_area_label_binary(root_dir,area_region_csv_path,classes,thresholdvalue,target_class)
	#shutil.copy(infofile,l[2])


