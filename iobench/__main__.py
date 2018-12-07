"""iobench CLI"""
import sys
import os
import logging
from timeit import default_timer as timer
from ._version import VERSION

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

# TODO: collect all metadata (host name, file system, cnt files, timing etc )
# TODO: use config to set default data path and logs path


def main():
    """entry point for the iobench CLI"""
    print("iobench v " + str(VERSION))
    if len(sys.argv) < 2:
        print("specify path")
    path = sys.argv[1]
    LOGGER.info("reading list of files in directory")
    time_start = timer()
    files = [os.path.join(path, f) for f in os.listdir(path)]
    time_end = timer()
    cnt_files = len(files)
    time_elapsed = time_end - time_start
    LOGGER.info("{} files listed in {} s".format(cnt_files, time_elapsed))

    # TODO: shuffle file names across workers
    # TODO: make each worker read its portion of files


if __name__ == "__main__":
    main()
