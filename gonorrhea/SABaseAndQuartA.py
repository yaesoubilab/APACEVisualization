import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set

DS_TESTS = 5000  # annual number of cases tested for drug-resistance

# conditions of variables to define scenarios to display on each series of cost-effectiveness plane
varBaseConditions = [
    Cls.VariableCondition('Decision Period', 364, 364,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.1,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=False),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS, DS_TESTS,
                          if_included_in_label=False)
]
varPolicyAQuarterlyConditions = [
    Cls.VariableCondition('Decision Period', 91, 91,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.03, 0.5,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS/4, DS_TESTS/4,
                          if_included_in_label=False)
]

# series to display on the cost-effectiveness plane
series = [
    Cls.Series('Base', 'blue',
               variable_conditions=varBaseConditions,
               if_find_frontier=False,
               labels_shift_x=-10,
               labels_shift_y=0.04),
    Cls.Series('Policy A-Quarterly', 'red',
               variable_conditions=varPolicyAQuarterlyConditions,
               if_find_frontier=False,
               labels_shift_x=2.5,
               labels_shift_y=-0.11)
]

# populate series
Cls.populate_series(series,
                    csv_filename=Set.SELECTED_SA_FILE_NAME,
                    save_cea_results=False,
                    interval_type='c',
                    x_axis_multiplier=1 / 1e3,
                    y_axis_multiplier=1 / 1e6)

# plot
Cls.plot_series(series=series,
                x_label='Expected Gonorrhea Infections Averted (Thousands)',
                y_label='Expected Additional Drug M Used (Millions)',
                file_name='-Base vs Quarterly A.png',
                show_only_on_frontier=False,
                x_range=Set.X_RANGE,
                y_range=Set.Y_RANGE,
                show_error_bars=True
                )
