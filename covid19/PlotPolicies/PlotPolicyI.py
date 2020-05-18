import matplotlib.pyplot as plt
import covid19.PolicyClasses as P
import covid19.CEOutcomesClasses as Res
import os

IF_WITH_OUTCOMES = True
WTP_RANGE = [0.01, 0.1601]
WTP_DELTA = 0.05
SHOW_DATA = False
MAX_VALUE = 75
# Y_LABEL = 'Estimated\nprevalence of infection '\
#           + r'$(I_t)$'+'\nper 100,000 population'
Y_LABEL = 'Number of COVID-19 patients\nin or waiting for ICU\n(per 100,000 population)'

# change the current working directory
os.chdir('../..')

policy = P.PolicySingleFeature(csv_file_name='covid19/csv_files/OptimizedThresholdsI.csv',
                               wtp_range=WTP_RANGE,
                               csv_file_name_proj_thresholds='covid19/csv_files/ProjOptimalThresholdsI.csv')

if not IF_WITH_OUTCOMES:
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5))

    # policy when off
    policy.add_policy_figure_when_relaxed(ax=axes[0],
                                          y_label=Y_LABEL,
                                          max_feature_value=MAX_VALUE,
                                          wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA)
    policy.add_policy_figure_when_tightened(ax=axes[1], max_feature_value=MAX_VALUE,
                                            wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA)

else:
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 7))
    # policy when off
    policy.add_policy_figure_when_relaxed(ax=axes[0][0],
                                          y_label=Y_LABEL,
                                          max_feature_value=MAX_VALUE,
                                          wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA,
                                          show_x_label=False)
    policy.add_policy_figure_when_tightened(ax=axes[0][1], max_feature_value=MAX_VALUE,
                                            wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA,
                                            show_x_label=False)

    # cost and health outcomes
    resUtil = Res.CEOutcomes(csv_file_name='covid19/csv_files/PolicyEvals/PolicyEvalAdaptiveIt.csv',
                             poly_degree=3)

    resUtil.add_affordability_to_axis(ax=axes[1][0], max_y_cost=100, max_y_n_switches=100,
                                      wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA)
    resUtil.add_effect_to_axis(ax=axes[1][1], max_y=1100,
                               wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA)

fig.tight_layout()
fig.savefig('covid19/figures/PolicyI.png', dpi=300, bbox_inches='tight')
fig.show()
