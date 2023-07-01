from PIL import Image                                              
import os, sys                       

path = 'images/'
dirs = os.listdir(path=path)                                       

# print(dirs)
def resize():
    for item in dirs:
        for img in os.listdir(path+item):
            img_dir=os.path.join(path+item,img)
            img = Image.open(img_dir)
            img = img.resize((148, 32)) 
            img.save(img_dir)

resize()