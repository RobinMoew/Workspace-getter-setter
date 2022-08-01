import os


class OpenFile:
    def __init__(self, window):
        self.window = window

    def open_file(self, file_name):
        self.window['INFO'].update(
            'Info: Ouverture du fichier: ' +
            file_name, text_color='blue'
        )
        os.startfile(file_name)

    def open_selected(self):
        for f in self.window['PATH_LISTBOX'].get():
            self.open_file(f)

    def open_all(self):
        for f in self.window['PATH_LISTBOX'].get_list_values():
            self.open_file(f)
