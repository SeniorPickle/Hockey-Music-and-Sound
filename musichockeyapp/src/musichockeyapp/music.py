import toga
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack
import pygame
import time

class Music():
    def __init__(self, album, name, number, path):
        self.album = album
        self.name = name
        self.number = number
        self.path = path
        self.music_playing=False
        self.start_time_of_music=0
        self.time_playing=0
        self.start_pause_time=0
        self.end_pause_time=0
        self.pause_time=0
        pygame.mixer.init()

    def build(self):
        album_entry_box = toga.Box()
        album = toga.Button(self.name, style=Pack(flex=1, height=60, padding=(10, 0, 0, 10)),on_press=self.play)
        album_close = toga.Button("X", style=Pack(height=60, padding=(10, 10, 0, 0)), on_press=self.song_delete)
        album_entry_box.add(album)
        album_entry_box.add(album_close)
        return album_entry_box

    def play(self, what=None, pause_unpause=False):

        if self.album.app.music_playing[1] != False and self.music_playing != True:
            self.album.app.music_playing[1] = False
            self.reset_values()
            self.album.app.albums[self.album.app.music_playing[0][0]].contents[self.album.app.music_playing[0][1]].music_playing = False
            pygame.mixer.music.pause()

        if self.music_playing == False and pause_unpause == False:
            pygame.mixer.music.load(self.path)
            self.start_time_of_music = time.time()
            self.time_playing = (-1*(self.start_time_of_music - time.time()))-self.pause_time
            self.music_playing = True
            pygame.mixer.music.play()
            self.album.app.music_playing = [[self.album.number, self.number], True, False]
        elif self.music_playing == True and pause_unpause == True:
            self.start_pause_time = time.time()
            self.music_playing = False
            pygame.mixer.music.pause()
            self.album.app.music_playing[1] = False
        elif self.music_playing == False and pause_unpause == True:
            self.end_pause_time = time.time()
            self.pause_time = (self.end_pause_time - self.start_pause_time)
            self.time_playing = ((-1 * (self.start_time_of_music - time.time()))-self.pause_time)
            self.music_playing = True
            pygame.mixer.music.unpause()
            self.album.app.music_playing = [[self.album.number, self.number], True, False]
        else:
            pass


        if self.album.app.music_playing[2] != True:
            self.album.app.music_playing[2] = True
            self.album.app.redefine_persistent_box()
            if self.album.app.current_page == "main_page":
                self.album.app.refresh_box()
            else:
                self.album.refresh_album_box()
            self.album.app.music_playing[2] = False

    def check_music_playing(self):
        self.time_playing = ((-1 * (self.start_time_of_music - time.time())) - self.pause_time)
        print(self.time_playing)
        if pygame.mixer.music.get_busy() != True:
            self.forward_play()

    def forward_play(self, what=None):
        try:
            self.music_playing = False
            self.reset_values()
            self.album.app.music_playing[0][1] += 1
            self.album.contents[self.album.app.music_playing[0][1]].play()
        except IndexError:
            self.reset_values()
            self.album.app.music_playing[0][1] = 0
            self.album.contents[self.album.app.music_playing[0][1]].play()

    def back_play(self, what=None):
        try:
            if ((-1 * (self.start_time_of_music - time.time())) - self.pause_time) <= 5:
                self.music_playing = False
                self.reset_values()
                self.album.app.music_playing[0][1] -= 1
                self.album.contents[self.album.app.music_playing[0][1]].play()
            else:
                self.reset_values()
                self.album.contents[self.album.app.music_playing[0][1]].play()
        except IndexError:
            self.reset_values()
            self.album.app.music_playing[0][1] = (len(self.album.contents)-1)
            self.album.contents[self.album.app.music_playing[0][1]].play()

    def reset_values(self, what=None):
        self.start_time_of_music = 0
        self.time_playing = 0
        self.start_pause_time = 0
        self.end_pause_time = 0
        self.pause_time = 0


    def song_delete(self, what=None):
        pass
