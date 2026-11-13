import os
import tempfile

def create_temp_file(filename: str, content: str) -> str:
    """Creates a temporary file with given content and returns its path."""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path
