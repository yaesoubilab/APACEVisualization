import SimPy.InOutFunctions as IO
import numpy as np

R_On = [1, 3]
R_Off = [0.3, 1]

N = 5


def generate_scenarios(t1_range, t2_range, n_of_samples):

    t1_samples = np.linspace(t1_range[0], t1_range[1], n_of_samples)
    t2_samples = np.linspace(t2_range[0], t2_range[1], n_of_samples)

    scenarios = []
    for t1 in t1_samples:
        for t2 in t2_samples:
            scenarios.append([t1, t2])

    return scenarios


# print(generate_scenarios(CAPACITY, N))

IO.write_csv(rows=generate_scenarios(R_On, R_Off, N),
             file_name='../covid19/csv_files/ReffPolicies.csv')