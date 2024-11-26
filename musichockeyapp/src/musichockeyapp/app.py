"""
Plays music and sound effects required during hockey game
"""

import toga
from toga import App, paths
from toga.style import Pack
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack
import re
import yt_dlp
from pydub import AudioSegment
import subprocess
import traceback
import os
from album import Album
import pygame
import time
from time import sleep
import asyncio


# Check if ffmpeg is installed
def is_ffmpeg_installed():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def download_audio_ytdlp(url, save_path='.'):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Use best audio format
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Save with title as filename
            'noplaylist': True,  # Don't download playlists, only the single video

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print(f"Audio downloaded to {info_dict['title']}.{info_dict['ext']}")
            return f"{save_path}/{info_dict['title']}.{info_dict['ext']}"
            print(f"{save_path}/{info_dict['title']}.{info_dict['ext']}")
    except Exception as e:
        print(f"An error occurred during download: {e}")
        traceback.print_exc()
        return None

def segment_audio(input_path, start_time_ms, end_time_ms, output_path):
    try:
        # Load the audio file (in mp4 format if downloaded using pytube)
        audio = AudioSegment.from_file(input_path)

        # Trim the audio between start and end time (in milliseconds)
        segment = audio[start_time_ms:end_time_ms]

        # Export the segmented audio to a new file
        segment.export(output_path, format="mp3")
        print(f"Segmented audio saved to {output_path}")
    except Exception as e:
        print(f"An error occurred during audio segmentation: {e}")

