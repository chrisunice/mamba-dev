import json
import time
import random
from datetime import datetime


def av_config_gen():
    options = ['majorconfig1', 'majorconfig2', 'majorconfig3']
    yield random.choice(options)


def av_sub_config_gen():
    options = ['light', 'heavy', 'modified']
    yield random.choice(options)


def tail_gen():
    options = [f'AV{i}' for i in range(1, 21)]
    yield random.choice(options)


def date_gen():
    rand_ts = random.randint(1, int(time.time()))
    rand_date = datetime.fromtimestamp(rand_ts)
    yield rand_date.strftime('%Y%m%d')


def umi_gen():
    yield f"{next(date_gen())}-{next(tail_gen())}"


def freq_gen():
    yield random.randint(2, 18)*1000


def pol_gen():
    options = ['HH', 'VV']
    yield random.choice(options)


if __name__ == '__main__':
    missions = {}

    # Define 50 missions to generate random data for ...
    num_missions = 50
    for msn_num in range(1, num_missions+1):

        # Index the mission
        missions[msn_num] = {}

        # Fake UMI
        missions[msn_num]['umi'] = next(umi_gen())

        # Fake configuration
        missions[msn_num]['config'] = next(av_config_gen())

        # Fake sub configuration
        missions[msn_num]['sub_config'] = next(av_sub_config_gen())

        # Fake vector groups
        vectors = []
        num_vectors = random.randint(10, 100)
        for _ in range(num_vectors):
            vector = f"{next(freq_gen())} MHz | {next(pol_gen())[0]}-pol"
            if vector not in vectors:
                vectors.append(vector)
        missions[msn_num]['vectors'] = sorted(vectors, key=lambda x: int(x.split(' ')[0]))

    # Save to json object
    path_to_test_assets = 'C:\\Mamba\\test_assets'
    with open(f"{path_to_test_assets}\\fake_metadata.json", mode='w+') as f:
        json.dump(missions, f)
