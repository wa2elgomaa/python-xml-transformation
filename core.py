# *** core ***
import time
from os import makedirs, path
from xml.dom.minidom import parse
from shutil import copy2
from re import sub, escape
from utils import update_body, list_files
from logger import Logger


class XMLUpdator:

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.logger = Logger()

    def update_files(self, files_list):
        # # read list of files in input directory

        for file_path in files_list:
            # delay read and write for 2 seconds
            time.sleep(2)
            # read and edit the file
            output_file_path = sub(escape(f'{self.input_folder}'), escape(f'{self.output_folder}'), str(file_path))
            try:
                if str(file_path).lower().endswith('.xml'):
                    doc = parse(str(file_path))
                    # get the body text and update
                    html_body = doc.getElementsByTagName("body")
                    for child in html_body:
                        text = getattr(child.firstChild, 'data', '')
                        if hasattr(child.firstChild , 'replaceData'):
                            child.firstChild.replaceData(
                                0, len(text), update_body(text))
                        self.logger.log_message(f'EDITED FILE : {file_path} ')

                    # write the updated xml in output directory
                    with open(output_file_path, 'w+', encoding='utf-8') as f:
                        doc.writexml(f)
                        doc.unlink()
                        self.logger.log_message(
                            f"OUTPUT FILE : {output_file_path}")
                else:
                    # make dirs if not exists
                    makedirs(path.dirname(output_file_path), exist_ok=True)
                    # copy the file
                    copy2(file_path, output_file_path)
                    self.logger.log_message(
                        f"COPIED NON-XML FILE : {output_file_path}")

            except Exception as e:
                self.logger.log_message(f'ERROR IN FILE : {file_path}', e)

    def process_files(self, files_list=None):
        if files_list is None:
            files_list = []

        if len(files_list) > 0:
            # update all files in input folder before moving
            self.update_files(files_list)
        else:
            # copy all the files to input folder
            dir_files = list_files(f'{self.input_folder}')
            # update all files in input folder before moving
            self.update_files(dir_files)

