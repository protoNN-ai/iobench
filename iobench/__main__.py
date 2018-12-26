"""iobench CLI"""
import sys
import os
import logging
import datetime
from mpi4py import MPI
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
    return files
    # TODO: move this logic to parent class for all experiments


def main():
    """entry point for the iobench CLI"""

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    cnt_workers = comm.Get_size()

    if rank == 0:
        print("iobench v " + str(VERSION))
        print("cnt workers = " + str(cnt_workers))

    if len(sys.argv) < 2:
        if rank == 0:
            print("specify path")
            exit(-1)

    metadata["timestamp"] = datetime.datetime.now().isoformat()
    metadata["platform"] = query_all()
    # TODO: get storage back-end details into metadata
    metadata["path_data"] = sys.argv[1]
    metadata["experiments"] = []
    comm.Barrier()
    files = None
    if rank == 0:
        files = list_files(metadata)
    print(files)
    files_local = comm.scatter(files, root=0)
    if rank == 0:
        save_results(metadata)
    # TODO: add hostname to results
    # TODO: shuffle file names across workers
    # TODO: make each worker read its portion of files


if __name__ == "__main__":
    main()
