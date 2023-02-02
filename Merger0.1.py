import os
import shutil

# prompt user for directory path
dir_path = input("Enter the path of the directory to search: ")

# create the Merger folder if it does not exist
merger_path = os.path.join(dir_path, 'Merger')
if not os.path.exists(merger_path):
    os.makedirs(merger_path)

# loop through all subfolders in the directory
for root, dirs, files in os.walk(dir_path):
    # ignore the Merger folder
    if root == merger_path:
        continue

    # move all files in the current subfolder to the Merger folder
    for file in files:
        file_path = os.path.join(root, file)
        shutil.move(file_path, os.path.join(merger_path, file))

print("Files merged into the Merger folder.")

# check if the user wants to delete empty Scrubber folders
delete_scrubber = input("Do you want to delete the empty Scrubber folders? (y/n) ")
if delete_scrubber == 'y':
    # loop through all subfolders in the directory
    for root, dirs, files in os.walk(dir_path):
        # ignore the Merger folder and any subfolders inside it
        if root == merger_path or root.startswith(merger_path):
            continue
        
        for d in dirs:
            # delete the folder if it has "Scrubber" in its name and is empty
            if "Scrubber" in d and not os.listdir(os.path.join(root, d)):
                shutil.rmtree(os.path.join(root, d))

print("Scrubber folders deleted (if specified).")
