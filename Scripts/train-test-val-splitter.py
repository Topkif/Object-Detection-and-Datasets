import os
import random
import shutil
import tkinter as tk
from tkinter import filedialog

# Initialize the Tkinter root and hide the main window
root = tk.Tk()
root.withdraw()

# Ask the user to choose the folder path containing the images
folder_path = filedialog.askdirectory(title="Select the folder containing the images")

# Define the proportions for training, validation, and testing
train_prop = 0.6
val_prop = 0.4
test_prop = 0

# Ask the user to choose the output folder for the split datasets
output_folder = filedialog.askdirectory(
    title="Select the output folder for the split datasets"
)

# Create the directories for the training, validation, and test sets
train_img_dir = os.path.join(output_folder, "images", "train")
val_img_dir = os.path.join(output_folder, "images", "val")
test_img_dir = os.path.join(output_folder,"images",  "test")

os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(val_img_dir, exist_ok=True)
os.makedirs(test_img_dir, exist_ok=True)

train_label_dir = os.path.join(output_folder, "labels", "train")
val_label_dir = os.path.join(output_folder,"labels", "val")
test_label_dir = os.path.join(output_folder,"labels", "test")

os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)
os.makedirs(test_label_dir, exist_ok=True)

# Get a list of all image files in the folder
image_files = [
    f for f in os.listdir(folder_path) if f.endswith((".png", ".jpg", ".jpeg"))
]

# Shuffle the list of image files
random.shuffle(image_files)

# Split the image files into training, validation, and test sets
train_count = int(train_prop * len(image_files))
val_count = int(val_prop * len(image_files))
test_count = len(image_files) - train_count - val_count  # Remaining for test

train_files = image_files[:train_count]
val_files = image_files[train_count : train_count + val_count]
test_files = image_files[train_count + val_count :]

# Move the image and label files to their respective directories
for filename in train_files:
    img_path = os.path.join(folder_path, filename)
    label_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".txt")

    shutil.move(img_path, os.path.join(train_img_dir, filename))

    if os.path.exists(label_path):  # Check if label file exists
        shutil.move(
            label_path, os.path.join(train_label_dir, os.path.splitext(filename)[0] + ".txt")
        )

for filename in val_files:
    img_path = os.path.join(folder_path, filename)
    label_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".txt")

    shutil.move(img_path, os.path.join(val_img_dir, filename))

    if os.path.exists(label_path):  # Check if label file exists
        shutil.move(
            label_path, os.path.join(val_label_dir, os.path.splitext(filename)[0] + ".txt")
        )

for filename in test_files:
    img_path = os.path.join(folder_path, filename)
    label_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".txt")

    shutil.move(img_path, os.path.join(test_img_dir, filename))

    if os.path.exists(label_path):  # Check if label file exists
        shutil.move(
            label_path, os.path.join(test_label_dir, os.path.splitext(filename)[0] + ".txt")
        )


print("Data split completed successfully!")
