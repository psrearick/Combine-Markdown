import os
import re
import sys
import argparse

def rename_files(directory, start, digits):
    """Renames files and subdirectories in a given directory with sequential numbers."""

    entries = os.listdir(directory)
    entries.sort()

    for i, entry in enumerate(entries):
        old_path = os.path.join(directory, entry)
        new_name = f"{str(i + start).zfill(digits)} {re.sub(r'^[\d.\s]+', '', entry)}"  # Strip and add numbering
        new_path = os.path.join(directory, new_name)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {entry} -> {new_name}")
        except OSError as e:
            print(f"Error renaming {entry}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Renames files and subdirectories in a given directory with sequential numbers")
    parser.add_argument("-p", "--path", help="Path to directory to rename (default: './')", type=str, default=".")
    parser.add_argument("-s", "--start", help="Starting Number (default: 1)", default=1, type=int)
    parser.add_argument("-d", "--digits", help="Number of digits for numbering (default: 2)", default=2, type=int)
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a valid directory.")
        sys.exit(1)

    rename_files(args.path, args.start, args.digits)
