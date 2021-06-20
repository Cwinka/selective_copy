import os
import shutil
import sys
from collections import defaultdict
# import pathlib

home = os.getcwd()

options ={
    '-i': ["jpeg", "jpg", "tiff", "gif", "bmp", "png", "bpg", "svg",
               "heif", "psd"], #  images
    '-t': ["txt", "in", "out"], #  plain text
    '-a': [],
}
sfg = """
You can choose the following modes:

-i      for images

-t      for plain text fiels

-a      allows you to add some extensions for searching (through spaces)
"""
ost = """
Flags: 
-d      by default it searches in the current directory,
        but if this flag is specified it goes iteratively
        through all directories below, including current
        """
def print_modes():
    print(sfg)
    print(ost)

def parse_args():
    all_extensions = defaultdict(str)
    args = [x for x in sys.argv[1:] if x != '-d']
    if not args:
        print()
        print('You need chooce at least one mode!')
        print_modes()
        exit()
    prev_opt = None
    for i in range(len(args)):
        opt = args[i]
        if '-' in opt:
            prev_opt = opt
        try:
            all_extensions[opt] = options[opt]
        except KeyError:
            try:
                all_extensions[prev_opt].append(opt)
            except AttributeError:
                print(f'Curent option {prev_opt} does not appear in the list of available options')
                print(f'Avlailable options: {" ".join(options.keys())}')
                exit()
            continue
    return all_extensions

def make_bucket_folder():
    folder_name = 'FoUnD FiLeS _'
    if not os.path.exists(os.path.join(home, folder_name)):
        os.mkdir(folder_name)
    return folder_name

def deep_search(extentions):
    ext = [val for x in extentions.values() for val in x]
    folder_name = make_bucket_folder()
    found = 0
    for path_to_dir, sub_dirs, filenames in os.walk(home):
        
        if folder_name in path_to_dir:
            continue
        print(f'Check {path_to_dir}')
        for file_ in filenames:
            *_, file_ext = file_.split('.')
            if file_ext in ext:
                found += 1
                from_ = os.path.join(home, path_to_dir, file_)
                to = os.path.join(home, folder_name, file_)
                shutil.copyfile(from_, to)
    try:
        os.rmdir(folder_name)
    except OSError:
        pass

    if not found:
        print('Sorry, but nothing was found')
    else:
        print('Done')

def search(extentions):
    ext = [val for x in extentions.values() for val in x]
    folder_name = make_bucket_folder()
    found = 0
    print(f'Check {home}')
    for dir_or_file in os.listdir():
        *_, file_ext = dir_or_file.split('.')
        if not file_ext:
            pass
        else:
            if file_ext in ext:
                found += 1
                from_ = os.path.join(home, dir_or_file)
                to = os.path.join(home, folder_name, dir_or_file)
                shutil.copyfile(from_, to)
    try:
        os.rmdir(folder_name)
    except OSError:
        pass
    if not found:
        print('Sorry, but nothing was found')
    else:
        print('Done')

if __name__ == "__main__":
    if '-d' in sys.argv:
        deep_search(parse_args())
    elif '-help' in sys.argv:
        print_modes()
    else:
        search(parse_args())
