import numpy as np
import matplotlib.pyplot as plt
import covid19.PolicyClasses as P
import os

# ---- settings ----
POLICY_PARAMS = [1.06359,-0.36608,0.11349,0.08916,-0.12382,0.12558]#
WTPS = np.linspace(0.5e5, 1.0e5, 9)  # [min, max, number of points]

# change the current working directory
os.chdir('../..')

policy = P.PolicyRtI(policy_params=POLICY_PARAMS, wtps=WTPS)
policy.write_to_csv(file_name='ThresholdsRtI.csv',
                    directory='covid19/csv_files')