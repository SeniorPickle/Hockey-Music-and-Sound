import toga
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack
from album import Album

class HelloWorld(toga.App):
    def startup(self):
        self.albums=[]
        self.add_album_questions = False
        self.sound_board_open = False
        self.current_page = None
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

        self.current_page= "main_page"

        #these are border lines
        self.black_line_border_box1 = toga.Box(style=Pack(height=4,background_color="#000000"))
        self.black_line_border_box2 = toga.Box(style=Pack(height=4, background_color="#4e4e4e"))
        self.black_line_border_box3 = toga.Box(style=Pack(height=4, background_color="#4e4e4e"))
        self.black_line_border_box4 = toga.Box(style=Pack(height=4, background_color="#000000"))

        #this is the top bar that contains the add and import button
        self.album_add_box = toga.Box(style=Pack(background_color="#800000"))
        album_fill_label = toga.Label("", style=Pack(flex=1, background_color="#800000"))
        album_import_button = toga.Button("Import", style=Pack(text_align=RIGHT, font_size=10, padding=(5, 5, 5, 0)))
        album_add_button = toga.Button("+", style=Pack(text_align=RIGHT, font_size=10, padding=(5, 20, 5, 5)),on_press=self.open_album_questions)
        self.album_add_box.add(album_fill_label)
        self.album_add_box.add(album_import_button)
        self.album_add_box.add(album_add_button)

        #this is the box that opens to the top that can add new albums
        self.album_questions_box = toga.Box(style=Pack(background_color="#808080"))
        album_questions_label = toga.Label("", style=Pack(flex=1.5, background_color="#808080"))
        album_questions_answers_box = toga.Box(style=Pack(direction=COLUMN, background_color="#808080", flex=1))
        album_questions_input_box = toga.Box(style=Pack(background_color="#808080", padding=(0,0,0,0)))
        self.album_questions_name_input = toga.TextInput(placeholder="Album Name", style=Pack(flex=1, padding=(10, 20, 5, 5)))
        album_questions_input_box.add(self.album_questions_name_input)
        album_questions_answers_box.add(album_questions_input_box)
        album_questions_buttons_box = toga.Box(style=Pack(background_color="#808080"))
        album_questions_close_button = toga.Button("X", style=Pack(text_align=LEFT, font_size=10, padding=(0, 0, 5, 5)),on_press=self.close_album_questions)
        album_questions_submit_button = toga.Button("Submit",style=Pack(text_align=RIGHT, font_size=10, padding=(0, 20, 5, 5),flex=1),on_press=self.add_album_fun)
        album_questions_buttons_box.add(album_questions_close_button)
        album_questions_buttons_box.add(album_questions_submit_button)
        album_questions_answers_box.add(album_questions_buttons_box)
        self.album_questions_box.add(album_questions_label)
        self.album_questions_box.add(album_questions_answers_box)

        #this is the box that contains albums
        album_list_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#ffffff"))
        for i in range(len(self.albums)):
            album = self.albums[i].build()
            album_list_box.add(album)
        self.album_list_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, flex=1),content=album_list_box)

        #this is the soundboard box that can open
        self.sound_board_box = toga.Box(style=Pack(background_color="#808080"))
        self.sound_board_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, height=60, background_color="#6f6cf6"),content=self.sound_board_box)

        #this is the bottom box that holds the sound board button
        self.sound_board_button_box = toga.Box(style=Pack(background_color="#800000"))
        self.sound_board_button_fill_label = toga.Label("", style=Pack(flex=1, background_color="#800000"))
        self.sound_board_button_button = toga.Button("Sound Board",style=Pack(text_align=RIGHT, font_size=10, padding=(10, 20, 10, 0)),on_press=self.toggel_sound_board)
        self.sound_board_button_box.add(self.sound_board_button_fill_label)
        self.sound_board_button_box.add(self.sound_board_button_button)

        self.refresh_box()

    def refresh_box(self, what=None):
        self.box = toga.Box(style=Pack(direction=COLUMN))

        #this is the compile wherer you add all the parts together
        self.box.add(self.album_add_box)
        self.box.add(self.black_line_border_box1)
        if self.add_album_questions == True:
            self.box.add(self.album_questions_box)
            self.box.add(self.black_line_border_box2)
        self.box.add(self.album_list_scroll_box)
        if self.sound_board_open == True:
            self.box.add(self.black_line_border_box3)
            self.box.add(self.sound_board_scroll_box)
        self.box.add(self.black_line_border_box4)
        self.box.add(self.sound_board_button_box)

        self.refresh_page(self.box)

    def open_album_questions(self,what=None):
        self.add_album_questions = True
        self.refresh_box()

    def close_album_questions(self, what=None):
        self.add_album_questions = False
        self.refresh_box()

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

    def toggel_sound_board(self,what=None):
        if self.sound_board_open == False:
            self.sound_board_open = True
        else:
            self.sound_board_open = False
        if self.current_page == "main_page":
            self.main_page()
        else:
            self.albums[0].refresh_album_box()

def main():
    return HelloWorld("hockey music", "the Smith Project")
