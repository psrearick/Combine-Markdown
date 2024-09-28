import subprocess
import os

def run_combine_markdown(root_folder, yaml_file=None, output_file=None, include_all=False, keep_numbers=False):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to combine_markdown.py
    combine_markdown_path = os.path.join(current_dir, "combine_markdown.py")

    # Start building the command
    command = ["python3", combine_markdown_path, root_folder]

    # Add optional arguments
    if yaml_file:
        command.extend(["-y", yaml_file])
    if output_file:
        command.extend(["-o", output_file])
    if include_all:
        command.append("-a")
    if keep_numbers:
        command.append("-k")

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        print("Markdown combined successfully")
    else:
        print("Error occurred while running combining markdown")
        print("Error message:", result.stderr)
