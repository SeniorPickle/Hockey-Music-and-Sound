"""
Plays music and sound effects required during hockey game
"""

import toga
from toga import App, paths
from toga.style import Pack
from toga.style.pack import RIGHT, LEFT, COLUMN, CENTER, ROW, Pack
import re
from googleapiclient.discovery import build
import yt_dlp
from pytube import YouTube
from pydub import AudioSegment
import subprocess
import traceback
import os
from musichockeyapp.album import Album



api_key = 'AIzaSyChY31_cLFs98C-J4-gLv2JASmzTO9DbHo'
youtube = build('youtube', 'v3', developerKey=api_key)

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
                print(entry.name)
                self.albums.append(Album(entry.name, self, len(self.albums)))
        project_dir = self.paths.data
        album_dir = os.path.join(project_dir, 'albums')
        if not os.path.exists(album_dir):
                os.makedirs(album_dir)
        
        self.sound_board_open = False
        self.current_page = None
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

    def _import(self, widget):
        self.current_page= "_import"

        width, height = self.main_window.size
        import_box_outer = toga.Box(style=Pack(direction=COLUMN))

        first_box = toga.Box(style=Pack(direction=COLUMN, width=150, padding=(5,0,5,width/2-75)))

        self.youtube_url_input = toga.TextInput(style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))
        self.youtube_url_input.placeholder = "Youtube Url"

        second_box= toga.Box(style=Pack(width=150, padding=(5,0,-5,width/2-150)))

        self.start_time_input = toga.TextInput(style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))
        self.start_time_input.placeholder = "Start Time (sec)"
        self.end_time_input = toga.TextInput(style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))
        self.end_time_input.placeholder = "End Time (sec)"

        third_box= toga.Box(style=Pack(direction=COLUMN, width=150, padding=(5,0,5,width/2-75)))

        youtube_url_submit = toga.Button("Submit", on_press=self.download_and_trim, style=Pack(width=150, text_align=CENTER,font_size=10,padding=(5,0,5,0)))
        self.status_label = toga.Label(text="", style=Pack(width=300))
        back_button = toga.Button("Back", on_press=self.main_page,style=Pack(width=150, text_align=RIGHT, font_size=10,padding=(5,0,5,0)))

        import_box_outer.add(first_box)
        import_box_outer.add(second_box)
        import_box_outer.add(third_box)
        first_box.add(self.youtube_url_input)
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

            project_dir = self.paths.data
            download_dir = os.path.join(project_dir, 'downloadsounds')
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)  # Create the directory if it doesn't exist

            downloaded_audio_path = download_audio_ytdlp(url, save_path=download_dir)

            if downloaded_audio_path:
                self.status_label.text = "Trimming audio..."

                # Extract the video title (without extension) to use as the output file name
                video_title = os.path.splitext(os.path.basename(downloaded_audio_path))[0]
                
                # Create the output path using the video title
                output_path = os.path.join(download_dir, f"{video_title}_trimmed.mp3")
                
                # Segment the audio (cut it based on start and end time)
                segment_audio(downloaded_audio_path, start_time, end_time, output_path)

                # Update the status
                self.status_label.text = f"Audio saved as {output_path}"

        except Exception as e:
            self.status_label.text = f"An error occurred: {e}"

    def main_page(self, what=None):
        self.current_page= "main_page"

        self.box = toga.Box(style=Pack(direction=COLUMN))

        album_add_box = toga.Box(style=Pack(background_color="#686868"))
        album_fill_label = toga.Label("", style=Pack(flex=1, background_color="#686868"))
        album_import_button = toga.Button("Import", on_press=self._import, style=Pack(text_align=RIGHT, font_size=10, padding=(5, 5, 5, 0)))
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
        self.sound_board_button = toga.Button("Sound Board", on_press=self.toggel_sound_board, style=Pack(text_align=RIGHT, font_size=10, padding=(10, 20, 10, 0)))
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
        
        project_dir = self.paths.data
        new_album_dir = os.path.join(project_dir, f'albums\{name}')
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
    return MusicHockeyApp()