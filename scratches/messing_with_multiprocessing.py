import os
import time
import multiprocessing as mp


def worker():
    while True:
        print(f'Currently running on process {mp.current_process().pid}')
        time.sleep(2)


if __name__ == '__main__':
    mp.freeze_support()
    process = mp.Process(name='imagery_process', target=worker)
    process.start()
    print(mp.active_children())
    print(process.pid)
    print(os.getppid())
