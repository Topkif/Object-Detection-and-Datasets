# Ask user for folder path
$folder_path = Read-Host "Enter the path of the folder containing the text files"

# Get the name of the folder
$folder_name = Split-Path $folder_path -Leaf

# Get the parent folder path
$parent_folder_path = Split-Path $folder_path -Parent

# Create a text file with the name of the folder in the parent folder
$txt_file = Join-Path $parent_folder_path ($folder_name + ".txt")
New-Item -ItemType File -Path $txt_file | Out-Null

# Loop through all the txt files in the folder and append their names to the txt file
Get-ChildItem -Path $folder_path -Filter *.txt | ForEach-Object { $_.Name } | Out-File -FilePath $txt_file -Append

Write-Host "Done! The names of all text files in '$folder_path' have been saved to '$txt_file'"
