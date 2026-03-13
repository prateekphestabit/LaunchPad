import os
from typing import List

def get_current_directory() -> str:
    """Returns the current working directory path."""
    return os.getcwd()

def create_file(filename: str, content: str) -> str:
    """Creates a file with the given filename and writes content into it.
    Use a relative or absolute path in filename to place it in a specific directory (e.g. 'outputs/test.py').
    The parent directory is created automatically if it does not exist."""
    full_path = os.path.abspath(filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    return f"File created at: {full_path}"

def create_folder(folder_name: str) -> str:
    """Creates a folder with the given name in the current working directory.
    Use a relative or absolute path in folder_name to create it elsewhere (e.g. 'outputs/test_folder')."""
    full_path = os.path.abspath(folder_name)
    os.makedirs(full_path, exist_ok=True)
    return f"Folder created at: {full_path}"

def read_file(filename: str) -> str:
    """Reads and returns the content of a file. Provide a relative or absolute path."""
    full_path = os.path.abspath(filename)
    if not os.path.exists(full_path):
        return f"Error: File '{filename}' not found."
    with open(full_path, "r", errors="replace") as f:
        return f.read()

def list_files(path: str) -> List[str]:
    """Lists all files in the given directory path."""
    target_path = os.path.abspath(path)
    if not os.path.exists(target_path):
        return [f"Error: Path '{path}' not found."]
    files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
    return files if files else ["No files found."]

def list_directories(path: str) -> List[str]:
    """Lists all subdirectories in the given directory path."""
    target_path = os.path.abspath(path)
    if not os.path.exists(target_path):
        return [f"Error: Path '{path}' not found."]
    dirs = [d for d in os.listdir(target_path) if os.path.isdir(os.path.join(target_path, d))]
    return dirs if dirs else ["No directories found."]