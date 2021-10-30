import os
import torch
import torch.utils.data as data
import numpy as np 
import pandas as pd 

from PIL import Image
import cv2

class XRAY(data.Dataset):
    
    
    def __init__(self, root, data_volume, split="train", transform=None):
        super(XRAY, self)
        if data_volume == '1':
            train_label_data = "train_1.txt"
        if data_volume == '10':
            train_label_data = "train_10.txt"
        if data_volume == '50':
            train_label_data = "train_50.txt"
        if data_volume == '100':
            train_label_data = "train.txt"
        test_label_data = "test.txt"
        val_label_data = "val.txt"

        self.split = split
        self.root = root
        self.transform = transform
        self.listImagePaths = []
        self.listImageLabels = []
        tmp_root = "../../data/VinBigData_Chest_X-ray/"
        self.train_val_root = tmp_root + "converted_train_images/"
        self.test_root = tmp_root + "converted_test_images/"

        if self.split == "train":
            downloaded_data_label_txt = train_label_data
            
        elif self.split == "val":
            downloaded_data_label_txt = val_label_data

        elif self.split == "test":
            downloaded_data_label_txt = test_label_data
 
        #---- Open file, get image paths and labels
        fileDescriptor = open(os.path.join(root,downloaded_data_label_txt), "r")
        #---- get into the loop
        line = True
        
        while line:
                
            line = fileDescriptor.readline()
            
            #--- if not empty
            if line:
          
                lineItems = line.split()
                
                if self.split == "train" or "val": 
                    imagePath = os.path.join(self.train_val_root, lineItems[0])
                elif self.split == "test":
                    imagePath = os.path.join(self.test_root, lineItems[0])
                imageLabel = lineItems[1:]
                imageLabel = [int(float(i)) for i in imageLabel]
                
                self.listImagePaths.append(imagePath)
                self.listImageLabels.append(imageLabel)   
            
        fileDescriptor.close()

    def __getitem__(self, index):
        
        imagePath = self.listImagePaths[index]
        
        imageData = Image.open(imagePath).convert('RGB')
        imageLabel= torch.FloatTensor(self.listImageLabels[index])
        
        if self.transform != None: imageData = self.transform(imageData)
        
        return imageData, imageLabel

    def __len__(self):
        
        return len(self.listImagePaths)

