# *** Utilities ***
from os import makedirs
from re import sub, I
from pathlib import Path
from sys import executable
from subprocess import check_call


def install(package):
    check_call([executable, "-m", "pip", "install", package])


def create_folder(folder_name):
    try:
        makedirs(name=folder_name, exist_ok=True)
    except Exception as e:
        msg = f'--LOG-- ERR CREATING FOLDER {folder_name}'
        print(msg)


def update_body(body):
    text = sub(r'<p><p>', '<br />', body, flags=I)
    text = sub(r'</p>', '<br />', text, flags=I)
    text = sub(r'<p>', '', text, flags=I)
    text = sub(r'&nbsp;', ' ', text)  # because of CDATA
    text = sub(r'<br />', '<p></p>', text)  # because of CDATA
    return f'<p>{text}</p>'


def list_files(dir_path , pattern='*.*'):
    folder = Path(dir_path)
    # Which you can wrap in a list() constructor to materialize
    return list(folder.rglob(pattern))

