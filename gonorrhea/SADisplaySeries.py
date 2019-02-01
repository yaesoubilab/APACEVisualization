import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set


def plot_series(list_series, file_name = 'fig.png'):
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
                        y_axis_multiplier=1 / 1e6)

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


# base vs. quarterly base
plot_series(list_series=[Set.base, Set.baseQuarterly], file_name='Base vs. Quarterly Base.png')
# base vs. base with enhanced testing
plot_series(list_series=[Set.base, Set.baseEnhancedTesting], file_name='Base vs. Base with Enhanced Testing.png')

