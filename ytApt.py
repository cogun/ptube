from pytube import YouTube
import os
import sys

from youtubesearchpython import VideosSearch

res =  VideosSearch("trap nation", limit = 5)
for i in res.result()["result"]:
    print(i["thumbnails"][0])