from pytube import YouTube
import os
import shutil
import sys

class Downloader:
    def mkPath(self,path):
        self.path = path
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
    def download(self,link,callback):
        self.yt = YouTube(link)
        self.yt.register_on_progress_callback(callback)
        self.video = self.yt.streams.filter(only_audio=True).first()
        out_file = self.video.download(output_path=self.path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    def progress_function(self,stream, chunk, bytes_remaining):
        print(round((1-bytes_remaining/self.video.filesize)*100, 3), '% done...')

# a = Downloader("songs/today")
# a.download("https://www.youtube.com/watch?v=eJJ_aOTAPJc")
