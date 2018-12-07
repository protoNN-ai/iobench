"""iobench CLI"""
import sys
import os
import logging
import datetime
from system_query import query_all
from timeit import default_timer as timer
from ._version import VERSION
from .utils.io import save_data_to_json, get_time_str

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

metadata = {}
# TODO: collect all metadata (host name, file system, cnt files, timing etc )
# TODO: use config to set default data path and logs path


def save_results(metadata):
    hostname = metadata["platform"]["host"]
    timestamp = metadata["timestamp"]
    name_file_results = "{}_{}.json".format(hostname, timestamp)
    path_results = "./logs"
    save_data_to_json(metadata, os.path.join(path_results, name_file_results))


def main():
    """entry point for the iobench CLI"""

    print("iobench v " + str(VERSION))
    if len(sys.argv) < 2:
        print("specify path")
    metadata["timestamp"] = datetime.datetime.now().isoformat()
    metadata["platform"] = query_all()
    # TODO: get storage back-end details
    path = sys.argv[1]
    LOGGER.info("reading list of files in directory")
    time_start = timer()
    files = [os.path.join(path, f) for f in os.listdir(path)]
    time_end = timer()
    cnt_files = len(files)
    time_elapsed = time_end - time_start
    LOGGER.info("{} files listed in {} s".format(cnt_files, time_elapsed))
    save_results(metadata)
    # TODO: add hostname to results
    # TODO: shuffle file names across workers
    # TODO: make each worker read its portion of files


if __name__ == "__main__":
    main()
