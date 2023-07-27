from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from re import sub, I
from core import XMLUpdator
from os import path
from logger import Logger
from traceback import print_exc


class Watcher:
    def __init__(self, input_folder, output_folder, ):
        self.observer = Observer()
        self.INPUT_FOLDER = input_folder
        # init XML updator
        self.xml_updator = XMLUpdator(input_folder, output_folder)
        # run the updates once for all for the first run
        self.update()
        self.logger = Logger()

    # update the edited/created file only
    def update(self, files_list=None):
        # move this file to temp folder
        self.xml_updator.process_files(files_list)

    def stop(self):
        self.observer.stop()

    def run(self):
        def _check_updates(filename):
            self.update([filename])

        class Handler(FileSystemEventHandler):
            @staticmethod
            def on_any_event(event):
                src = sub(r'.xml~$', '.xml', event.src_path)
                if path.isfile(str(src)):
                    if event.event_type == 'created':
                        # Take any action here when a file is first created.
                        self.logger.log_message("CREATED EVENT - %s" % src)
                        _check_updates(src)


        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.INPUT_FOLDER, recursive=True)
        self.observer.start()
        try:
            while True:
                sleep(5)
        except:
            print_exc()
            self.observer.stop()

        self.observer.join()
