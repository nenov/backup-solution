import hashlib
import os
import shutil
import logging
import sys

BUF_SIZE = 65536


def hashfile(file):
    """A function which returns the hashing of a file"""
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


class Synchronizer:
    def __init__(self, source, replica, log_file):
        self.source = source
        self.replica = os.path.join(replica, os.path.basename(source) + "_backup")
        self.log_file = log_file
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename=log_file, encoding='utf-8', level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    def backup_folder(self):
        """A method which synchronizes the contents of two folders"""
        # Create a folder for the replica
        try:
            if not os.path.isdir(self.replica):
                os.mkdir(self.replica)
        except Exception:
            logging.error(f"Replica destination:{self.replica} could not be created.")
            raise
        # variable to track if new changes have occurred
        is_changed = 0

        for dirname, dirnames, filenames in os.walk(self.source):
            # Loop through the source location
            for filename in filenames:
                source_file = os.path.join(dirname, filename)
                destination_file = source_file.replace(self.source, self.replica)
                destination_location = dirname.replace(self.source, self.replica)

                # check if destination folder exists and if not, create it
                if not os.path.exists(destination_location):
                    os.makedirs(destination_location)
                    logging.info(f"New folder created:{destination_location}")
                    is_changed = 1
                # check if destination file exists and it not, copy it
                if not os.path.isfile(destination_file):
                    shutil.copy2(source_file, destination_file)
                    logging.info(f"New file copied:{source_file} -> {destination_file}")
                    is_changed = 1
                else:
                    # if the file already exists, check if file has to be updated
                    f1_hash = hashfile(source_file)
                    f2_hash = hashfile(destination_file)
                    if f1_hash != f2_hash:
                        shutil.copy2(source_file, destination_file)
                        logging.info(f"File Updated with newer version:{source_file} -> {destination_file}")
                        is_changed = 1

        # delete obsolete files and folders in the replica folder
        for dirname, dirnames, filenames in os.walk(self.replica):
            for filename in filenames:
                replica_file = os.path.join(dirname, filename)
                source_file = replica_file.replace(self.replica, self.source)
                # delete obsolete files
                if not os.path.isfile(source_file):
                    os.remove(replica_file)
                    logging.info(f"Obsolete file deleted:{replica_file}")
                    is_changed = 1

            for folder in dirnames:
                replica_destination = os.path.join(dirname, folder)
                source_location = replica_destination.replace(self.replica, self.source)
                # delete obsolete folders
                if not os.path.exists(source_location):
                    shutil.rmtree(replica_destination)
                    logging.info(f"Obsolete folder deleted:{replica_destination}")
                    is_changed = 1

        if is_changed == 0:
            logging.info(f"No changes found.")
