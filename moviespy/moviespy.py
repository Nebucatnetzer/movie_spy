#!/usr/bin/python3


"""
Movie Spy Is a programm to quickly collect all personal information
from a computer. Ideally run from a live USB stick. The name comes
from the fact that in movies spies can just quickly insert a USB key
and get all the important data.

Usage:
  moviespy <source> <destination>
  moviespy (-h | --help)
  moviespy --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

import os
import fnmatch
from shutil import copy2
import time

from docopt import docopt
import jpgSorter
import numberOfFilesPerFolderLimiter as max_files_per_folder


file_types = {
    'movies': ['mp4', 'mkv'],
    'documents': ['docx', 'xlsx', 'txt', 'doc', 'xls', 'pdf', 'odt', 'ods'],
    'pictures': ['jpg', 'png', 'gif'],
    'keys': ['key', 'kdbx', 'kdb', 'gpg']
}
maxNumberOfFilesPerFolder = 500
splitMonths = True
minEventDeltaDays = 4


def find(pattern, path):
    result = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result[os.path.join(root, name)] = name
    return result


def find_extensions(extensions, path):
    path_dictionary = {}

    for extension in extensions:
        extension_wildcard = "*." + extension
        files = find(extension_wildcard, path)
        path_dictionary[extension] = files
    return path_dictionary


def copy_files(extensions, search_path, dest):
    path_dictionary = find_extensions(extensions, search_path)

    for file_type, files_by_type in path_dictionary.items():
        if files_by_type:
            path = os.path.join(dest, file_type)
            if not os.path.exists(path):
                os.makedirs(path)

        for file in files_by_type.items():
            if not os.path.islink(file):
                try:
                    copy2(file, path)
                except Exception as e:
                    print(e)
                    continue


def sort_jpgs(location):
    jpgSorter.postprocessImages(location,
                                minEventDeltaDays,
                                splitMonths)


if __name__ == '__main__':
    start_time = time.time()
    arguments = docopt(__doc__, version='Movie Spy v1.0')
    source = arguments['<source>']
    destination = arguments['<destination>']

    for file_type, extensions in file_types.items():
        type_destination = os.path.join(arguments['<destination>'], file_type)
        if not os.path.exists(type_destination):
            os.makedirs(type_destination)
        copy_files(extensions, source, type_destination)
        if 'jpg' in extensions:
            sort_jpgs(os.path.join(destination, type_destination, "jpg"))

    max_files_per_folder.limitFilesPerFolder(destination,
                                             maxNumberOfFilesPerFolder)

    print("--- %s seconds ---" % (time.time() - start_time))




