import PySimpleGUIQt as sg
import os


class Listbox(sg.Listbox):

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        data = window['LISTBOX'].get_list_values()
        items = [str(v) for v in e.mimeData().text().strip().split('\n')]
        items = [path.removeprefix('file:///') for path in items]
        items = list(set(items) - set(data))
        data.extend(items)
        window['LISTBOX'].update(data)
        window.refresh()

    def doubleClickEvent(self, e):
        open_file(self.QT_ListWidget.itemAt(e.pos().x(), e.pos().y()).text())

    def enable_drop(self):
        self.Widget.setAcceptDrops(True)
        self.Widget.dragEnterEvent = self.dragEnterEvent
        self.Widget.dragMoveEvent = self.dragMoveEvent
        self.Widget.dropEvent = self.dropEvent

    def enable_double_click(self):
        self.Widget.mouseDoubleClickEvent = self.doubleClickEvent


def search(values, window):
    global results
    window['LISTBOX'].update(values=results)

    for root, _, files in os.walk(values['PATH']):
        for file in files:
            file = f'{root}\\{file}'.replace('\\', '/')
            if file not in results:
                if values['TERM'].lower() in file.lower():
                    results.append(file)
                    window['LISTBOX'].update(results)


def open_file(file_name):
    print('Opening: ' + file_name)
    os.startfile(file_name)


def open_all():
    for f in window['LISTBOX'].get_list_values():
        open_file(f)


results = []
sg.change_look_and_feel('LightGreen7')
layout = [
    [sg.Text('Rechercher', size=(11, 1)), sg.Input(
        '', size=(40, 1), key='TERM')],
    [sg.Text('dans', size=(11, 1)), sg.Input('', size=(40, 1), key='PATH'),
     sg.FolderBrowse('Parcourir', size=(10, 1), key='BROWSE'),
     sg.Button('Rechercher', size=(10, 1), key='SEARCH'),
     sg.Button('Ouvrir tout', size=(10, 1), key='OPEN')],
    [Listbox(values=results, size=(100, 10), enable_events=True, key='LISTBOX')]]

window = sg.Window('Work spaces', layout=layout,
                   finalize=True, return_keyboard_events=True)
window['LISTBOX'].enable_drop()
window["LISTBOX"].enable_double_click()

# main event loop
while True:
    event, values = window.read()
    if event is None:
        break
    if event == 'SEARCH' or event == 'special 16777220' and 'TERM' != '' and 'PATH' != '':
        search(values, window)
    if event == 'LISTBOX':
        pass
        # file_name = values['LISTBOX']
        # if file_name:
        #     open_file(file_name[0])
    if event == 'OPEN':
        open_all()
