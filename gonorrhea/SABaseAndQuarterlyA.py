import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set

# conditions of variables to define scenarios to display on each series of cost-effectiveness plane
varBaseConditions = [
    Cls.VariableCondition('Decision Period', 364, 364, False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.1, True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1, False)
]
varPolicyAQuarterlyConditions = [
    Cls.VariableCondition('Decision Period', 91, 91, False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.15, True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 0, 0.11, True, label_format='{:.1%}')
]

# series to display on the cost-effectiveness plane
series = [
    Cls.Series('Base', 'blue',
               variable_conditions=varBaseConditions,
               if_find_frontier=True,
               labels_shift_x=-11,
               labels_shift_y=0.03),
    Cls.Series('Policy A-Quarterly', 'red',
               variable_conditions=varPolicyAQuarterlyConditions,
               if_find_frontier=True,
               labels_shift_x=2,
               labels_shift_y=-0.1)
]

# populate series
Cls.populate_series(series,
                    csv_filename=Set.SELECTED_SA_FILE_NAME,
                    store_cea_CIs=True,
                    x_axis_multiplier=1 / 1e3,
                    y_axis_multiplier=1 / 1e6)

# plot
Cls.plot_series(series=series,
                x_label='Expected Gonorrhea Infections Averted (Thousands)',
                y_label='Expected Additional Drug M Used (Millions)',
                file_name='-Base vs Quarterly A.png',
                x_range=(-70, 70),
                y_range=(-0.7, 1.9),
                show_error_bars=True
                )