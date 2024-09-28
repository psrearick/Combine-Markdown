import os
import re
import argparse
import yaml

def get_content_for_path(item_path, depth = 1):
    with open(item_path, 'r') as f:
        content = f.read()

    if not re.match(r'^# ', content):
        file_name = os.path.splitext(os.path.basename(item_path))[0]
        content = f"# {file_name}\n\n{content}\n"

    for i in range(6, 0, -1):
        search_pattern = rf'^{"#" * i} ' if i > 1 else r'^# '
        replace_pattern = f'{"#" * (i + depth)} '
        content = re.sub(search_pattern, replace_pattern, content, flags=re.MULTILINE)

    return f"\n{content}"

def process_folder(folder_path, depth=1, item_order=None):
    output = []

    if item_order:
        items_to_process = item_order
    else:
        items_to_process = sorted(os.listdir(folder_path))

    for item in items_to_process:
        sub_item_order = None
        item_name = item

        if isinstance(item, dict):
            for k, v in item.items():
                item_name = k
                sub_item_order = v

        item_path = os.path.join(folder_path, item_name)

        if os.path.isdir(item_path):
            output.append(f"\n{'#' * (depth + 1)} {item_name}\n")
            output.extend(process_folder(item_path, depth + 1, sub_item_order))
        elif item_name.endswith('.md') and os.path.isfile(item_path):
            output.append(get_content_for_path(item_path, depth))

    return output

def main():
    parser = argparse.ArgumentParser(description="Combine Markdown files from a folder hierarchy.")
    parser.add_argument("path", help="Path to the root directory")
    parser.add_argument("-o", "--output", help="Output file name (default: directory_name.md)")
    parser.add_argument("-y", "--yaml", help="Path to the YAML order file (default: order.yaml in root directory)")

    args = parser.parse_args()
    root_folder = args.path
    root_folder_name = os.path.basename(os.path.normpath(root_folder))
    output_file = args.output or f"{root_folder_name}.md"

    order_config = None
    item_order = None
    yaml_path = args.yaml or os.path.join(root_folder, 'order.yaml')

    if os.path.exists(yaml_path):
        with open(yaml_path, 'r') as f:
            order_config = yaml.safe_load(f)

    if order_config:
        item_order = order_config.get(root_folder_name)
        if item_order == None:
            item_order = order_config.get("root")

    with open(output_file, 'w') as f:
        f.write(f"# {root_folder_name}\n")
        f.writelines(process_folder(root_folder, item_order=item_order if order_config else None))

if __name__ == '__main__':
    main()
