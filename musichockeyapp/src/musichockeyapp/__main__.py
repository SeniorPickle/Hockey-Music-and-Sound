from app import main
import toga
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack

def build(app):
    box = toga.Box()
    box.style.update(direction=COLUMN)

    add_box = toga.Box(style=Pack(background_color="#686868"))
    music_fill_lable = toga.Label("",style=Pack(flex=1,background_color="#686868"))
    music_import_button = toga.Button("Import", style=Pack(text_align=RIGHT, font_size=10,padding=(5,5,5,0)))
    music_add_button = toga.Button("+", style=Pack(text_align=RIGHT, font_size=10, padding=(5,20,5,5)))
    add_box.add(music_fill_lable)
    add_box.add(music_import_button)
    add_box.add(music_add_button)

    music_list_box = toga.Box(style=Pack(direction=COLUMN,flex=1))
    for i in range(20):
        example_song = toga.Button(f"Music Example {i}", style=Pack(height=40,flex=1))
        music_list_box.add(example_song)
    music_list_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, flex=1), content=music_list_box)


    sound_board_box = toga.Box(style=Pack(background_color="#686868"))
    sound_board_fill_label = toga.Label("",style=Pack(flex=1,background_color="#686868"))
    sound_board_button = toga.Button("Sound Board", style=Pack(text_align=RIGHT, font_size=10, padding=(10,20,10,0)))
    sound_board_box.add(sound_board_fill_label)
    sound_board_box.add(sound_board_button)

    box.add(add_box)
    box.add(music_list_scroll_box)
    box.add(sound_board_box)

    return box


def main():
    return toga.App("hockey music", "the Smith Project", startup=build)

if __name__ == "__main__":
    main().main_loop()


if __name__ == "__main__":
    main().main_loop()
