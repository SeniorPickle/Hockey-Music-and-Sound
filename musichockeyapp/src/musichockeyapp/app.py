import toga
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack

class HelloWorld(toga.App):
    def startup(self,what=None):

        self.box = toga.Box(style=Pack(direction=COLUMN))

        album_add_box = toga.Box(style=Pack(background_color="#686868"))
        album_fill_label = toga.Label("", style=Pack(flex=1, background_color="#686868"))
        album_import_button = toga.Button("Import", style=Pack(text_align=RIGHT, font_size=10, padding=(5, 5, 5, 0)))
        album_add_button = toga.Button("+",style=Pack(text_align=RIGHT, font_size=10, padding=(5, 20, 5, 5)))
        album_add_box.add(album_fill_label)
        album_add_box.add(album_import_button)
        album_add_box.add(album_add_button)

        album_list_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        example_album = toga.Button("Example Album 1", style=Pack(flex=1, height=60, padding=(10, 10, 0, 10)),on_press=self.open_album)
        album_list_box.add(example_album)
        album_list_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, flex=1),content=album_list_box)

        self.sound_board_box = toga.Box(style=Pack(background_color="#686868"))
        self.sound_board_fill_label = toga.Label("", style=Pack(flex=1, background_color="#686868"))
        self.sound_board_button = toga.Button("Sound Board",style=Pack(text_align=RIGHT, font_size=10, padding=(10, 20, 10, 0)))
        self.sound_board_box.add(self.sound_board_fill_label)
        self.sound_board_box.add(self.sound_board_button)

        self.box.add(album_add_box)
        self.box.add(album_list_scroll_box)
        self.box.add(self.sound_board_box)

        try:
            if self.main_window == None:
                pass
        except ValueError:
            self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.box
        self.main_window.show()


    def open_album(self,widget):

        self.albumn_box = toga.Box(style=Pack(direction=COLUMN))

        music_add_box = toga.Box(style=Pack(background_color="#686868"))
        music_back_button = toga.Button("X",style=Pack(text_align=LEFT,font_size=10,padding=(5,0,5,20)),on_press=self.startup)
        music_add_label = toga.Label("",style=Pack(flex=1,background_color="#686868"))
        music_add_button = toga.Button("+",style=Pack(text_align=RIGHT,font_size=10,padding=(5, 20, 5, 0)))
        music_add_box.add(music_back_button)
        music_add_box.add(music_add_label)
        music_add_box.add(music_add_button)

        music_list_box = toga.Box(style=Pack(direction=COLUMN,flex=1))
        for i in range(20):
            example_music = toga.Button(f"Example Music {i+1}", style=Pack(flex=1,height=30,padding=(10,10,0,10)))
            music_list_box.add(example_music)
        music_list_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, flex=1),content=music_list_box)

        self.albumn_box.add(music_add_box)
        self.albumn_box.add(music_list_scroll_box)
        self.albumn_box.add(self.sound_board_box)

        self.main_window.content = self.albumn_box
        self.main_window.show()


def main():
    return HelloWorld("hockey music", "the Smith Project")