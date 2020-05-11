import numpy as np
import matplotlib.pyplot as plt
import covid19.PolicyClasses as P
import os

# ---- settings ----
POLICY_PARAMS = [6.69172,-2.82836,6.23949,-2.60692]# not bad: [7, -1, 7, -1]
# good option: [3.5, -0.5, 0.25, 500, -0.5, 0.5] for WTPS = np.linspace(1e5, 3e5, 9)
WTPS = np.linspace(0.25, 1.25, 9)  # [min, max, number of points]

# change the current working directory
os.chdir('../..')

policy = P.PolicyExponential(policy_params=POLICY_PARAMS, wtps=WTPS)
policy.write_to_csv(file_name='ThresholdsI.csv',
                    directory='covid19/csv_files')