import PySimpleGUIQt as sg
import os
import json


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
        item = self.QT_ListWidget.itemAt(
            e.pos().x(), e.pos().y()
        )
        if None != item:
            open_file(item.text())

    def enable_drop(self):
        self.Widget.setAcceptDrops(True)
        self.Widget.dragEnterEvent = self.dragEnterEvent
        self.Widget.dragMoveEvent = self.dragMoveEvent
        self.Widget.dropEvent = self.dropEvent

    def enable_double_click(self):
        self.Widget.mouseDoubleClickEvent = self.doubleClickEvent


def search(values):
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


def open_selected():
    for f in window['LISTBOX'].get():
        open_file(f)


def open_all():
    for f in window['LISTBOX'].get_list_values():
        open_file(f)


def suppr_selected():
    items = window['LISTBOX'].get_list_values()
    selectedItems = window['LISTBOX'].get()
    items = list(set(items) - set(selectedItems))
    window['LISTBOX'].update(items)


def addWorkspace():
    workspace_name = sg.popup_get_text(
        'Nom: ',
        keep_on_top=True
    )
    workspaces = window['WORKSPACE_LISTBOX'].get_list_values()


def setWorkspace(workspace, pathList):
    with open(workspace, 'w') as file:
        json.dump(pathList, file, indent=2)


def getWorkspace():
    pass
    # with open(workspace, 'w') as file:
    #     json.dump(pathList, file)


results = []
sg.change_look_and_feel('LightGreen7')
layout = [
    [
        sg.Text('Rechercher', size=(11, 1)),
        sg.Input('', size=(31.18, 1), key='TERM'),
        sg.Text('   dans', size=(5, 1)),
        sg.Input('', size=(31.18, 1), key='PATH'),
        sg.FolderBrowse('Parcourir', size=(10, 1), key='BROWSE'),
        sg.Button('Rechercher', size=(10, 1), key='SEARCH')
    ],
    [
        sg.Text('Workspaces', size=(11, 1)),
        sg.Button('+', size=(4, 1), key='ADD'),
        sg.Button('-', size=(4, 1), key='SUPPR_WORKSPACE'),
        sg.Text('', size=(1, 1)),
        sg.Text('Fichiers', size=(47.5, 1)),
        sg.Button('Ouvrir', size=(10, 1), key='OPEN'),
        sg.Button('Ouvrir tout', size=(10, 1), key='OPEN_ALL'),
        sg.Button('Supprimer', size=(10, 1), key='SUPPR')
    ],
    [
        sg.Listbox(values=results, size=(20, 10),
                   enable_events=True, key='WORKSPACE_LISTBOX'),
        Listbox(values=results, size=(80, 10),
                enable_events=True, key='PATH_LISTBOX')
    ]
]
add_workspace_popup = [
    [
        sg.Text('Nom', size=(11, 1)),
        sg.Input('', size=(20, 1), key='WORKSPACE_NAME')
    ]
]

window = sg.Window('Work spaces', layout=layout,
                   finalize=True, return_keyboard_events=True)
window['PATH_LISTBOX'].enable_drop()
window['PATH_LISTBOX'].enable_double_click()

# main event loop
while True:
    event, values = window.read()
    if event is None:
        break
    if event == 'SEARCH' or event == 'special 16777220' and 'TERM' != '' and 'PATH' != '':
        search(values)
    if event == 'ADD':
        addWorkspace()
    if event == 'OPEN':
        open_selected()
    if event == 'OPEN_ALL':
        open_all()
    if event == 'SUPPR':
        suppr_selected()
