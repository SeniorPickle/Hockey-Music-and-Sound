"""
Plays music and sounds
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class HockeyMusicandSound(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        main_box.add(toga.Button('Open window 2', on_press=self.ViewSoundboards))
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def ViewSoundboards(self, widget):
        outer_box = toga.Box()
        self.second_window = toga.Window(title='Second window')
        self.windows.add(self.second_window)
        self.second_window.content = outer_box
        self.second_window.show()
        self.main_window.close()


def main():
    return HockeyMusicandSound()
