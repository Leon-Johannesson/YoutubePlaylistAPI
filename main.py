from pytube import Playlist
import os 
import subprocess
from random import randint
from playsound import playsound
import ctypes

class PlayList:
    def __init__(self, playList) -> None:
        self.playList = playList
        self.songAmount = 0
        self.loop = False
        self.shuffle = False
        self.songStart = 0

    def setSongAmount(self, amt:int):
        self.songAmount = amt

    def setShuffleTrue(self):
        self.shuffle = True

    def setLoopTrue(self):
        self.loop = True

    def setSongStart(self, amt:int):
        self.songStart = amt

    def download(self):
        path, dirs, files = next(os.walk("songs"))
        file_count = len(files)

        print('Number of videos in playlist: %s' % len(self.playList.video_urls))
        
        if (file_count < self.songAmount):
            count = file_count - 1
            if (file_count == 0):
                count = 0
            print(file_count, count)
            for video in self.playList.videos:
                if file_count < count or file_count == 0:
                    print("Downloading song file...")
                    v = video.streams.filter(only_audio=True).all()
                    v[0].download("songs", f"{count}.mp3")    
                    
                    # convert mp3 to wav file
                    subprocess.call(['ffmpeg', '-i', f'songs/{count}.mp3',
                                    f'songs/{count}.wav'], shell=False)
                    print("Converting MP3 to WAV file... ")
                    os.remove(f'songs/{count}.mp3')
                    count += 1

    def play_songs(self):
        folder = "songs"

        #hiding the cmd window
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')

        SW_HIDE = 0

        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, SW_HIDE)


        if (self.songStart != -1):
            playsound(f"{folder}/{self.songStart}.wav")

        if self.shuffle:
            if self.loop:
                while True:
                    playsound(f"{folder}/{randint(0, self.songAmount)}.wav")
            else:
                played_songs = []
                while len(played_songs) != self.songAmount:
                    index = randint(0, self.songAmount)
                    if index not in played_songs:
                        playsound(f"{folder}/{index}.wav")
                        played_songs.append(index)
        elif self.loop:
            while True:
                for i in range(len(self.playList.videos)):
                    playsound(f"{folder}/{i}.wav")
        else:
            for i in range(len(self.playList.videos)):
                    playsound(f"{folder}/{i}.wav")



player = PlayList("https://www.youtube.com/playlist?list=PLZ6lVRBHR4RnWDzx-PKbMuLXiAM5xbzPR")

def main():
    init()
    player.download()
    player.play_songs()

def init():
    player.setSongAmount(player.playList.video_urls)
    shuffle = input("Do you want to shuffle? (y/n) : ")
    if shuffle == "y":
        player.setShuffleTrue()
    loop = input("Do you want to loop? (y/n) : ")
    if loop == "y":
        player.setLoopTrue()
    own_start = int(input(f"Do you have any specific index you want to start at? : (1-{player.songAmount+1} or if undefined 0) : "))-1
    player.setSongStart(own_start)

main()