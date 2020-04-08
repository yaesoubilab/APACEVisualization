import covid19.PolicyClases as P
import matplotlib.pyplot as plt
import numpy as np
import os

# ---- settings ----
POLICY_PARAMS = [5.0096096195,-1.0157278249,0.0033164372] # [5,-1,0.25] # [5.0096096195,-1.0157278249,0.0033164372]
WTPS = np.linspace(50000, 150000, 25)  # [min, max, number of points]

WTP_DELTA = 50000
R_EFF_MIN_DELTA = [0, 1]
MAX_R_EFF = 4

# ---------------
# change the current working directory
os.chdir('..')
policy = P.RBasedPolicy(policy_params=POLICY_PARAMS, wtps=WTPS)
policy.write_to_csv(file_name='Policies.csv',
                    directory='covid19/csv_files')
resUtil = P.ResourceUtilization(csv_file_name='covid19/csv_files/PolicyEval.csv', wtps=WTPS)

fig, axes = plt.subplots(2, 2, figsize=(7.2, 7))

# policy when off
policy.add_policy_figure_when_relaxed(ax=axes[0], max_r=MAX_R_EFF, delta_wtp=WTP_DELTA)

# policy when on
policy.add_policy_figure_when_tightened(ax=axes[1], max_r=MAX_R_EFF, delta_wtp=WTP_DELTA)

# affordability curve
resUtil.add_plot_to_axis(ax=axes[2], ys=[y*1e-6 for y in resUtil.costs],
                         title='Affordability curve',
                         y_label='Overall cost expected to incurred\n(million dollars)',
                         panel_label='C)',
                         max_y=2500, delta_wtp=50000)
# utilization
resUtil.add_plot_to_axis(ax=axes[3], ys=resUtil.util,
                         title='',
                         y_label='Expected number of weeks with\ntightened social distancing',
                         panel_label='D)',
                         max_y=25, delta_wtp=50000)

fig.tight_layout()
fig.show()
