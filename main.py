import os
import shutil
import hashlib


def hashfile(file):
    """A function which returns the hashing of a file"""

    BUF_SIZE = 65536

    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


source = input("Source folder for synchronization: ")
if not os.path.isdir(source):
    raise NameError('Location does not exist!')

replica = input("Destination folder for replication: ")
replica = os.path.join(replica, os.path.basename(source) + "_backup")
if not os.path.exists(replica):
    os.mkdir(replica)

for dirname, dirnames, filenames in os.walk(source):
    # print path to all filenames.
    for filename in filenames:
        source_file = os.path.join(dirname, filename)
        destination_file = source_file.replace(source, replica)
        destination_location = dirname.replace(source, replica)

        # check if folder exists and if not, create it
        if not os.path.exists(destination_location):
            os.makedirs(destination_location)
        # check if file exists and it not, copy it
        if not os.path.isfile(destination_file):
            shutil.copy2(source_file, destination_file)
        else:
            f1_hash = hashfile(source_file)
            f2_hash = hashfile(destination_file)
            if f1_hash != f2_hash:
                shutil.copy2(source_file, destination_file)
                print("Different Hash" + source_file)


# delete obsolete files and folders in the replica folder
for dirname, dirnames, filenames in os.walk(replica):
    for filename in filenames:
        replica_file = os.path.join(dirname, filename)
        source_file = replica_file.replace(replica, source)
        # delete removed files
        if not os.path.isfile(source_file):
            os.remove(replica_file)

    for folder in dirnames:
        replica_destination = os.path.join(dirname, folder)
        source_location = replica_destination.replace(replica, source)
        # delete removed folders
        if not os.path.exists(source_location):
            shutil.rmtree(replica_destination)


#sync_interval = input("Synchronization interval: ")
#log_file = input("Destination for log file: ")


