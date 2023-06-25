import os
import random
import shutil

def split_data(mainTrainFolder, valSplitRatio, testSplitRatio, outputFolderPath):
    # Create output folders
    images_folder = os.path.join(outputFolderPath, "images")
    labels_folder = os.path.join( outputFolderPath, "labels")
    train_folder = os.path.join(images_folder, "train")
    val_folder = os.path.join(images_folder, "val")
    test_folder = os.path.join(images_folder, "test")
    train_labels_folder = os.path.join(labels_folder, "train")
    val_labels_folder = os.path.join(labels_folder, "val")
    test_labels_folder = os.path.join(labels_folder, "test")
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    os.makedirs(train_labels_folder, exist_ok=True)
    os.makedirs(val_labels_folder, exist_ok=True)
    os.makedirs(test_labels_folder, exist_ok=True)

    # Get list of all image files in mainTrainFolder
    image_files = [f for f in os.listdir(mainTrainFolder)
                   if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")]

    # Shuffle the list of image files
    random.shuffle(image_files)

    # Calculate number of images to use for validation and testing
    total_images = len(image_files)
    val_count = int(total_images * valSplitRatio)
    test_count = int(total_images * testSplitRatio)

    # Move validation images and labels
    val_images = image_files[:val_count]
    for image_file in val_images:
        src_image_path = os.path.join(mainTrainFolder, image_file)
        dst_image_path = os.path.join(val_folder, image_file)
        shutil.move(src_image_path, dst_image_path)
        label_file = os.path.splitext(image_file)[0] + ".txt"
        src_label_path = os.path.join(mainTrainFolder, label_file)
        dst_label_path = os.path.join(val_labels_folder, label_file)
        shutil.move(src_label_path, dst_label_path)

    # Move test images and labels
    test_images = image_files[val_count:(val_count+test_count)]
    for image_file in test_images:
        src_image_path = os.path.join(mainTrainFolder, image_file)
        dst_image_path = os.path.join(test_folder, image_file)
        shutil.move(src_image_path, dst_image_path)
        label_file = os.path.splitext(image_file)[0] + ".txt"
        src_label_path = os.path.join(mainTrainFolder, label_file)
        dst_label_path = os.path.join(test_labels_folder, label_file)
        shutil.move(src_label_path, dst_label_path)

    # Move remaining images and labels to train folder
    train_images = image_files[(val_count+test_count):]
    for image_file in train_images:
        src_image_path = os.path.join(mainTrainFolder, image_file)
        dst_image_path = os.path.join(train_folder, image_file)
        shutil.move(src_image_path, dst_image_path)
        label_file = os.path.splitext(image_file)[0] + ".txt"
        src_label_path = os.path.join(mainTrainFolder, label_file)
        dst_label_path = os.path.join(train_labels_folder, label_file)
        shutil.move(src_label_path, dst_label_path)

if __name__ == '__main__':
    mainFolderPath = "train" # the path is relative
    valSplitRatio = 0.2
    testSplitRatio = 0.1
    outputFolderPath = "output" # the path is relative
    
    rootPath = os.path.dirname(os.path.abspath(__file__))
    split_data(os.path.join(rootPath,mainFolderPath), 
               valSplitRatio, 
               testSplitRatio, 
               os.path.join(rootPath,outputFolderPath))
