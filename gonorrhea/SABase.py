import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set

# conditions of variables to define scenarios to display on each series of cost-effectiveness plane
varBaseConditions = [
    Cls.VariableCondition('Decision Period', 364, 364, False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.1, True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1, False)
]

# series to display on the cost-effectiveness plane
series = [
    Cls.Series('Base', 'blue', # '#1874CD',
               variable_conditions=varBaseConditions,
               if_find_frontier=True,
               labels_shift_x=-10,
               labels_shift_y=0.04)
]

# populate series
Cls.populate_series(series,
                    csv_filename=Set.SELECTED_SA_FILE_NAME,
                    save_cea_results=True,      # set it to True if the CE table should be generated
                    store_cea_CIs=True,
                    x_axis_multiplier=1 / 1e3,
                    y_axis_multiplier=1 / 1e6)

# plot
Cls.plot_series(series=series,
                x_label='Expected Gonorrhea Infections Averted (Thousands)',
                y_label='Expected Additional Drug M Used (Millions)',
                file_name='-Base.png',
                show_only_on_frontier=False,
                x_range=Set.X_RANGE,
                y_range=Set.Y_RANGE,
                show_error_bars=True
                )
