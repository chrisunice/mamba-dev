import os
import time
import numpy as np
from typing import Callable
from itertools import product
from pathos.pools import ProcessPool

import pandas as pd


def set_progress(progress: tuple[int, int]) -> None:
    """ progress is a tuple representing (value, max) for a Progress bar """
    # does some shit that I dont understand
    return None

def query_chunk(
        param_chunk: dict,
        avconfig: str,
        avsubconfig: str,
        use_bin: bool,
        set_progress: Callable
):
    is_monitoring = param_chunk['monitor']
    chunk = param_chunk['params']

    if is_monitoring:
        print(f"{os.getpid()} is monitoring the progress")
    else:
        print(f"{os.getpid()} is NOT monitoring the progress")

    total = len(chunk)
    for idx, params in enumerate(chunk):
        look, depr, freq, pol = params
        if is_monitoring:
            set_progress((idx + 1, total))
        pass
    time.sleep(1)

    return pd.DataFrame([1, 2, 3])


if __name__ == '__main__':
    # Hard coded config values
    NUM_WORKERS = 8

    # Things that I want to iterate over
    looks = np.arange(0, 360, 60)
    deprs = np.arange(-90, 90, 30)
    freqs = np.arange(1000, 10000, 1000)
    pols = ['HH', 'VV']

    iterable_params = list(product(looks, deprs, freqs, pols))

    constant_params = dict(
        avconfig='ABCD2',
        avsubconfig='LT',
        use_bin=False,
        set_progress=set_progress
    )

    # Split the iterable parameters up into chunks based on number of workers
    chunk_size = np.ceil(len(iterable_params) / NUM_WORKERS).astype(int)
    param_chunks = [iterable_params[i:i + chunk_size] for i in range(0, len(iterable_params), chunk_size)]

    # Randomly assign one of the chunks to monitor the progress
    monitor_flags = [False] * NUM_WORKERS
    chosen_idx = np.random.choice(range(NUM_WORKERS))
    monitor_flags[chosen_idx] = True
    param_dict = {i: dict(monitor=flag, params=chunk) for i, (flag, chunk) in enumerate(zip(monitor_flags, param_chunks))}

    if NUM_WORKERS <= 1:
        # Basic map
        results = list(map(lambda x: query_chunk(x, **constant_params), param_dict.values()))
    else:
        pool = ProcessPool(NUM_WORKERS)
        # pool.map cannot handle (unpack) the ** notation when passing the constant params
        try:
            results = pool.map(lambda x: query_chunk(x, 'ABCD2', 'LT', False, set_progress), param_dict.values())
        except ValueError:
            pool.restart()
            results = pool.map(lambda x: query_chunk(x, 'ABCD2', 'LT', False, set_progress), param_dict.values())
        pool.terminate()

    print("I'm done")
