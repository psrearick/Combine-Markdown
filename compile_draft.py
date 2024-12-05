import os
import argparse
import yaml

def main():
    parser = argparse.ArgumentParser(description="Compile Draft directory into the Manuscript directory")
    parser.add_argument("-d", "--destination", help="Path to the destination directory relative to current working directory (default: './Manuscript')")
    parser.add_argument("-s", "--source", help="Path to the source directory relative to the current working directory (default: ./Draft)")

    args = parser.parse_args()

    source = os.path.normpath(os.path.join(os.getcwd(), "Draft" if args.source is None else args.source))
    destination = os.path.normpath(os.path.join(os.getcwd(), "Manuscript" if args.destination is None else args.destination))

    try:
        os.rmdir(destination)
    except OSError as error:
        print("Directory '% s' can not be removed" % destination)


if __name__ == '__main__':
    main()
