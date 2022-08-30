"""
Module of helper functions to be used through the project
"""
import os
import shutil
from os import listdir


def make_directorytree_if_not_exists(path):
    """
    Ensure a directory path exists

    Args:
        path ([type]): [description]
    """
    if not os.path.exists(path):
        os.makedirs(path)

def get_filename_from_path(filepath: str) -> str:
    """
    Strip the filename from a path eg test.sql from foobar/test.sql

    Args:
        filepath (str): [filename to get name from]

    Returns:
        str: [filename]
    """
    filename = ""

    if "/" in filepath:
        # fmt: off
        filename = filepath[filepath.rindex("/") + 1:]
        # fmt: on
    else:
        filename = filepath

    return filename

def get_filename_from_path_without_extension(filepath: str) -> str:
    """
    Strip the filename and extension from a path eg test from foobar/test.sql

    Args:
        filepath (str): [filename to get name from]

    Returns:
        str: [filename]
    """
    filename = ""

    if "/" in filepath:
        # fmt: off
        filename = filepath[filepath.rindex("/") + 1:]
        # fmt: on
    else:
        filename = filepath

    if "." in filename:
        filename = filename[: filename.rindex(".")]

    return filename


def empty_directory(folder: str) -> str:
    """[summary]

    Args:
        folder (str): [folder to empty]

    Returns:
        None
    """

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def get_files_in_directory(path_to_dir, suffix=".csv"):
    """
    Args:
        path_to_dir (str): [path to scan]
        suffix (str, optional): [extension type to filter for]. Defaults to ".csv".
    Returns:
        list: [filepaths]
    """
    
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]