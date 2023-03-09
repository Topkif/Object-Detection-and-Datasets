# Ask user for folder path
$folder_path = Read-Host "Enter the path of the folder containing the JPEG files"

# Get all jpeg files in the folder
$jpeg_files = Get-ChildItem -Path $folder_path -Filter *.jpeg

# Loop through each jpeg file and rename it to jpg
foreach ($file in $jpeg_files) {
    # Generate new file name with ".jpg" extension
    $new_name = $file.Name -replace "\.jpeg$", ".jpg"

    # Check if the file with the new name already exists
    $i = 0
    while (Test-Path (Join-Path $folder_path $new_name)) {
        # If the file exists, add a number to the end of the name and try again
        $i++
        $new_name = $file.Name -replace "\.jpeg$", "-$i.jpg"
    }

    # Rename the file with the new name
    $new_path = Join-Path $folder_path $new_name
    Rename-Item -Path $file.FullName -NewName $new_name
    Write-Host "Renamed file '$($file.FullName)' to '$new_name'"
}

Write-Host "Done! All JPEG files in '$folder_path' have been renamed to JPG and made unique."
