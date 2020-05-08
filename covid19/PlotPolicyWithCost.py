import covid19.PolicyClasses as P
import covid19.CostAndHealthOutcomesClasses as Res
import matplotlib.pyplot as plt
import numpy as np
import os

# ---- settings ----
POLICY_PARAMS = [7.72959,-1.80252,0.24708] # [5,-1,0.25] # [5.0096096195,-1.0157278249,0.0033164372]
SCALE = (1e5 + 3e5)/2
WTPS = np.linspace(100000, 200000, 19)  # [min, max, number of points]
SHOW_DATA = False

WTP_DELTA = 50000
R_DELTA = 0.5
MAX_R_OFF = 4.0
MAX_R_ON = 4.0

# ---------------
# change the current working directory
os.chdir('..')
policy = P.PolicyRt(policy_params=POLICY_PARAMS, scale=SCALE, wtps=WTPS)
policy.write_to_csv(file_name='Policies.csv',
                    directory='covid19/csv_files')
resUtil = Res.RtOutcomesAndUtilization(csv_file_name='covid19/csv_files/PolicyEvalFixed.csv',
                                       wtps=WTPS, poly_degree=3)

fig, axes = plt.subplots(2, 2, figsize=(7.5, 7))

# policy when off
policy.add_policy_figure_when_relaxed(ax=axes[0][0], max_r=MAX_R_OFF, delta_wtp=WTP_DELTA)

# policy when on
policy.add_policy_figure_when_tightened(ax=axes[0][1], max_r=MAX_R_ON, delta_wtp=WTP_DELTA)

# affordability curve
resUtil.add_affordability_to_axis(ax=axes[1][0],
                                  title='Affordability curve',
                                  y_label='Overall cost expected to incurred\n(million dollars)',
                                  panel_label='C)',
                                  max_y_cost=2000,
                                  max_y_qaly=20.1,
                                  delta_wtp=WTP_DELTA,
                                  show_data=SHOW_DATA)
# utilization
resUtil.add_utilization_to_axis(ax=axes[1][1],
                                title='Utilization of social distancing',
                                y_label='Expected number of weeks with\ntightened social distancing',
                                panel_label='D)',
                                max_y=20.1,
                                max_y_n_switches=2.01,
                                delta_wtp=WTP_DELTA,
                                show_data=SHOW_DATA)

fig.tight_layout()
fig.savefig('covid19/figures/PolicyWithCost.png', dpi=300, bbox_inches='tight')
fig.show()
