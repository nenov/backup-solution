import os


class Synchronizer():
    def __init__(self):
        self.source = input("Source folder for synchronization: ")
        self.replica = input("Destination folder for replication: ")
        self.sync_interval = input("Synchronization interval: ")
        self.log_file = input("Destination for log file: ")

    def input_source_folder(self):
        while True:
            path = input("Source folder for synchronization: ")
            os.path.isdir(path)
            self.source = path



