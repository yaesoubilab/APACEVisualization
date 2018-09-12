import matplotlib.pyplot as plt
import apace.ScenariosClasses as Cls

markers = ['o', 's', '^', 'D']
colors = ['r', 'b', 'g', '#FF9912']

PROB = 0.75

# conditions of variables to define scenarios to display on the cost-effectiveness plane
varConditions = [
    Cls.VariableCondition('Prob {Tc+ | Tc}',
                          minimum=PROB,
                          maximum=PROB,
                          if_included_in_label=False),
    Cls.VariableCondition('Follow-Up Rate (Tc+>1)',
                          minimum=0,
                          maximum=1,
                          if_included_in_label=True,
                          label_rules=[
                              (0, 'Follow-up at yr 1'),
                              (1, 'Annual follow-up')]
                          ),
    Cls.VariableCondition('IPT',
                          minimum=0,
                          maximum=1,
                          if_included_in_label=True,
                          label_rules=[
                              (0, 'No IPT'),
                              (1, 'With IPT')]
                          )
]

# series to display on the cost-effectiveness plane
series = [
    Cls.Series(name='{:.{prec}f}%'.format(PROB*100, prec=0),
               color='#808A87',
               variable_conditions=varConditions,
               if_find_frontier=True,
               labels_shift_x=-0.04,
               labels_shift_y=0.01)
]

# populate series
Cls.populate_series(series, 'csvfiles\TBScenarios.csv',
                    save_cea_results=True,
                    x_axis_multiplier=1,
                    y_axis_multiplier=1/1e3)

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

        ax.errorbar(x_value, ser.yValues[j],
                    xerr=[[x_err_l], [x_err_u]],
                    yerr=[[y_err_l], [y_err_u]],
                    fmt='none', color='k', linewidth=1, alpha=0.2)

    ax.plot(ser.frontierXValues, ser.frontierYValues, color=ser.color, alpha=1)

    # legend
    ser.legend.append('Frontier')
    ax.legend(ser.legend, loc=1)

plt.xlabel('DALY Averted')
plt.ylabel('Additional Cost (Thousand Dollars)')
plt.xlim(-500, 8500)
plt.ylim(-50, 650)
plt.axvline(x=0, linestyle='--', color='black', linewidth=1)
plt.axhline(y=0, linestyle='--', color='black', linewidth=1)
plt.savefig('figures/cea/' + 'CEA {:.{prec}f}%'.format(PROB*100, prec=0) + '.png')
