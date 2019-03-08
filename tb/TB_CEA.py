import matplotlib.pyplot as plt
import apace.ScenariosClasses as Cls
import SimPy.EconEvalClasses as Econ

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
                              (0, 'Follow-up at yr 1'),
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
                              (0, 'No IPT'),
                              (1, 'With IPT')]
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
                    interval_type='p',
                    effect_multiplier=1,
                    cost_multiplier=1 / 1e3)


print(series[0].CEA.get_dCost_dEffect_cer(interval_type='p',
                                          alpha=0.05,
                                          cost_digits=0, effect_digits=2, icer_digits=1,
                                          cost_multiplier=1, effect_multiplier=1))

# plot
fig, ax = plt.subplots(figsize=(6, 5))
for i, ser in enumerate(series):
    for j, x_value in enumerate(ser.xValues):
        ax.plot(x_value, ser.yValues[j], markers[j], color=colors[j], markersize=8, mew=1)

        # error bars
        x_err_l = x_value-ser.xIntervals[j][0]
        x_err_u = ser.xIntervals[j][1] - x_value
        y_err_l = ser.yValues[j]-ser.yIntervals[j][0]
        y_err_u = ser.yIntervals[j][1] - ser.yValues[j]

        # ax.errorbar(x_value, ser.yValues[j],
        #             xerr=[[x_err_l], [x_err_u]],
        #             yerr=[[y_err_l], [y_err_u]],
        #             fmt='none', color='k', linewidth=1, alpha=0.4)

    ax.plot(ser.frontierXValues, ser.frontierYValues, color=ser.color, alpha=1)

    # legend
    ser.legend.append('Frontier')
    ax.legend(ser.legend, loc=1)

plt.xlabel('DALY Averted')
plt.ylabel('Additional Cost (Thousand Dollars)')
plt.xlim(-500, 6500)
plt.ylim(-150, 650)
plt.axvline(x=0, linestyle='--', color='black', linewidth=.5)
plt.axhline(y=0, linestyle='--', color='black', linewidth=.5)
plt.savefig('figures/cea/'
            + 'CEA U{:.{prec}f}% '.format(PROB_UPTAKE * 100, prec=0)
            + 'D{:.{prec}f}%'.format(PROB_DROPOUT * 100, prec=0)
            + '.png')
