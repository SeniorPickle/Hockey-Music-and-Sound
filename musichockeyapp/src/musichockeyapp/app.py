"""
Plays music and sound effects required during hockey game
"""

import toga
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

class MusicHockeyApp(toga.App):
    def startup(self, what=None):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        box = toga.Box()
        box.style.update(direction=COLUMN)

        add_box = toga.Box(style=Pack(background_color="#686868"))
        music_fill_lable = toga.Label("",style=Pack(flex=1,background_color="#686868"))
        music_import_button = toga.Button("Import", on_press=self._import, style=Pack(text_align=RIGHT,font_size=10,padding=(5,5,5,0)))
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
        try:
            if self.main_window == None:
                pass
        except ValueError:
            self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = box
        self.main_window.show()

    def _import(self, widget):
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
        back_button = toga.Button("Back", on_press=self.startup,style=Pack(width=150, text_align=RIGHT, font_size=10,padding=(5,0,5,0)))

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

            project_dir = os.path.dirname(os.path.abspath(__file__))
            download_dir = os.path.join(project_dir, 'downloadsounds')
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)  # Create the directory if it doesn't exist

            downloaded_audio_path = download_audio_ytdlp(url, save_path=download_dir)
            
            if downloaded_audio_path:
                self.status_label.text = "Trimming audio..."
                output_path = os.path.join(project_dir,"downloadsounds/trimmed_audio.mp3")
                segment_audio(downloaded_audio_path, start_time, end_time, output_path)
                self.status_label.text = f"Audio saved as {output_path}"

        except Exception as e:
            self.status_label.text = f"An error occurred: {e}"
    

def main():
    return MusicHockeyApp()
