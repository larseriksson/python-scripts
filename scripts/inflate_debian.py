#!/usr/bin/python3
from __future__ import print_function

__author__ = 'lars.q.eriksson@gmail.com'

import argparse
import os
import os.path as path
import tempfile

import subprocess

# constants
AR_CMD = ["ar", "x"]
XZ_CMD = ["xz", "-d"]
TAR_CMD = ["tar", "xf"]
DATA_FILE_NAME = "data.tar"
DESCRIPTION = "installs bracket manually from tarball"


# build arguments
def existing_file(string):
    """
    Check if given file exists.
    The value is interpreted as a file path in the file system and determines
    if a file exists with the given name
    :param string: the string to be interpreted as a file path
    :return: the string if the file exists, otherwise an exception is raised
    """
    if not path.exists(string):
        msg = "file %r does not exists" % string
        raise argparse.ArgumentTypeError(msg)

    if not path.isfile(string):
        msg = "%r exists but is not a file" % string
        raise argparse.ArgumentTypeError(msg)

    return string


parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('file',
                    help="The file to inflate",
                    type=existing_file,
                    metavar="FILE")
# Utilities


def ar(file, member):
    return AR_CMD + [file, member]


def xz(file):
    return XZ_CMD + [file]


def tar(file):
    return TAR_CMD + [file]


def check_if_exists(file, msg, code):
    print("%s completes" % msg)

    if code != 0:
        error_msg = "%(task)s failed and returned error code %(error)s (%(code)s)" \
                    % {"task": msg, "error": os.strerror(code), "code": code}

        raise FileNotFoundError(error_msg)

    if not path.exists(file) or not path.isfile(file):
        error_msg = "%s reported to exit normally but no file %r could not be found" \
                    % (msg, file)

        raise FileNotFoundError(error_msg)

    pass

#

temp_folder = tempfile.TemporaryDirectory(prefix="update_brackets_")

print(temp_folder)

file_to_inflate = parser.parse_args().file
compressed_data_file = path.join(temp_folder.name, DATA_FILE_NAME + ".xz")
data_file = path.join(temp_folder.name, DATA_FILE_NAME)

try:
    print("entering %r" % temp_folder.name)

    os.chdir(temp_folder.name)

    r = subprocess.call(ar(file_to_inflate, compressed_data_file))
    check_if_exists(compressed_data_file, "inflating %r" % file_to_inflate, r)

    r = subprocess.call(xz(compressed_data_file))
    check_if_exists(data_file, "inflating %r" % compressed_data_file, r)

    r = subprocess.call(tar(data_file))
    check_if_exists(data_file, "inflating %r" % data_file, r)

    dirs_to_copy = [name for name in os.listdir(temp_folder.name)
                    if path.isdir(path.join(temp_folder.name, name))]

    for dir_to_copy in dirs_to_copy:
        try:
            target = "/"
            r = subprocess.call(["sudo", "cp", "-r", dir_to_copy, target])
            if r == 0:
                print("%r copied successfully" % dir_to_copy)
            else:
                print("failed to move %(file)r, reason: %(error)s (%(code)s)" %
                      {"file": dirs_to_copy,
                       "error": os.strerror(r),
                       "code": r})

        except OSError as e:
            print("error occurred during move: %s" % e)

    print("cleaning up")
    temp_folder.cleanup()

except OSError as e:
    raise IOError("IOError occurred: %s" % e)
