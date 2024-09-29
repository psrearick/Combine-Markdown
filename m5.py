from run_combine_markdown import run_combine_markdown
import os
import argparse

def process(category, item, source_type, process_all=False, recursive=False, propagate=False):
    root = "/Users/philliprearick/Home-Local/Active/Personal/Writing/The Modular Five/Version 2"
    output_path = f"{root}/Combination"
    source_path = f"{root}/Source/{source_type}"

    if category:
        output_path = f"{output_path}/{source_type}"
        source_path = f"{source_path}/{category}"
        if item:
            output_path = f"{output_path}/{category}"
            source_path = f"{source_path}/{item}"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if propagate:
        if item:
            process(category, None, source_type, False, False, True)
        elif category:
            process(None, None, source_type, False, False, False)

    if process_all and not item:
        all_items = os.listdir(source_path)
        for sub_item in all_items:
            item_path = os.path.join(source_path, sub_item)
            if os.path.isdir(item_path):
                if category:
                    process(category, sub_item, source_type, False, recursive, False)
                    continue
                process(sub_item, None, source_type, recursive, recursive, False)
        if not recursive:
            return

    run_combine_markdown(
        source_path,
        # yaml_file="/path/to/your/order.yaml",
        output_file=output_path,
        include_all=True,
        keep_numbers=False
    )

def main():
    parser = argparse.ArgumentParser(description="Combine Markdown files for The Modular Five.")
    parser.add_argument("-t", "--type", help="Type")
    parser.add_argument("-c", "--category", help="Category")
    parser.add_argument("-i", "--item", help="Item")
    parser.add_argument("-a", "--all", action="store_true", help="Include all markdown files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Include all markdown files, recursively")
    parser.add_argument("-p", "--propagate", action="store_true", help="Propagate up ancestor tree")
    args = parser.parse_args()

    source_type = args.type if args.type else "Comprehensive Reference"

    process(args.category, args.item, source_type, args.all, args.recursive, args.propagate)

if __name__ == '__main__':
    main()
