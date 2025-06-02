import eel
import os
import tkinter as tk
from tkinter import filedialog

@eel.expose
def save_temp_file(filename, contents):
    """Save a dropped NC file to the temp directory."""
    try:
        temp_path = os.path.join(os.path.dirname(__file__), '..', 'temp', filename)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, 'w') as f:
            f.write(contents)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@eel.expose
def select_folder():
    """Open a folder selection dialog."""
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory()
    root.destroy()
    return folder
