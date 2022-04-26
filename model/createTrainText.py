from os import listdir

files = listdir("/home/edo/COCO-YOLO-Parser/image") #folder containing .txt annotation files
path_from_root = "./data/obj/" #path of folder containing images
image_type = "jpg" 

#Change above fields as required

f = open("train.txt", "w+")
for file in files:
        ending = file
        f.write(path_from_root+ending+"\n") 
        
