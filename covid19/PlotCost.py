import covid19.PolicyClases as P
import matplotlib.pyplot as plt
import numpy as np


WTPS = np.linspace(50000, 150000, 25)  # [min, max, number of points]

# ---------------

resUtil = P.ResourceUtilization(csv_file_name='csv_files/PolicyEval.csv', wtps=WTPS)

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5))

resUtil.add_plot_to_axis(ax=axes[0], ys=[y*1e-6 for y in resUtil.costs],
                         title='Affordability curve',
                         y_label='Overall cost expected to incurred\n(million dollars)',
                         panel_label='C)',
                         max_y=2500, delta_wtp=50000)
resUtil.add_plot_to_axis(ax=axes[1], ys=resUtil.util,
                         title='',
                         y_label='Expected number of weeks with\ntightened social distancing',
                         panel_label='D)',
                         max_y=25, delta_wtp=50000)

fig.tight_layout()
fig.show()
