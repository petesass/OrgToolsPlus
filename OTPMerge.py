import os
import shutil

# prompt user for directory path
dir_path = input("Enter the path of the directory to search: ")

# create the OTPMerge folder if it does not exist
OTPMerge_path = os.path.join(dir_path, 'OTPMerge')
if not os.path.exists(OTPMerge_path):
    os.makedirs(OTPMerge_path)

# loop through all subfolders in the directory
for root, dirs, files in os.walk(dir_path):
    # ignore the OTPMerge folder
    if root == OTPMerge_path:
        continue

    # move all files in the current subfolder to the OTPMerge folder
    for file in files:
        file_path = os.path.join(root, file)
        shutil.move(file_path, os.path.join(OTPMerge_path, file))

print("Files merged into the OTPMerge folder.")

# check if the user wants to delete empty OTPScrub folders
delete_OTPScrub = input("Do you want to delete the empty OTPScrub folders? (y/n) ")
if delete_OTPScrub == 'y':
    # loop through all subfolders in the directory
    for root, dirs, files in os.walk(dir_path):
        # ignore the OTPMerge folder and any subfolders inside it
        if root == OTPMerge_path or root.startswith(OTPMerge_path):
            continue
        
        for d in dirs:
            # delete the folder if it has "OTPScrub" in its name and is empty
            if "OTPScrub" in d and not os.listdir(os.path.join(root, d)):
                shutil.rmtree(os.path.join(root, d))

print("OTPScrub folders deleted (if specified).")
