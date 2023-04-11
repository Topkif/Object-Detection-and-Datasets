import os

import random

import shutil



# Define the folder path and proportion of data to use for training and validation

folder_path = "train"

train_prop = 0.8

val_prop = 0.2



# Create the directories for the training and validation sets

train_dir = os.path.join(folder_path, "train")

val_dir = os.path.join(folder_path, "val")



os.makedirs(train_dir, exist_ok=True)

os.makedirs(val_dir, exist_ok=True)



# Get a list of all image files in the folder

image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]



# Shuffle the list of image files

random.shuffle(image_files)



# Split the image files into training and validation sets

train_count = int(train_prop * len(image_files))

val_count = int(val_prop * len(image_files))



train_files = image_files[:train_count]

val_files = image_files[train_count:train_count+val_count]



# Move the image and label files to their respective directories

for filename in train_files:

    img_path = os.path.join(folder_path, filename)

    label_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".txt")

    shutil.move(img_path, os.path.join(train_dir, filename))

    shutil.move(label_path, os.path.join(train_dir, os.path.splitext(filename)[0] + ".txt"))



with open(os.path.join(train_dir,"..", "train.txt"), "w") as f:

    for filename in train_files:

        f.write(os.path.join("train", filename) + "\n")



for filename in val_files:

    img_path = os.path.join(folder_path, filename)

    label_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".txt")

    shutil.move(img_path, os.path.join(val_dir, filename))

    shutil.move(label_path, os.path.join(val_dir, os.path.splitext(filename)[0] + ".txt"))



with open(os.path.join(val_dir,"..", "val.txt"), "w") as f:

    for filename in val_files:

        f.write(os.path.join("val", filename) + "\n")



print("Data split completed successfully!")