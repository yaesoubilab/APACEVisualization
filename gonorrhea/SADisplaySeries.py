import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set


Y_AXIS_MULTIPLIER = 1


def plot_series(list_series, y_axis_multiplier=1.0, file_name='fig.png'):
    """    
    :param list_series: (list) of series to display on the CE plane
    :param file_name: (string) the file name to save the plot as
    """

    # populate series
    Cls.populate_series(list_series,
                        csv_filename=Set.SELECTED_SA_FILE_NAME,
                        save_cea_results=False,
                        interval_type='c',
                        x_axis_multiplier=1 / 1e3,
                        y_axis_multiplier=y_axis_multiplier)

    # plot
    Cls.plot_series(series=list_series,
                    x_label='Expected Gonorrhea Infections Averted (Thousands)',
                    y_label='Expected Additional Drug M Used (Millions)',
                    file_name=file_name,
                    show_only_on_frontier=False,
                    x_range=Set.X_RANGE,
                    y_range=Set.Y_RANGE,
                    show_error_bars=True
                    )


# change this to false to show M used
SHOW_EFFECTIVE_LIFE = True
if SHOW_EFFECTIVE_LIFE:
    Set.Y_RANGE = (-3, 3)
    Cls.COST_MEASURE = 'Average ratio: Effective life of AB'
    Y_AXIS_MULTIPLIER = 50
else:
    Set.Y_RANGE = (-0.5, 0.5)
    Cls.COST_MEASURE = 'Total Cost'
    Y_AXIS_MULTIPLIER = 1 / 1e6


# base vs. quarterly base
plot_series(list_series=[Set.base, Set.baseQuarterly],
            y_axis_multiplier=Y_AXIS_MULTIPLIER,
            file_name='Base vs. Quarterly Base.png')
# base vs. base with enhanced testing
plot_series(list_series=[Set.base, Set.baseEnhancedTesting],
            y_axis_multiplier=Y_AXIS_MULTIPLIER,
            file_name='Base vs. Base with Enhanced Testing.png')
# base vs. quarterly base with enhanced testing
plot_series(list_series=[Set.base, Set.baseQuarterlyEnhancedTesting],
            y_axis_multiplier=Y_AXIS_MULTIPLIER,
            file_name='Base vs. Quarterly Base with Enhanced Testing.png')

