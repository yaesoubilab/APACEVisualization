import numpy as np
import matplotlib.pyplot as plt
import covid19.PolicyClasses as P
import os

# ---- settings ----
POLICY_PARAMS = [0.16945,-3.11665,0.57042,-3.26263]# not bad: [2, -2, 2, -2]
# good option: [3.5, -0.5, 0.25, 500, -0.5, 0.5] for WTPS = np.linspace(1e5, 3e5, 9)
WTPS = np.linspace(0.25, 1.25, 10)  # [min, max, number of points]


F_Min_DELTA = [0, 1]
MAX_F_OFF = 4.01
MAX_F_ON = 4.01
WTP_DELTA = (WTPS[-1] - WTPS[0])/2

# change the current working directory
os.chdir('../..')

policy = P.PolicyFtRangeOfWTP(policy_params=POLICY_PARAMS, wtps=WTPS)
policy.write_to_csv(file_name='ThresholdsFt.csv',
                    directory='covid19/csv_files')


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5))

# policy when off
policy.add_policy_figure_when_relaxed(ax=axes[0], max_r=MAX_F_OFF, delta_wtp=WTP_DELTA)

# policy when on
policy.add_policy_figure_when_tightened(ax=axes[1], max_r=MAX_F_ON, delta_wtp=WTP_DELTA)

fig.tight_layout()
fig.savefig('covid19/figures/Policy.png', dpi=300, bbox_inches='tight')
fig.show()