import matplotlib.pyplot as plt
import covid19.PolicyClasses as P
import covid19.CEOutcomesClasses as Res
import os

IF_WITH_OUTCOMES = True
WTP_RANGE = [0.1, 2.1]
WTP_DELTA = 0.5
SHOW_DATA = False

# change the current working directory
os.chdir('../..')

policy = P.PolicySingleFeature(csv_file_name='covid19/csv_files/OptimizedThresholdsFt.csv',
                               wtp_range=WTP_RANGE,
                               csv_file_name_proj_thresholds='covid19/csv_files/ProjOptimalThresholdsFt.csv')

if not IF_WITH_OUTCOMES:
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5))

    # policy when off
    policy.add_policy_figure_when_relaxed(ax=axes[0], y_label='Estimated\nforce of infection ' + r'$(F_t)$',
                                          max_feature_value=1,
                                          wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA)
    policy.add_policy_figure_when_tightened(ax=axes[1], max_feature_value=1,
                                            wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA)

else:
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 7))
    # policy when off
    policy.add_policy_figure_when_relaxed(ax=axes[0][0], max_feature_value=1,
                                          wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA,
                                          show_x_label=False)
    policy.add_policy_figure_when_tightened(ax=axes[0][1], max_feature_value=1,
                                            wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA,
                                            show_x_label=False)

    # cost and health outcomes
    resUtil = Res.CEOutcomes(csv_file_name='covid19/csv_files/PolicyEvals/PolicyEvalAdaptiveFt.csv',
                             poly_degree=2)

    resUtil.add_affordability_to_axis(ax=axes[1][0], max_y_cost=400, max_y_n_switches=100,
                                      wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA)
    resUtil.add_effect_to_axis(ax=axes[1][1], max_y=1000,
                               wtp_range=WTP_RANGE, wtp_delta=WTP_DELTA, show_data=SHOW_DATA)

fig.tight_layout()
fig.savefig('covid19/figures/Policy.png', dpi=300, bbox_inches='tight')
fig.show()