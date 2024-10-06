import os
import re
import sys

def rename_files(directory):
    """Renames files and subdirectories in a given directory with sequential numbers."""

    entries = os.listdir(directory)
    entries.sort()

    for i, entry in enumerate(entries):
        old_path = os.path.join(directory, entry)
        new_name = f"{str(i + 1).zfill(2)} {re.sub(r'^[\d.\s]+', '', entry)}"  # Strip and add numbering
        new_path = os.path.join(directory, new_name)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {entry} -> {new_name}")
        except OSError as e:
            print(f"Error renaming {entry}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python number_directory.py [directory_path]")
        sys.exit(1)

    target_directory = sys.argv[1] if len(sys.argv) == 2 else "."  # Default to current directory

    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        sys.exit(1)

    rename_files(target_directory)
