# OrgTools+
set of python scripts used to optimize organization of file systems + *some fun tools!*

created out of __necessity__ and __curiosity__.

__**©Petesass 2023 - Licensed under GNU GPLv3**__
-----------------------------------------

Run the .py files in anaconda3 by: ```python file/path/script.py```

Scripts:

*```OTPScrub.py```*

Will prompt the user to choose a directory, search for filetypes, return a text file with a list of filetypes, ask for exclusions, ask for subdirectory max depth, and finally output to a new folder in the directory filetypeScrubber.

*```OTPMerge.py```*

Will prompt the user to choose a directory and merge all files in all subfolders into a new folder Merger, then ask the user if they want to delete empty filetypeScrubber folders.

Fun stuff:

*```OTPYtGet.py```*

Will prompt the user for a youtube URL to download from, produce a temporary .webm file, convert to .mp3 file, delete temp .webm and place generated .mp3 in a new folder with filepath user\documents\OTPYtGet.

Dependencies: ```pytube```, ```moviepy```
