import json
import os

import PySimpleGUI as pysg
import PySimpleGUIQt as sg


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
    if [] == window['WORKSPACE_LISTBOX'].get() and [] != window['WORKSPACE_LISTBOX'].get_list_values():
      workspaceName = window['WORKSPACE_LISTBOX'].get_list_values()[-1]
      saveWorkspace(workspaceName)
    elif window['WORKSPACE_LISTBOX'].get():
      workspaceName = window['WORKSPACE_LISTBOX'].get()[0]
      saveWorkspace(workspaceName)

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
  path_results = []


def open_file(file_name):
  window['INFO'].update(
    'Info: Ouverture du fichier: ' +
    file_name, text_color='blue'
    )
  os.startfile(file_name)


def open_selected():
  for f in window['PATH_LISTBOX'].get():
    open_file(f)


def open_all():
  for f in window['PATH_LISTBOX'].get_list_values():
    open_file(f)


def suppr_selected(listbox):
  items = window[listbox].get_list_values()
  selectedItems = window[listbox].get()
  items = list(set(items) - set(selectedItems))
  window[listbox].update(items)
  if 'WORKSPACE_LISTBOX' == listbox and [] != selectedItems:
    workspaces_results.remove(selectedItems[0])
    window['PATH_LISTBOX'].update([])
    window['INFO'].update(
      'Info: "' + selectedItems[0] +
      '" supprimé', text_color='blue'
      )
  listbox = ''


def addWorkspace(workspaceName):
  global workspaces_results
  window['WORKSPACE_LISTBOX'].update(values=workspaces_results)

  if workspaceName not in workspaces_results:
    workspaces_results.append(workspaceName)
    window['WORKSPACE_LISTBOX'].update(workspaces_results)
  else:
    window['INFO'].update(
      'Erreur: "' + workspaceName +
      '" déjà présent dans la liste', text_color='red'
      )


def saveWorkspace(workspace):
  if ('ADD' != event):
    pathList = window['PATH_LISTBOX'].get_list_values()
    data = getJsonFromFile()
    workspaceWithPaths = {workspace: pathList}
    data.update(workspaceWithPaths)
    if ([] == data[workspace]):
      data.pop(workspace, '')
    with open('./workspaces.json', 'w') as file:
      json.dump(data, file)
      file.close()


def getPathsfromWorkspaceName(workspaceName):
  window['PATH_LISTBOX'].update([])
  path_results = []
  data = getJsonFromFile()
  if workspaceName in data:
    for path in data[workspaceName]:
      path_results.append(path)
      window['PATH_LISTBOX'].update(path_results)


def loadWorkspace():
  data = getJsonFromFile()
  workspaces = list(data.keys())
  for workspace in workspaces:
    workspaces_results.append(workspace)
    addWorkspace(workspace)


def getJsonFromFile():
  with open('./workspaces.json', 'r') as file:
    data = json.load(file)
    file.close()
  return data


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
    Listbox(
      values=workspaces_results, select_mode=sg.SELECT_MODE_SINGLE, size=(20, 10),
      enable_events=True, key='WORKSPACE_LISTBOX'
      ),
    Listbox(
      values=path_results, size=(80, 10),
      enable_events=True, key='PATH_LISTBOX'
      )
  ],
  [
    sg.Input(
      'Hello, tu peux commencer à ajouter des workspaces et des fichiers 👽',
      key='INFO', disabled=True, size=(100.4, 1)
      )
  ]
]
add_workspace_popup = [
  [
    sg.Text('Nom', size=(11, 1)),
    sg.Input('', size=(20, 1), key='WORKSPACE_NAME')
  ]
]

window = sg.Window(
  'Work spaces', layout=layout,
  finalize=True, return_keyboard_events=True
  )
window['WORKSPACE_LISTBOX'].enable_double_click()
window['PATH_LISTBOX'].enable_drop()
window['PATH_LISTBOX'].enable_double_click()

loadWorkspace()

try:
  while True:
    event, values = window.read()
    if event is None:
      break
    if event == 'SEARCH' and 'TERM' != '' and 'PATH' != '':
      search(values)
      if window['WORKSPACE_LISTBOX'].get():
        workspaceName = window['WORKSPACE_LISTBOX'].get()[0]
        saveWorkspace(workspaceName)
    if event == 'ADD':
      workspaceName = sg.popup_get_text(
        'Nom: ',
        keep_on_top=True
      )
      if '' != workspaceName:
        addWorkspace(workspaceName)
    if event == 'OPEN':
      open_selected()
    if event == 'OPEN_ALL':
      open_all()
    if event in ('SUPPR_PATH_LISTBOX', 'SUPPR_WORKSPACE_LISTBOX'):
      if window['WORKSPACE_LISTBOX'].get():
        workspaceName = window['WORKSPACE_LISTBOX'].get()[0]
        suppr_selected(event.removeprefix('SUPPR_'))
        saveWorkspace(workspaceName)
    if event == 'WORKSPACE_LISTBOX':
      if window['WORKSPACE_LISTBOX'].get():
        workspaceName = window['WORKSPACE_LISTBOX'].get()[0]
        getPathsfromWorkspaceName(workspaceName)
except Exception as e:
  pysg.popup_error_with_traceback(
    f'T\'as cassé ! Ne ferme pas et donne moi ces infos:', e
  )
