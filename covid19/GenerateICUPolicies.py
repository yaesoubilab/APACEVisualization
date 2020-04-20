import SimPy.InOutFunctions as IO
import numpy as np

ICU_CAPACITY = 0.89/10000*2
MAX_I = 0.1

# MAX = 30 * ICU_CAPACITY
# MIN = 0
MAX = MAX_I/5
MIN = 0.0005
N = 20


def generate_scenarios(t1_min, t1_max, n_of_samples):

    t1_samples = np.linspace(t1_min, t1_max, n_of_samples)

    scenarios = []
    for t1 in t1_samples:

        t1_index = 0
        while True:
            t2 = t1_samples[t1_index]
            scenarios.append([t1, t2])

            t1_index += 1
            if t1_index >= len(t1_samples) \
                    or t1_samples[t1_index] > t1:
                break
    return scenarios


# print(generate_scenarios(CAPACITY, N))

IO.write_csv(rows=generate_scenarios(MIN, MAX, N),
             file_name='../covid19/csv_files/ICUPolicies.csv')
