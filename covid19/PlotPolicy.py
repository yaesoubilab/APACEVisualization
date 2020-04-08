import numpy as np
import matplotlib.pyplot as plt
import covid19.PolicyClases as P
import os

# ---- settings ----
POLICY_PARAMS = [5.0096096195,-1.0157278249,0.0033164372] # [5,-1,0.25] # [5.0096096195,-1.0157278249,0.0033164372]
WTPS = np.linspace(50000, 150000, 25)  # [min, max, number of points]

WTP_DELTA = 50000
R_EFF_MIN_DELTA = [0, 1]
MAX_R_EFF = 4
# ------------------

# change the current working directory
os.chdir('..')

policy = P.RBasedPolicy(policy_params=POLICY_PARAMS, wtps=WTPS)
policy.write_to_csv(file_name='Policies.csv',
                    directory='covid19/csv_files')

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5))

# policy when off
policy.add_policy_figure_when_relaxed(ax=axes[0], max_r=MAX_R_EFF, delta_wtp=WTP_DELTA)

# policy when on
policy.add_policy_figure_when_tightened(ax=axes[1], max_r=MAX_R_EFF, delta_wtp=WTP_DELTA)

fig.tight_layout()
fig.savefig('covid19/figures/Policy.png', dpi=300, bbox_inches='tight')
fig.show()
