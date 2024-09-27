import tkinter as tk
from tkinter import filedialog, simpledialog
import os

# Initialize the Tkinter root and hide the main window
root = tk.Tk()
root.withdraw()

# Open folder dialog
folder_path = filedialog.askdirectory(
    title="Select the folder containing the image files"
)
if not folder_path:
    exit()

# Ask for a prefix string
default_prefix = "C:/Users/HP/Documents/GitHub/Object-Detection-and-Datasets/Datasets/New Building/Goals/"
prefix = simpledialog.askstring(
    "Prefix Input",
    "Enter a prefix to add before each path.\nFor instance:",
    initialvalue=default_prefix,
)
if prefix is None:  # User canceled the input
    prefix = ""


# Open save file dialog
txt_file = filedialog.asksaveasfilename(
    defaultextension=".txt",
    initialfile="_output.txt",
    title="Save the output file as",
    filetypes=[("Text files", "*.txt")],
)
if not txt_file:
    exit()

# Write to the file if paths were selected
with open(txt_file, "w") as f:
    for file_name in os.listdir(folder_path):
        if file_name.endswith((".png", ".jpg", ".jpeg")):
            sanitized_file_name = file_name.strip()  # Ensure no extra characters
            f.write(prefix + sanitized_file_name + "\n")

print(
    f"Done! The names of all text files in '{folder_path}' have been saved to '{txt_file}' with the prefix '{prefix}'"
)
