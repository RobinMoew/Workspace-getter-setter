import PySimpleGUIQt as sg
import os
import json


class Listbox(sg.Listbox):

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        data = window['PATH_LISTBOX'].get_list_values()
        items = [str(v) for v in e.mimeData().text().strip().split('\n')]
        items = [path.removeprefix('file:///') for path in items]
        items = list(set(items) - set(data))
        data.extend(items)
        window['PATH_LISTBOX'].update(data)
        window.refresh()

    def doubleClickEvent(self, e):
        if 'PATH_LISTBOX' == self.Key:
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


def checkWorkspace():
    pass


def search(values):
    global path_results
    window['PATH_LISTBOX'].update(values=path_results)

    for root, _, files in os.walk(values['PATH']):
        for file in files:
            file = f'{root}\\{file}'.replace('\\', '/')
            if file not in path_results:
                if values['TERM'].lower() in file.lower():
                    path_results.append(file)
                    window['PATH_LISTBOX'].update(path_results)


def open_file(file_name):
    print('Opening: ' + file_name)
    os.startfile(file_name)


def open_selected():
    for f in window['PATH_LISTBOX'].get():
        open_file(f)


def open_all():
    for f in window['PATH_LISTBOX'].get_list_values():
        open_file(f)


def suppr_selected(listbox):
    print(listbox)
    items = window[listbox].get_list_values()
    selectedItems = window[listbox].get()
    items = list(set(items) - set(selectedItems))
    window[listbox].update(items)
    listbox = ''


def addWorkspace():
    global workspaces_results
    window['WORKSPACE_LISTBOX'].update(values=workspaces_results)
    workspace_name = sg.popup_get_text(
        'Nom: ',
        keep_on_top=True
    )
    if workspace_name not in workspaces_results:
        workspaces_results.append(workspace_name)
        window['WORKSPACE_LISTBOX'].update(workspaces_results)


def setWorkspace(workspace, pathList):
    with open(workspace, 'w') as file:
        json.dump(pathList, file, indent=2)


def getWorkspace(workspace):
    with open(workspace, 'w') as file:
        print(file)
        json.dump(file)


path_results = []
workspaces_results = []
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
        sg.Button('-', size=(4, 1), key='SUPPR_WORKSPACE_LISTBOX'),
        sg.Text('', size=(1, 1)),
        sg.Text('Fichiers', size=(47.5, 1)),
        sg.Button('Ouvrir', size=(10, 1), key='OPEN'),
        sg.Button('Ouvrir tout', size=(10, 1), key='OPEN_ALL'),
        sg.Button('Supprimer', size=(10, 1), key='SUPPR_PATH_LISTBOX')
    ],
    [
        Listbox(values=workspaces_results, select_mode=sg.SELECT_MODE_SINGLE, size=(20, 10),
                enable_events=True, key='WORKSPACE_LISTBOX'),
        Listbox(values=path_results, size=(80, 10),
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
window['WORKSPACE_LISTBOX'].enable_double_click()

# main event loop
while True:
    event, values = window.read()
    if event is None:
        break
    if event == 'SEARCH' and 'TERM' != '' and 'PATH' != '':
        search(values)
    if event == 'ADD':
        addWorkspace()
    if event == 'OPEN':
        open_selected()
    if event == 'OPEN_ALL':
        open_all()
    if event == 'SUPPR_PATH_LISTBOX' or event == 'SUPPR_WORKSPACE_LISTBOX':
        suppr_selected(event.removeprefix('SUPPR_'))
    if event == 'WORKSPACE_LISTBOX':
        print(window['WORKSPACE_LISTBOX'].get())
        # getWorkspace(values['WORKSPACE_LISTBOX'])
