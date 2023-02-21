import os
import shutil

# prompt user for directory path
dir_path = input("Enter the path of the directory to search: ")

# initialize an empty set to store unique file types
file_types = set()

# search the directory for all file types
for root, dirs, files in os.walk(dir_path):
    for file in files:
        # split the file name and extension
        file_name, file_extension = os.path.splitext(file)

        # add the file extension to the set of file types
        file_types.add(file_extension)

# write the list of file types to a txt file
with open("file_types.txt", "w") as file:
    for file_type in file_types:
        file.write(file_type + "\n")

# open the txt file containing the list of file types
os.startfile("file_types.txt")

# ask user to exclude types
exclude_types = input("Enter file types to exclude, separated by spaces: ").split()

# remove the excluded file types from the set
file_types -= set(exclude_types)

# specify the number of subdirectories to search through
max_depth = int(input("Enter the number of subdirectories to search through: "))

# create a dictionary to store the file types and their respective folder names
file_types_dict = {}
for file_type in file_types:
    folder_name = file_type.replace(".", "") + "OTPScrub"
    file_types_dict[file_type] = folder_name

# create a nested dictionary to store the files found for each file type
found_files = {file_type: [] for file_type in file_types_dict.keys()}

# search the directory for all file types
for root, dirs, files in os.walk(dir_path):
    if max_depth <= 0:
        break
    max_depth -= 1
    dirs[:] = [d for d in dirs if 'OTPScrub' not in d]
    for file in files:
        for file_type, folder_name in file_types_dict.items():
            if file.endswith(file_type):
                if file_type not in exclude_types:
                    found_files[file_type].append(os.path.join(root, file))

# create the folders for each file type if they do not exist
for file_type, folder_name in file_types_dict.items():
    if not os.path.exists(os.path.join(dir_path, folder_name)):
        os.makedirs(os.path.join(dir_path, folder_name))

# move the files to their respective folders
for file_type, folder_name in file_types_dict.items():
    for file in found_files[file_type]:
        shutil.move(file, os.path.join(dir_path, folder_name, os.path.basename(file)))

print("Files moved to their respective folders.")
