import os.path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class DirectoryWatcher:
    def __init__(self, dir_path, callback):
        self.directory = os.path.abspath(dir_path)
        self.callback = callback
        self.observer = Observer()

    def join(self):
        self.observer.join()

    def stop(self):
        self.observer.stop()

    def run(self):
        event_handler = Handler(self.callback)
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()


class FileWatcher:
    def __init__(self, file_path, callback):
        self.file_path = os.path.abspath(file_path)
        self.callback = callback
        self.directory = os.path.dirname(self.file_path)
        self.observer = Observer()

    def join(self):
        self.observer.join()

    def stop(self):
        self.observer.stop()

    def run(self):
        def callback(event):
            if event.src_path == self.file_path:
                self.callback(event)

        event_handler = Handler(callback)
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()


class Handler(FileSystemEventHandler):
    def __init__(self, callback_when_modify):
        self.callback = callback_when_modify

    def on_created(self, event):
        self.callback(event)

    def on_modified(self, event):
        self.callback(event)


if __name__ == '__main__':
    w = FileWatcher("/Users/temp/Desktop/start_kibana_and_head.sh", print)
    w.run()
    w.join()
