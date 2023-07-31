from shutil import rmtree
from argparse import ArgumentParser
from sys import argv
# from watcher import Watcher
from utils import create_folder, list_different_files
from core import XMLUpdator


def main():
    # user inputs
    parser = ArgumentParser(
        prog='XML Script', description='Updating XML files per folder updates')
    parser.add_argument('-debug', nargs='*',
                        help='A folder contains NewsML XML files.')
    parser.add_argument(
        '-i', nargs='*', help='A folder contains NewsML XML files.')
    parser.add_argument(
        '-o', nargs='*', help='Where to save the altered XML files.')

    args = parser.parse_args(args=argv[1:])
    input_folder_args = args.i
    output_folder_args = args.o

    # get the values from the args or user direct input
    input_folder = input_folder_args[0] if input_folder_args is not None and len(input_folder_args) > 0 else input(
        r"Enter the input directory: ")
    output_folder = output_folder_args[0] if output_folder_args is not None and len(output_folder_args) > 0 else input(
        r"Enter the output directory: ")

    # the output folder should not be the watcher will listen to both updates and cause infinite loop
    if output_folder == input_folder:
        raise ValueError(
            'Output directory should be different from input folder')
    else:
        create_folder(output_folder)

    # init watcher
    # Watcher(input_folder, output_folder).run()
    files_list = list_different_files(input_folder, output_folder)
    XMLUpdator(input_folder, output_folder).process_files(files_list)


if __name__ == "__main__":
    main()
