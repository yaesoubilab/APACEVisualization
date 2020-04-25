import numpy as np
import matplotlib.pyplot as plt
import covid19.PolicyClasses as P
import os

# ---- settings ----
POLICY_PARAMS = [1.09924, -0.11247, 0.19871, 0.0214, -0.08848, 0.5]#
WTPS = np.linspace(0.25e5, 0.75e5, 9)  # [min, max, number of points]

# change the current working directory
os.chdir('../..')

policy = P.PolicyRtI(policy_params=POLICY_PARAMS, wtps=WTPS)
policy.write_to_csv(file_name='ThresholdsRtI.csv',
                    directory='covid19/csv_files')