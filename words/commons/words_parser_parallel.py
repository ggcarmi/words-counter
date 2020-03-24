"""
methods for parsing very big files with parallels processes
"""
import multiprocessing
import os
import logging
from collections import Counter

from words.commons.words_parser_common import parse_lines


logger = logging.getLogger("words.sub")


def read_lines_in_chunks(file, chunk_size=1024):
    """ generator for yield chunks of multiple lines from input file, chunk_size is in Bytes"""

    logger.debug("start yield lines")

    while True:
        lines = file.readlines(chunk_size)
        if not lines:
            break
        yield lines

    logger.debug("finish yield lines")


def calculate_lines_buff_size(file_name):
    """ calculate the optimal lines buffer size in Bytes
     from my analysis, for large files, chunks of 1MB gave good results """

    num_of_processes = multiprocessing.cpu_count() - 1
    file_size = os.stat(file_name).st_size

    lines_buff_size = file_size // num_of_processes
    MB = pow(2, 20)

    if lines_buff_size > MB:
        return MB

    if lines_buff_size > pow(2,10):
        return pow(2,10)

    logger.debug(f"lines buffer size: {lines_buff_size}")
    return lines_buff_size


def read_file_in_parallel(file_name):
    """ parse txt file into words frequencies dictionary
    due to the option of very large files ( >GB ) we will use muliprocesses """

    logger.debug("start process large file in parallel")

    # create pool of workers
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)

    # calculate the chunk size - for reading the file
    lines_buff_size = calculate_lines_buff_size(file_name)

    frequencies_counter = Counter()

    with open(file_name) as file:
        lines_iterator = read_lines_in_chunks(file, lines_buff_size)

        # map the work function to the workers, and provide ierator which iterate the lines in chunks
        results = pool.imap_unordered(parse_lines, lines_iterator, 1)

        # as soon as we start to receive results (partial dictionaries) from workers - merge them to the result dict
        for counter in results:
            frequencies_counter += counter

    logger.debug("finished process large file in parallel")
    return frequencies_counter


