import os, subprocess

def click_on_file(filename):
    try:
        os.startfile(filename)
    except AttributeError:
        subprocess.call(['open', filename])

with open('./favorites.txt', 'r') as f:
    for line in f:
        print(f'Overture de : {line}...')
        click_on_file(line.replace('/','\\').rstrip())
