import toga
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack
import pygame

class Music():
    def __init__(self, album, name, number, path):
        self.album = album
        self.name = name
        self.number = number
        self.path = path
        self.music_playing=False
        pygame.mixer.init()

    def build(self):
        album_entry_box = toga.Box()
        album = toga.Button(self.name, style=Pack(flex=1, height=60, padding=(10, 0, 0, 10)),on_press=self.play)
        album_close = toga.Button("X", style=Pack(height=60, padding=(10, 10, 0, 0)), on_press=self.song_delete)
        album_entry_box.add(album)
        album_entry_box.add(album_close)
        return album_entry_box

    def play(self, what=None):

        if self.album.app.music_playing[1] != False:
            self.album.app.music_playing[1] = False
            self.album.app.albums[self.album.app.music_playing[0][0]].contents[self.album.app.music_playing[0][1]].music_playing = False
            pygame.mixer.music.pause()

        pygame.mixer.music.load(self.path)
        if self.music_playing == False:
            self.music_playing = True
            pygame.mixer.music.play()
            self.album.app.music_playing = [[self.album.number, self.number], True, False]
        else:
            self.music_playing = False
            pygame.mixer.music.pause()
            self.album.app.music_playing = [[None, None], False, False]

    def song_delete(self, what=None):
        pass
