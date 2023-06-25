import os
path_to_label_folder = 'C:/Users/Robot-2/Documents/Yolo/Dataset_new_angle/train'

# Loop through all files in folder and subfolders
for foldername, subfolders, filenames in os.walk(path_to_label_folder):
    for filename in filenames:
        # Check if file is a .txt file
        if filename.endswith('.txt'):
            # Open file and remove duplicates
            filepath = os.path.join(foldername, filename)
            lines_seen = set()
            new_lines = []
            with open(filepath, 'r') as f:
                for line in f:
                    if line not in lines_seen:
                        new_lines.append(line)
                        lines_seen.add(line)
            # Write unique lines back to file
            with open(filepath, 'w') as f:
                f.writelines(new_lines)
                print("Cleaned {}".format(filename))
