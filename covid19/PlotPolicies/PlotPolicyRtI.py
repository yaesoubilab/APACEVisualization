import numpy as np
import matplotlib.pyplot as plt
import covid19.PolicyClasses as P
import os

# ---- settings ----
POLICY_PARAMS = [3.5, -0.5, 0.25, 500, -0.5, 0.5]#
# good option: [3.5, -0.5, 0.25, 500, -0.5, 0.5] for WTPS = np.linspace(1e5, 3e5, 9)
WTPS = np.linspace(1e5, 3e5, 9)  # [min, max, number of points]

# change the current working directory
os.chdir('../..')

policy = P.PolicyRtI(policy_params=POLICY_PARAMS, wtps=WTPS)
policy.write_to_csv(file_name='ThresholdsRtI.csv',
                    directory='covid19/csv_files')