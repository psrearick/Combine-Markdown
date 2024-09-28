from run_combine_markdown import run_combine_markdown
import argparse

def main():
    parser = argparse.ArgumentParser(description="Combine Markdown files for The Modular Five.")
    parser.add_argument("-c", "--category", help="Root Folder")
    parser.add_argument("-i", "--item", help="Item")
    args = parser.parse_args()

    category = args.category
    item = args.item
    root = "/Users/philliprearick/Home-Local/Active/Personal/Writing/The Modular Five/Version 2/Source"
    source_path = f"{root}/Comprehensive Reference/{category}"
    output_path = f"{root}/Combination"

    source_path = f"{source_path}/{item}" if item else source_path

    run_combine_markdown(
        "/Users/philliprearick/Home-Local/Active/Personal/Writing/The Modular Five/Version 2/Source/Comprehensive Reference/Items",
        # yaml_file="/path/to/your/order.yaml",
        output_file="/Users/philliprearick/Home-Local/Active/Personal/Writing/The Modular Five/Version 2/Combination",
        include_all=True,
        keep_numbers=False
    )

if __name__ == '__main__':
    main()
