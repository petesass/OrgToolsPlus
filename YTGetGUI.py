import tkinter as tk
import pytube
import moviepy.editor as mp
import os
from tkinter import messagebox
from tkinter import filedialog


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.youtube_link_label = tk.Label(self, text="Enter the URL of the YouTube video:")
        self.youtube_link_label.pack()

        self.youtube_link_entry = tk.Entry(self)
        self.youtube_link_entry.pack()

        self.keep_video_var = tk.BooleanVar()
        self.keep_video_checkbox = tk.Checkbutton(self, text="Keep video file", variable=self.keep_video_var)
        self.keep_video_checkbox.pack()

        self.download_button = tk.Button(self, text="Download", command=self.download_audio)
        self.download_button.pack()

        self.open_folder_button = tk.Button(self, text="Open Folder", command=self.open_folder)
        self.open_folder_button.pack()

    def download_audio(self):
        youtube_link = self.youtube_link_entry.get()

        youtube_object = pytube.YouTube(youtube_link)

        audio_stream = youtube_object.streams.filter(only_audio=True).order_by('abr').desc().first()

        audio_file = audio_stream.download()

        video_title = youtube_object.title
        filename = video_title.replace('|', '').replace('"', '').replace('/', '').replace('\\', '').replace('*', '').replace('?', '').replace('<', '').replace('>', '').replace(':', '').replace('.', '').strip() + '.mp3'

        folder_path = os.path.join(os.path.expanduser('~'), 'documents', 'youtubeGet')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        output_file_path = os.path.join(folder_path, filename)

        mp_audio = mp.AudioFileClip(audio_file)
        mp_audio.write_audiofile(output_file_path, verbose=False)

        if self.keep_video_var.get():
            video_stream = youtube_object.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video_file = video_stream.download()

            video_filename = video_title.replace('|', '').replace('"', '').replace('/', '').replace('\\', '').replace('*', '').replace('?', '').replace('<', '').replace('>', '').replace(':', '').replace('.', '').strip() + '.mp4'
            video_output_path = os.path.join(folder_path, video_filename)

            mp_video = mp.VideoFileClip(video_file)
            mp_video.audio.write_audiofile(output_file_path, verbose=False)
            final_clip = mp_video.set_audio(mp_audio)
            final_clip.write_videofile(video_output_path, audio_codec='aac', verbose=False)

            os.remove(video_file)

        os.remove(audio_file)

        messagebox.showinfo("Success", "Download successful!")

    def open_folder(self):
        folder_path = os.path.join(os.path.expanduser('~'), 'documents', 'youtubeGet')
        os.system(f'start "" "{folder_path}"')


root = tk.Tk()
app = Application(master=root)
app.mainloop()
