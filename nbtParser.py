import os
from nbtlib import File

def parse_nbt_file(file_path):
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return None

    try:
        nbt_file = File.load(file_path, gzipped=True)
        return nbt_file
    except Exception as e:
        print(f"Error parsing NBT file: {e}")
        return None