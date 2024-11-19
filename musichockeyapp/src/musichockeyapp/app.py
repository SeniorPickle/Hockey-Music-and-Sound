import toga
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack
from album import Album

class HelloWorld(toga.App):
    def startup(self):
        self.albums=[]
        self.add_album_questions = False
        self.main_page()

    def refresh_page(self,content,what=None):
        try:
            if self.main_window == None:
                pass
        except ValueError:
            self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = content
        self.main_window.show()

    def main_page(self, what=None):
        self.box = toga.Box(style=Pack(direction=COLUMN))

        album_add_box = toga.Box(style=Pack(background_color="#686868"))
        album_fill_label = toga.Label("", style=Pack(flex=1, background_color="#686868"))
        album_import_button = toga.Button("Import", style=Pack(text_align=RIGHT, font_size=10, padding=(5, 5, 5, 0)))
        album_add_button = toga.Button("+", style=Pack(text_align=RIGHT, font_size=10, padding=(5, 20, 5, 5)),on_press=self.open_album_questions)
        album_add_box.add(album_fill_label)
        album_add_box.add(album_import_button)
        album_add_box.add(album_add_button)

        album_questions_box = toga.Box(style=Pack(background_color="#7b7b7b"))
        album_questions_label = toga.Label("", style=Pack(flex=1.5, background_color="#7b7b7b"))
        album_questions_answers_box = toga.Box(style=Pack(direction=COLUMN, background_color="#7b7b7b", flex=1))
        album_questions_input_box = toga.Box(style=Pack(background_color="#7b7b7b", padding=(0,0,0,0)))
        album_questions_name_input_title = toga.Label("Album name:", style=Pack(text_align=RIGHT, font_size=10, background_color="#7b7b7b", color="#ffffff", padding = (10, 0, 5, 5)))
        self.album_questions_name_input = toga.TextInput(style=Pack(flex=1, padding=(10, 20, 5, 5)))
        album_questions_input_box.add(album_questions_name_input_title)
        album_questions_input_box.add(self.album_questions_name_input)
        album_questions_answers_box.add(album_questions_input_box)
        album_questions_buttons_box = toga.Box(style=Pack(background_color="#7b7b7b"))
        album_questions_close_button = toga.Button("X", style=Pack(text_align=LEFT, font_size=10, padding=(0, 0, 5, 5)),on_press=self.close_album_questions)
        album_questions_submit_button = toga.Button("Submit",style=Pack(text_align=RIGHT, font_size=10, padding=(0, 20, 5, 5),flex=1),on_press=self.add_album_fun)
        album_questions_buttons_box.add(album_questions_close_button)
        album_questions_buttons_box.add(album_questions_submit_button)
        album_questions_answers_box.add(album_questions_buttons_box)
        album_questions_box.add(album_questions_label)
        album_questions_box.add(album_questions_answers_box)

        album_list_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        for i in range(len(self.albums)):
            album = self.albums[i].build()
            album_list_box.add(album)
        album_list_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, flex=1),content=album_list_box)

        self.sound_board_box = toga.Box(style=Pack(background_color="#686868"))
        self.sound_board_fill_label = toga.Label("", style=Pack(flex=1, background_color="#686868"))
        self.sound_board_button = toga.Button("Sound Board",style=Pack(text_align=RIGHT, font_size=10, padding=(10, 20, 10, 0)))
        self.sound_board_box.add(self.sound_board_fill_label)
        self.sound_board_box.add(self.sound_board_button)

        self.box.add(album_add_box)
        if self.add_album_questions == True:
            self.box.add(album_questions_box)
        self.box.add(album_list_scroll_box)
        self.box.add(self.sound_board_box)

        self.refresh_page(self.box)

    def open_album_questions(self,what=None):

        self.add_album_questions = True
        self.main_page()

    def close_album_questions(self, what=None):
        self.add_album_questions = False
        self.main_page()

    def add_album_fun(self, what=None):

        self.add_album_questions = False

        name=self.album_questions_name_input.value
        self.albums.append(Album(name, self, len(self.albums)))
        self.main_page()

    def delete_album(self, number, what=None):
        self.albums.remove(self.albums[number])
        for i in range(len(self.albums)-number):
            i+=number
            self.albums[i].number-=1
        self.main_page()

def main():
    return HelloWorld("hockey music", "the Smith Project")
