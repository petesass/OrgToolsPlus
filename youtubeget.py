import pytube
import moviepy.editor as mp
import os

# Step 1: Get the YouTube video URL from the user
youtube_link = input("Enter the URL of the YouTube video: ")

# Step 2: Create a Pytube object for the YouTube video
youtube_object = pytube.YouTube(youtube_link)

# Step 3: Get the highest quality audio stream from the YouTube video
audio_stream = youtube_object.streams.filter(only_audio=True).order_by('abr').desc().first()

# Step 4: Download the audio stream to a local file
audio_file = audio_stream.download()

# Step 5: Get the title of the YouTube video
video_title = youtube_object.title

# Step 6: Replace special characters in the title and create a file name
filename = video_title.replace('|', '').replace('"', '').replace('/', '').replace('\\', '').replace('*', '').replace('?', '').replace('<', '').replace('>', '').replace(':', '').replace('.', '').strip() + '.mp3'

# Step 7: Create a folder called "youtubeGet" in the "documents" directory if it does not already exist
folder_path = os.path.join(os.path.expanduser('~'), 'documents', 'youtubeGet')
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Step 8: Create the full path for the output MP3 file
output_file_path = os.path.join(folder_path, filename)

# Step 9: Convert the downloaded audio file to MP3 format using MoviePy library and save to the output file path
mp_audio = mp.AudioFileClip(audio_file)
mp_audio.write_audiofile(output_file_path)

# Step 10: Delete the downloaded audio and video files
os.remove(audio_file)
for file in os.listdir(os.getcwd()):
    if file.endswith('.webm'):
        os.remove(file)
