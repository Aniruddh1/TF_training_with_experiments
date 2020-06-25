import cv2
import glob
import os
import glob
import xml.etree.ElementTree as ET
from tqdm import tqdm
import pathlib

def rescale_annotations(dataset_path, output_path,scale, rename_prefix = False):
	pathlib.Path(output_path).mkdir(parents=True, exist_ok=True) 

	for i in tqdm(glob.glob('{}/*.jpg'.format(dataset_path))):

		######### Editing images #########
		img = cv2.imread('{}'.format(i))
		img = cv2.resize(img,(0,0),fx=scale,fy=scale)
        
		a = i.split('\\')[1] 
		if rename_prefix:
			a = rename_prefix + i.split('\\')[1] 
            
		cv2.imwrite(output_path + str(a),img)

		####### Editing XML file ##########
		xml_file = i.replace('.jpg','.xml')
		tree = ET.parse(xml_file)

		tree.find('.//width').text = str(int(int(tree.find('.//width').text)*scale))
		tree.find('.//height').text = str(int(int(tree.find('.//width').text)*scale))

		if rename_prefix:
			for i in (tree.iterfind('.//filename')): 
				i.text = str(a)

		for i in (tree.iterfind('.//xmin')): 
			i.text = str(int(int(i.text)*scale))
		
		for i in (tree.iterfind('.//xmax')): 
			i.text = str(int(int(i.text)*scale))
		
		for i in (tree.iterfind('.//ymin')): 
			i.text = str(int(int(i.text)*scale))
		
		for i in (tree.iterfind('.//ymax')): 
			i.text = str(int(int(i.text)*scale))

		a = xml_file.split('\\')[1] 
            
		if rename_prefix:
			a = rename_prefix + xml_file.split('\\')[1] 

		tree.write(output_path + str(a))
	print('Done rescaling annotations')

dataset_path = "F:/trash/kangaroo/one folder is alrdy resized and other is by 768 to 432/dust_def4/"
output_path = "F:/trash/kangaroo/one folder is alrdy resized and other is by 768 to 432/dust_def4_rescaled/"

scale = 0.75
rename_prefix = False#'moisture_def6'
rescale_annotations(dataset_path,output_path, scale, rename_prefix)