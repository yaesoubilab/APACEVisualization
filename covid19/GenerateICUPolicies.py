import SimPy.InOutFunctions as IO
import numpy as np

CAPACITY = 0.89/10000*2*20
N = 10


def generate_scenarios(capacity, n_of_samples):

    capacity_samples = np.linspace(0, capacity, n_of_samples)

    scenarios = []
    for close in capacity_samples:

        open_index = 0
        while True:
            c_open = capacity_samples[open_index]
            scenarios.append([close, c_open])

            open_index += 1
            if open_index >= len(capacity_samples) \
                    or capacity_samples[open_index] > close:
                break
    return scenarios


# print(generate_scenarios(CAPACITY, N))

IO.write_csv(rows=generate_scenarios(CAPACITY, N),
             file_name='../covid19/csv_files/ICUPolicies.csv')