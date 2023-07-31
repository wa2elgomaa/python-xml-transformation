# *** Utilities ***
from os import makedirs, path, walk
from re import sub, I
from pathlib import Path
from sys import executable
from subprocess import check_call
import filecmp


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


def list_files(dir_path, pattern='*.*'):
    folder = Path(dir_path)
    # Which you can wrap in a list() constructor to materialize
    return list(folder.rglob(pattern))


left_only = []


def list_different_files(src_path, dest_path):
    filecmp.clear_cache()
    dir_comp = filecmp.dircmp(src_path, dest_path)
    for item in dir_comp.left_only:
        file_path = path.join(src_path, item)
        if path.isdir(file_path):
            for base, sub_dirs, files in walk(file_path):
                # print("Folder", base, "exists only in", dir1)
                for file in files:
                    left_only.append(path.join(base, file))
                    # print("File", os.path.join(base, file), "exists only in", dir1)
        else:
            left_only.append(file_path)
            # print('File', path, 'exist only in', dir1)

    # for item in dir_comp.right_only:
    #     file_path = path.join(dest_path, item)
    #     if os.path.isdir(file_path):
    #         for base, subdirs, files in walk(file_path):
    #             print("Folder", base, "exists only in", dest_path)
    #             for file in files:
    #                 print("File", path.join(base, file), "exists only in", dest_path)
    #     else:
    #         print('File', path.join(file_path), 'exist only in', dest_path)

    for SubDirs in dir_comp.common_dirs:
        sub_dir1 = path.join(src_path, SubDirs)
        sub_dir2 = path.join(dest_path, SubDirs)
        list_different_files(sub_dir1, sub_dir2)

    return left_only
