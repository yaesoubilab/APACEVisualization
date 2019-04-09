import matplotlib.pyplot as plt
import apace.ScenariosClasses as Cls
import numpy as np

markers = ['o', 's', '^', 'D']
colors = ['r', 'b', 'g', '#FF9912']

PROB_UPTAKE = 0.75      # 0.5, 0.75, 1
PROB_DROPOUT = 0.15     # 0.1, 0.15, 0.25,

# conditions of variables to define scenarios to display on the cost-effectiveness plane
# here we want scenarios with
# 'Prob {Tc+ | Tc}' = PROB,
# 'Follow-Up (Tc+>1)' = any, and
# 'IPT' = any
varConditions = [
    Cls.VariableCondition('Prob {Tc+ | Tc}',
                          minimum=PROB_UPTAKE,
                          maximum=PROB_UPTAKE,
                          if_included_in_label=False),
    Cls.VariableCondition('Follow-Up (Tc+>1)',
                          minimum=0,
                          maximum=1,
                          if_included_in_label=True,
                          label_rules=[
                              (0, 'First-year follow-up'),
                              (1, 'Annual follow-up')]
                          ),
    Cls.VariableCondition('Prob {Drop-Out in Tc+>1}',
                          values=(PROB_DROPOUT, 0),
                          if_included_in_label=False),
    Cls.VariableCondition('IPT',
                          minimum=0,
                          maximum=1,
                          if_included_in_label=True,
                          label_rules=[
                              (0, ''),
                              (1, 'with continuous IPT')]
                          )
]

# data frame of scenarios
dfScenarios = Cls.ScenarioDataFrame(csv_file_name='csvfiles\TBScenarios.csv')

# series to display on the cost-effectiveness plane
series = [
    Cls.Series(name='U{:.{prec}f}%'.format(PROB_UPTAKE * 100, prec=0)
                    +'-D{:.{prec}f}%'.format(PROB_DROPOUT * 100, prec=0),
               scenario_df=dfScenarios,
               color='#4D4D4D',  # '#808A87',
               variable_conditions=varConditions,
               if_find_frontier=True,
               labels_shift_x=-0.04,
               labels_shift_y=0.01)
]

# populate series
Cls.populate_series(series,
                    save_cea_results=True,
                    colors_of_strategies=colors,
                    interval_type='p',
                    effect_multiplier=1,
                    cost_multiplier=1 / 1e3)

# CBA
del series[0].CBA._strategies[1:3]

series[0].CBA.graph_incremental_NMBs(
    min_wtp=0,
    max_wtp=1000,
    title='',
    y_label='Net Monetary Benefit ($)',
    x_label='Cost-Effectiveness Threshold ($ per DALY Averted)',
    interval_type='p',
    transparency=0.1,
    show_legend=True,
    figure_size=(6, 5)
)

# print dCost, dEffect and cost-effectiveness ratio with respect to the base
print(series[0].CEA.get_dCost_dEffect_cer(interval_type='p',
                                          alpha=0.05,
                                          cost_digits=0, effect_digits=0, icer_digits=1,
                                          cost_multiplier=1, effect_multiplier=1))

withCloud = True

# plot
fig, ax = plt.subplots(figsize=(6, 5))
for i, ser in enumerate(series):

    if not withCloud:
        for j, x_value in enumerate(ser.xValues):
            ax.plot(x_value, ser.yValues[j], markers[j], color=colors[j], markersize=8, mew=1)

        # # error bars
        # x_err_l = x_value-ser.xIntervals[j][0]
        # x_err_u = ser.xIntervals[j][1] - x_value
        # y_err_l = ser.yValues[j]-ser.yIntervals[j][0]
        # y_err_u = ser.yIntervals[j][1] - ser.yValues[j]
        #
        # # ax.errorbar(x_value, ser.yValues[j],
        # #             xerr=[[x_err_l], [x_err_u]],
        # #             yerr=[[y_err_l], [y_err_u]],
        # #             fmt='none', color='k', linewidth=1, alpha=0.4)

    # add the clouds
    if withCloud:
        for idx, s in enumerate(ser.CEA.get_shifted_strategies()):
            # add the center of the cloud
            ax.plot(s.aveEffect, s.aveCost/1000,
                    c='k',  # color
                    alpha=1,  # transparency
                    linewidth=2,  # line width
                    marker='x',  # markers
                    markersize=12,  # marker size
                    markeredgewidth=2)  # marker edge width
            # add the cloud
            #if not s.ifDominated:
            if idx >= 2:
                ax.scatter(s.effectObs, np.divide(s.costObs, 1000),
                           c=s.color,  # color of dots
                           alpha=0.15,  # transparency of dots
                           s=25,  # size of dots
                           label=s.name)  # name to show in the legend

    # add frontier
    ax.plot(ser.frontierXValues, ser.frontierYValues, color=ser.color, alpha=1)

    if withCloud:
        ax.legend()
    else:
        # legend
        leg = ['First-year follow-up',
               'Annual follow-up',
               'First-year follow-up with limited IPT',
               'Annual follow-up with continuous IPT',
               'Frontier']
        #ser.legend.append('Frontier')
        ax.legend(leg, loc=1) #ser.legend

ax.set_xlabel('DALY Averted')
ax.set_ylabel('Additional Cost (Thousand Dollars)')

if withCloud:
    ax.set_xlim(-5000, 20000)
    ax.set_ylim(-1000, 1500)
else:
    ax.set_xlim(-5000, 20000)  # (-500, 6500)
    ax.set_ylim(-1000, 1500)  # (-150, 850)

ax.axvline(x=0, linestyle='--', color='black', linewidth=.5)
ax.axhline(y=0, linestyle='--', color='black', linewidth=.5)

plt.tight_layout()
plt.savefig('figures/cea/'
            + 'CEA U{:.{prec}f}% '.format(PROB_UPTAKE * 100, prec=0)
            + 'D{:.{prec}f}%'.format(PROB_DROPOUT * 100, prec=0)
            + '.png')
