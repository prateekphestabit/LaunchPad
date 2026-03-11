import os
from typing import List

def create_file(filename: str, content: str) -> str:
    """Create a file and optionally write content into it."""
    with open(filename, "w") as f:
        f.write(content)
    return f"File {filename} created."

def read_file(filename: str) -> str:
    """Read and return the contents of a file."""
    with open(filename, "r") as f:
        return f.read()

def list_files(path: str = ".") -> List[str]:
    """List files in a directory."""
    return os.listdir(path)