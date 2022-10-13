import os
import string
import shutil
import win32con
import win32api

icon_folder = "./ico-png"
output_folder = "./output"
ico_png_pair = False
fav_name = "l3043y"

FILE_ATTRIBUTE_READONLY = 0x01
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
FILE_ATTRIBUTE_DIRECTORY = 0x10
FILE_ATTRIBUTE_ARCHIVE = 0x20
FILE_ATTRIBUTE_NORMAL = 0x80
FILE_ATTRIBUTE_TEMPORARY = 0x0100


class IconFolder:
    def __init__(self, ico_file: os.DirEntry[str], png_file: os.DirEntry[str] = None):
        self.ico_file = ico_file
        self.png_file = png_file

    def __str__(self):
        return f'ico:{self.ico_file.path}, '  # png:{self.png_file.path}

    def __repr__(self):
        return f'ico:{self.ico_file.path}, '  # png:{self.png_file.path}


def create_if_not_exist(path: string):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'{path} is created')
    else:
        print("Clear existing folder in the output directory")
        exit(0)


def set_file_win_attribute(path: string):
    att = FILE_ATTRIBUTE_ARCHIVE | FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
    win32api.SetFileAttributes(path, att)


def create_desktop_ini(path: string):
    desktop_ini_path = os.path.join(path, 'desktop.ini')
    if os.path.exists(desktop_ini_path):
        os.remove(desktop_ini_path)
    with open(desktop_ini_path, 'w') as f:
        f.write('[.ShellClassInfo]\n')
        f.write(f'IconResource=.\\.{fav_name}\\folder_icon.ico,0\n')
        f.write('[ViewState]\n')
        f.write('Mode=\n')
        f.write('Vid=\n')
        f.write('FolderType=Generic\n')
    set_file_win_attribute(desktop_ini_path)


def create_dir(folder_name: string, icon: IconFolder):
    target_path = os.path.join(output_folder, folder_name)
    icon_path = os.path.join(target_path, f'.{fav_name}')

    create_if_not_exist(target_path)
    create_if_not_exist(icon_path)

    shutil.copyfile(icon.ico_file, os.path.join(icon_path, 'folder_icon.ico'))
    set_file_win_attribute(icon_path)
    create_desktop_ini(target_path)

    win32api.SetFileAttributes(target_path, FILE_ATTRIBUTE_READONLY)


if __name__ == "__main__":
    folders = {
        'Telegram': 'telegram',
        'Downloads': 'arktube',
        'Backups': 'sidesync',
        'Documents': 'adobeacrobat'
    }

    icons_dict = {}
    for path in os.scandir(icon_folder):
        if path.is_file():
            [parent_path, filename] = os.path.split(path)
            [basename, extension] = os.path.splitext(filename)
            if ico_png_pair:
                pass
            else:
                if extension.lower() == '.ico':
                    icons_dict[basename] = IconFolder(path)

    for folder_name in folders:
        target_icon = folders[folder_name]
        if target_icon in icons_dict:
            create_dir(folder_name, icons_dict[target_icon])
