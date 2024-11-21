import toga
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack

class Album():
    def __init__(self, name, app, number, contents=[]):
        self.formal_name = name
        self.app = app
        self.number = number
        self.contents = contents

    def build(self, what=None):

        album_entry_box = toga.Box()
        album = toga.Button(self.formal_name, style=Pack(flex=1, height=60, padding=(10, 0, 0, 10)), on_press=self.open_album)
        album_close = toga.Button("X", style=Pack(height=60, padding=(10, 10, 0, 0)), on_press=self.album_delete)
        album_entry_box.add(album)
        album_entry_box.add(album_close)
        return album_entry_box

    def album_delete(self, what=None):
        self.app.delete_album(self.number)

    def open_album(self, what=None):
        self.albumn_box = toga.Box(style=Pack(direction=COLUMN))

        music_add_box = toga.Box(style=Pack(background_color="#686868"))
        music_back_button = toga.Button("X", style=Pack(text_align=LEFT, font_size=10, padding=(5, 0, 5, 20)),on_press=self.app.main_page)
        music_add_label = toga.Label(self.formal_name, style=Pack(flex=1, background_color="#686868", color="#ffffff",text_align=CENTER, font_size=20))
        music_add_button = toga.Button("+", style=Pack(text_align=RIGHT, font_size=10, padding=(5, 20, 5, 0)))
        music_add_box.add(music_back_button)
        music_add_box.add(music_add_label)
        music_add_box.add(music_add_button)

        music_list_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        music_list_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, flex=1),content=music_list_box)

        self.albumn_box.add(music_add_box)
        self.albumn_box.add(music_list_scroll_box)
        self.albumn_box.add(self.app.sound_board_box)

        self.app.refresh_page(self.albumn_box)