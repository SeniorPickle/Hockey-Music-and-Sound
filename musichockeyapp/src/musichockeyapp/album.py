import toga
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack

class Album():
    def __init__(self, name, app, number, path, contents=[]):
        self.formal_name = name
        self.app = app
        self.number = number
        self.path = path
        self.contents = contents

    def build(self, what=None):

        album_entry_box = toga.Box()
        album = toga.Button(self.formal_name, style=Pack(flex=1, height=60, padding=(10, 0, 0, 10)), on_press=self.open_album)
        album_close = toga.Button("X", style=Pack(height=60, padding=(10, 10, 0, 0)), on_press=self.album_delete)
        album_entry_box.add(album)
        album_entry_box.add(album_close)
        return album_entry_box

    def import_funnel(self,widget):
        self.app._import(self.number, widget)

    def album_delete(self, what=None):
        self.app.delete_album(self.number)

    def open_album(self, what=None):

        self.app.current_page = "open_album"

        self.music_add_box = toga.Box(style=Pack(background_color="#800000"))
        music_back_button = toga.Button("X", style=Pack(text_align=LEFT, font_size=10, padding=(5, 0, 5, 20)),on_press=self.app.main_page)
        music_add_label = toga.Label(self.formal_name, style=Pack(flex=1, background_color="#800000", color="#ffffff",text_align=CENTER, font_size=15))
        music_add_button = toga.Button("+", style=Pack(text_align=RIGHT, font_size=10, padding=(5, 20, 5, 0)),on_press=self.import_funnel)
        self.music_add_box.add(music_back_button)
        self.music_add_box.add(music_add_label)
        self.music_add_box.add(music_add_button)

        music_list_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.music_list_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, flex=1),content=music_list_box)

        self.refresh_album_box()


    def refresh_album_box(self, what=None):
        self.albumn_box = toga.Box(style=Pack(direction=COLUMN))

        self.albumn_box.add(self.music_add_box)
        self.albumn_box.add(self.app.black_line_border_box1)
        self.albumn_box.add(self.music_list_scroll_box)
        if self.app.sound_board_open == True:
            self.albumn_box.add(self.app.black_line_border_box3)
            self.albumn_box.add(self.app.sound_board_scroll_box)
        self.albumn_box.add(self.app.black_line_border_box4)
        self.albumn_box.add(self.app.sound_board_button_box)

        self.app.refresh_page(self.albumn_box)