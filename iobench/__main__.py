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
# TODO: use config to set default data path and logs path


def save_results(metadata):
    hostname = metadata["platform"]["host"]
    timestamp = metadata["timestamp"]
    name_file_results = "{}_{}.json".format(hostname, timestamp)
    path_results = "./logs"
    save_data_to_json(metadata, os.path.join(path_results, name_file_results))


def list_files(metadata):
    LOGGER.info("reading list of files in directory")
    time_start = timer()
    path = metadata["path_data"]
    files = [os.path.join(path, f) for f in os.listdir(path)]
    time_end = timer()
    cnt_files = len(files)
    time_elapsed = time_end - time_start
    metadata["cnt_files"] = cnt_files
    LOGGER.info("{} files listed in {} s".format(cnt_files, time_elapsed))
    experiment_data = {}
    experiment_data["name"] = "listing"
    experiment_data["time_elapsed"] = time_elapsed
    metadata["experiments"].append(experiment_data)
    # TODO: move this logic to parent class for all experiments


def main():
    """entry point for the iobench CLI"""

    print("iobench v " + str(VERSION))
    if len(sys.argv) < 2:
        print("specify path")
        exit(-1)

    metadata["timestamp"] = datetime.datetime.now().isoformat()
    metadata["platform"] = query_all()
    # TODO: get storage back-end details into metadata
    metadata["path_data"] = sys.argv[1]
    metadata["experiments"] = []
    list_files(metadata)
    save_results(metadata)
    # TODO: add hostname to results
    # TODO: shuffle file names across workers
    # TODO: make each worker read its portion of files


if __name__ == "__main__":
    main()