class MusicHockeyApp(App):
    def startup(self):
        
        """
        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        
        project_dir = self.paths.data
        album_dir = os.path.join(project_dir, 'albums')
        if not os.path.exists(album_dir):
                os.makedirs(album_dir)

        self.albums=[]
        for entry in os.scandir(album_dir):
            if entry.is_dir():
                specific_album_dir=os.path.join(album_dir, entry.name)
                self.albums.append(Album(entry.name, self, len(self.albums), specific_album_dir))
        project_dir = self.paths.data
        album_dir = os.path.join(project_dir, 'albums')
        if not os.path.exists(album_dir):
                os.makedirs(album_dir)
        
        self.sound_board_open = False
        self.current_page = None
        self.add_album_questions = False
        self.music_playing = [[None,None],False, False]
        self.start_time = time.time()
        self.main_page()
        asyncio.create_task(self.loop_fun())
        
    def refresh_page(self,content,what=None):
        try:
            if self.main_window == None:
                pass
        except ValueError:
            self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = content
        self.main_window.show()

    def _import(self, album_iteration, widget):
        self.current_page= "_import"
        self.temp_album_iteration=album_iteration

        width, height = self.main_window.size
        import_box_outer = toga.Box(style=Pack(direction=COLUMN))

        first_box = toga.Box(style=Pack(direction=COLUMN, width=150, padding=(5,0,5,width/2-75)))

        self.youtube_url_input = toga.TextInput(style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))
        self.youtube_url_input.placeholder = "Youtube Url"

        self.song_name_input = toga.TextInput(placeholder="Name", style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))

        second_box= toga.Box(style=Pack(width=150, padding=(5,0,-5,width/2-150)))

        self.start_time_input = toga.TextInput(style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))
        self.start_time_input.placeholder = "Start Time (sec)"
        self.end_time_input = toga.TextInput(style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))
        self.end_time_input.placeholder = "End Time (sec)"

        third_box= toga.Box(style=Pack(direction=COLUMN, width=150, padding=(5,0,5,width/2-75)))

        youtube_url_submit = toga.Button("Submit", on_press=self.download_and_trim, style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))
        self.status_label = toga.Label(text="", style=Pack(width=300))
        back_button = toga.Button("Back", on_press=self.albums[self.temp_album_iteration].open_album,style=Pack(width=150, text_align=RIGHT, font_size=10,padding=(5,0,5,0)))

        import_box_outer.add(first_box)
        import_box_outer.add(second_box)
        import_box_outer.add(third_box)
        first_box.add(self.youtube_url_input)
        first_box.add(self.song_name_input)
        second_box.add(self.start_time_input)
        second_box.add(self.end_time_input)
        third_box.add(youtube_url_submit)
        third_box.add(self.status_label)
        third_box.add(back_button)

        self.main_window.content = import_box_outer
        self.main_window.show()

    def download_and_trim(self, widget):
        url = self.youtube_url_input.value
        try:
            start_time = int(self.start_time_input.value) * 1000 if self.start_time_input.value else 0  # Convert to milliseconds
            end_time = int(self.end_time_input.value) * 1000 if self.end_time_input.value else 60000  # Convert to milliseconds, default 1 min

            # Check ffmpeg installation
            if not is_ffmpeg_installed():
                self.status_label.text = "FFmpeg is not installed. Please install it."
                return
            self.status_label.text = "Downloading audio..."

            project_cache_dir = self.paths.cache
            download_webm_dir = os.path.join(project_cache_dir, 'downloadsounds')
            if not os.path.exists(download_webm_dir):
                os.makedirs(download_webm_dir)  # Create the directory if it doesn't exist
            print(download_webm_dir)

            downloaded_audio_path = download_audio_ytdlp(url, save_path=download_webm_dir)

            if downloaded_audio_path:
                self.status_label.text = "Trimming audio..."

                # Extract the video title (without extension) to use as the output file name
                video_title = os.path.splitext(os.path.basename(downloaded_audio_path))[0]
                
                # Create the output path using the video title
                project_dir = self.paths.data
                albums_dir = os.path.join(project_dir, 'albums')
                album_dir = os.path.join(albums_dir, self.albums[self.temp_album_iteration].formal_name)
                if not os.path.exists(album_dir):
                    os.makedirs(album_dir)  # Create the directory if it doesn't exist
                self.albums[self.temp_album_iteration].add_music(self.song_name_input.value, album_dir)

                output_path = os.path.join(album_dir, f"{self.song_name_input.value}.mp3")

                # Segment the audio (cut it based on start and end time)

                segment_audio(downloaded_audio_path, start_time, end_time, output_path)
                # Update the status

                self.status_label.text = f"Audio saved as {output_path}"

        except Exception as e:
            self.status_label.text = f"An error occurred: {e}"

    def main_page(self, what=None):

        self.current_page= "main_page"

        #these are border lines cant reuse them for some reason
        self.black_line_border_box1 = toga.Box(style=Pack(height=4,background_color="#000000"))
        self.black_line_border_box2 = toga.Box(style=Pack(height=4, background_color="#4e4e4e"))
        self.black_line_border_box3 = toga.Box(style=Pack(height=4, background_color="#4e4e4e"))
        self.black_line_border_box4 = toga.Box(style=Pack(height=4, background_color="#000000"))


         #this is the top bar that contains the add and import button
        self.album_add_box = toga.Box(style=Pack(background_color="#800000"))
        album_fill_label = toga.Label("", style=Pack(flex=1, background_color="#800000"))
        album_add_button = toga.Button("+", style=Pack(text_align=RIGHT, font_size=10, padding=(5, 20, 5, 5)),on_press=self.open_album_questions)
        self.album_add_box.add(album_fill_label)
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

        album_list_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#ffffff"))
        for i in range(len(self.albums)):
            album = self.albums[i].build()
            album_list_box.add(album)
        self.album_list_scroll_box = toga.ScrollContainer(vertical=True, style=Pack(direction=COLUMN, flex=1),content=album_list_box)

        #this is the soundboard box that can open
        self.sound_board_box = toga.Box(style=Pack(background_color="#808080"))
        #blank presets
        self.sound_board_button_1 = toga.Button("1", style=Pack(padding=(15, 5, 15, 20)))
        self.sound_board_button_2 = toga.Button("2", style=Pack(padding=(15, 5, 15, 10)))
        self.sound_board_button_3 = toga.Button("3", style=Pack(padding=(15, 5, 15, 10)))
        self.sound_board_button_4 = toga.Button("4", style=Pack(padding=(15, 5, 15, 10)))
        self.sound_board_button_5 = toga.Button("5", style=Pack(padding=(15, 5, 15, 10)))
        self.sound_board_button_6 = toga.Button("6", style=Pack(padding=(15, 5, 15, 10)))
        self.sound_board_button_7 = toga.Button("7", style=Pack(padding=(15, 5, 15, 10)))
        self.sound_board_button_8 = toga.Button("8", style=Pack(padding=(15, 5, 15, 10)))
        self.sound_board_box.add(self.sound_board_button_1)
        self.sound_board_box.add(self.sound_board_button_2)
        self.sound_board_box.add(self.sound_board_button_3)
        self.sound_board_box.add(self.sound_board_button_4)
        self.sound_board_box.add(self.sound_board_button_5)
        self.sound_board_box.add(self.sound_board_button_6)
        self.sound_board_box.add(self.sound_board_button_7)
        self.sound_board_box.add(self.sound_board_button_8)
        self.sound_board_scroll_box = toga.ScrollContainer(horizontal=True, vertical=False, style=Pack(direction=COLUMN, height=60, background_color="#6f6cf6"),content=self.sound_board_box)

        self.redefine_persistent_box()

        self.refresh_box()

    def redefine_persistent_box(self):

        #this really needs to be reorganized it looks like shit
        # this is the bottom box that holds the sound board button

        self.persistent_box = toga.Box(style=Pack(background_color="#800000"))

        self.persistent_fill_label = toga.Label("", style=Pack(flex=1, background_color="#800000"))

        self.song_info_box = toga.Box(style=Pack(direction=COLUMN, background_color="#630000", width=175))

        self.song_name_box = toga.Box(style=Pack(flex=1,background_color="#630000"))

        self.song_manipulation_box = toga.Box(style=Pack(flex=1, background_color="#630000"))


        self.song_manipulation_label1 = toga.Label("", style=Pack(flex=1, background_color="#630000"))
        self.last_song_button = toga.Button("<", style=Pack(font_size=7, padding=(10, 10, 0, 30)), on_press=self.last_song_button_fun)
        self.play_pause_button = toga.Button("|>", style=Pack(font_size=7, padding=(10, 10, 0, 0)), on_press=self.play_pause_button_fun)
        self.next_song_button = toga.Button(">", style=Pack(font_size=7, padding=(10, 30, 0, 0)), on_press=self.next_song_button_fun)
        self.song_manipulation_label2 = toga.Label("", style=Pack(flex=1, background_color="#630000"))


        self.name_spaceing_label1 = toga.Label("", style=Pack(flex=1, background_color="#630000"))
        if self.music_playing[0] == [None,None]:
            self.song_name_label = toga.Label("Nothing Playing", style=Pack(flex=1, font_size=10, padding=(3, 0, 10, 0),background_color="#630000"))
        else:
            self.song_name_label = toga.Label(self.albums[self.music_playing[0][0]].contents[self.music_playing[0][1]].name, style=Pack(flex=1, font_size=10, padding=(3, 0, 10, 0), background_color="#630000"))
        self.name_spaceing_label2 = toga.Label("", style=Pack(flex=1, background_color="#630000"))


        self.song_manipulation_box.add(self.song_manipulation_label1)
        self.song_manipulation_box.add(self.last_song_button)
        self.song_manipulation_box.add(self.play_pause_button)
        self.song_manipulation_box.add(self.next_song_button)
        self.song_manipulation_box.add(self.song_manipulation_label2)

        self.song_name_box.add(self.name_spaceing_label1)
        self.song_name_box.add(self.song_name_label)
        self.song_name_box.add(self.name_spaceing_label2)

        self.song_info_box.add(self.song_manipulation_box)
        self.song_info_box.add(self.song_name_box)

        self.persistent_fill_label2 = toga.Label("", style=Pack(flex=.5, background_color="#800000"))
        self.persistent_sound_board_button = toga.Button("Sound Board", style=Pack(text_align=RIGHT, font_size=10,padding=(10, 20, 10, 0)), on_press=self.toggle_sound_board)

        self.persistent_box.add(self.persistent_fill_label)
        self.persistent_box.add(self.song_info_box)
        self.persistent_box.add(self.persistent_fill_label2)
        self.persistent_box.add(self.persistent_sound_board_button)

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
        self.box.add(self.persistent_box)

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
        if len(name) > 25:
            name = name[:25] + "..."

        project_dir = self.paths.data
        album_dir = os.path.join(project_dir, 'albums')
        specific_album_dir = os.path.join(album_dir, name)
        os.makedirs(specific_album_dir)

        self.albums.append(Album(name, self, len(self.albums), specific_album_dir))
        
        project_dir = self.paths.data
        new_album_dir = os.path.join(project_dir, f'albums\\{name}')
        if not os.path.exists(new_album_dir):
                os.makedirs(new_album_dir)
        else:
            pass
        
        self.main_page()

    def delete_album(self, number, what=None):

        try:
            project_dir = self.paths.data
            album_dir = os.path.join(project_dir, 'albums')
            target_dir = os.path.join(album_dir, self.albums[number].formal_name)
            os.remove(target_dir)
        except(PermissionError, FileNotFoundError):
            print('perm error')
            pass
        
        self.albums.remove(self.albums[number])

        for i in range(len(self.albums)-number):
            i+=number
            self.albums[i].number-=1
        self.main_page()

    def toggle_sound_board(self, what=None):
        if self.sound_board_open == False:
            self.sound_board_open = True
        else:
            self.sound_board_open = False
        if self.current_page == "main_page":
            self.main_page()
        else:
            self.albums[0].refresh_album_box()

    def play_pause_button_fun(self,what=None):
        try:
            if self.music_playing[0] != [None,None]:
                self.albums[self.music_playing[0][0]].contents[self.music_playing[0][1]].play(None, True)
            else:
                pass
        except TypeError:
            pass

    def next_song_button_fun(self, what=None):
        if self.music_playing[1] == True:
            self.albums[self.music_playing[0][0]].contents[self.music_playing[0][1]].forward_play()

    def last_song_button_fun(self, what=None):
        if self.music_playing[1] == True:
            self.albums[self.music_playing[0][0]].contents[self.music_playing[0][1]].back_play()

    async def loop_fun(self, what=None):
        #put all loop tasks in here
        while True:
            if self.music_playing[1] == True:
                self.albums[self.music_playing[0][0]].contents[self.music_playing[0][1]].check_music_playing()
            await asyncio.sleep(1)



def main():
    return MusicHockeyApp("hockey music", "The smith project")
