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
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
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


def chunk_list(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


# TODO: make each worker read its portion of files
def read_files(files, metadata):
    time_start = timer()
    path = metadata["path_data"]
    for entry in files:
        # path_full = os.path.join(path, entry)
        in_file = open(entry, "rb")
        data = in_file.read()
    time_end = timer()
    time_elapsed = time_end - time_start
    experiment_data = {}
    experiment_data["name"] = "listing"
    experiment_data["time_elapsed"] = time_elapsed


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
    chunks = None
    if rank == 0:
        files = list_files(metadata)
        chunks = chunk_list(files, cnt_workers)
    files_local = comm.scatter(chunks, root=0)
    print("rank {} got {} files".format(rank, len(files_local)))
    read_files(files_local, metadata)
    if rank == 0:
        save_results(metadata)


if __name__ == "__main__":
    main()
