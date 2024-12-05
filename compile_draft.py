import os
import argparse
import shutil

def remove_directory(directory):
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        pass
    except OSError as e:
        print(f"Error: Failed to remove directory '{directory}': {e}")

def copy_directory(source_dir, target_dir):
    try:
        shutil.copytree(source_dir, target_dir)
    except OSError as e:
        print(f"Error: Failed to copy directory '{source_dir}' to '{target_dir}': {e}")

def prevent_headings(target_dir):
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isdir(item_path):
            try:
                with open(os.path.join(item_path, ".no-headings"), 'w') as f:
                    pass
            except OSError as e:
                print(f"Error: Failed to create .no-headings file in '{item_path}': {e}")

def main():
    parser = argparse.ArgumentParser(description="Compile Draft directory into the Manuscript directory")
    parser.add_argument("-d", "--destination", help="Path to the destination directory relative to current working directory (default: './Manuscript')")
    parser.add_argument("-s", "--source", help="Path to the source directory relative to the current working directory (default: ./Draft)")

    args = parser.parse_args()

    source = os.path.normpath(os.path.join(os.getcwd(), "Draft" if args.source is None else args.source))
    destination = os.path.normpath(os.path.join(os.getcwd(), "Manuscript" if args.destination is None else args.destination))

    remove_directory(destination)
    copy_directory(source, destination)
    prevent_headings(destination)

if __name__ == '__main__':
    main()
