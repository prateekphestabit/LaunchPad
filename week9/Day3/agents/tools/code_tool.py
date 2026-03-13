import subprocess
import sys
import os

def execute_python_file(filepath: str) -> str:
    """Executes an existing Python (.py) file and returns its stdout output and any errors.
    Provide a relative or absolute path to the .py file."""
    full_path = os.path.abspath(filepath)

    if not os.path.exists(full_path):
        return f"Error: File '{filepath}' not found at '{full_path}'."

    if not full_path.endswith(".py"):
        return f"Error: '{filepath}' is not a Python file. Only .py files can be executed."

    try:
        result = subprocess.run(
            [sys.executable, full_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
        return output if output else "Script executed successfully with no output."
    except subprocess.TimeoutExpired:
        return "Error: Script execution timed out after 30 seconds."
    except Exception as e:
        return f"Error executing file: {str(e)}"
