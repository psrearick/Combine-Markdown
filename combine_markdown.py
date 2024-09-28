import os
import re
import argparse
import yaml

def remove_leading_number(title):
    return re.sub(r'^\d+\s+', '', title)

def get_content_for_path(item_path, depth = 1, custom_title=None, keep_numbers=False):
    with open(item_path, 'r') as f:
        content = f.read()

    existing_title_match = re.match(r'^# (.+)$', content, re.MULTILINE)

    new_title = os.path.splitext(os.path.basename(item_path))[0]
    if custom_title:
        new_title = custom_title
    elif existing_title_match:
        new_title = existing_title_match.group(1)

    if not keep_numbers:
        new_title = remove_leading_number(new_title)

    content = re.sub(r'^# .+\n', '', content, count=1, flags=re.MULTILINE)
    content = f"# {new_title}\n\n{content.strip()}\n"

    for i in range(6, 0, -1):
        search_pattern = rf'^{"#" * i} (.+)$'
        def replace_func(match):
            title = match.group(1)
            if not keep_numbers:
                title = remove_leading_number(title)
            return f'{"#" * (i + depth)} {title}'
        content = re.sub(search_pattern, replace_func, content, flags=re.MULTILINE)

    return f"\n{content}"

def process_folder(folder_path, depth=1, item_order=None, include_all=False, keep_numbers=False):
    output = []
    processed_items = set()

    if item_order:
        for item in item_order:
            sub_item_order = None
            item_name = item
            custom_title = None

            if isinstance(item, dict):
                item_name, item_value = next(iter(item.items()))
                if isinstance(item_value, str):
                    custom_title = item_value
                elif isinstance(item_value, list):
                    order_list = list()
                    for sub_item in item_value:
                        if isinstance(sub_item, dict) and 'order' in sub_item:
                            sub_item_order = sub_item['order']
                        elif isinstance(sub_item, dict) and 'title' in sub_item:
                            custom_title = sub_item['title']
                        elif isinstance(sub_item, str):
                            order_list.append(sub_item)
                    if len(order_list) > 0 and sub_item_order == None:
                        sub_item_order = order_list

            item_path = os.path.join(folder_path, item_name)
            processed_items.add(item_name)

            if os.path.isdir(item_path):
                folder_title = custom_title or item_name
                if not keep_numbers:
                    folder_title = remove_leading_number(folder_title)
                output.append(f"\n{'#' * (depth + 1)} {folder_title}\n")
                output.extend(process_folder(item_path, depth + 1, sub_item_order))
            elif item_name.endswith('.md') and os.path.isfile(item_path):
                output.append(get_content_for_path(item_path, depth, custom_title))

        if include_all:
            all_items = sorted(os.listdir(folder_path))
            for item in all_items:
                if item not in processed_items:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        output.append(f"\n{'#' * (depth + 1)} {item}\n")
                        output.extend(process_folder(item_path, depth + 1, None, include_all))
                    elif item.endswith('.md') and os.path.isfile(item_path):
                        output.append(get_content_for_path(item_path, depth))

    return output

def main():
    parser = argparse.ArgumentParser(description="Combine Markdown files from a folder hierarchy.")
    parser.add_argument("path", help="Path to the root directory")
    parser.add_argument("-o", "--output", help="Output file name (default: directory_name.md)")
    parser.add_argument("-y", "--yaml", help="Path to the YAML order file (default: order.yaml in root directory)")
    parser.add_argument("-a", "--all", action="store_true", help="Include all markdown files, even those not in the YAML file")
    parser.add_argument("-k", "--keep-numbers", action="store_true", help="Keep leading numbers in titles")

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
        root_title = root_folder_name if args.keep_numbers else remove_leading_number(root_folder_name)
        f.write(f"# {root_title}\n")
        f.writelines(process_folder(root_folder, item_order=item_order if order_config else None, include_all=args.all, keep_numbers=args.keep_numbers))

if __name__ == '__main__':
    main()
