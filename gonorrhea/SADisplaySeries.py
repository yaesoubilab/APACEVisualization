import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set


Y_AXIS_MULTIPLIER = 1
LABELS = ('', '')


def plot_series(list_series, y_axis_multiplier=1.0, labels=('', ''), file_name='fig.png'):
    """    
    :param list_series: (list) of series to display on the CE plane
    :param y_axis_multiplier: the y-axis multiplier
    :param labels: (tuple) x_ and y-axis labels
    :param file_name: (string) the file name to save the plot as
    """

    # populate series
    Cls.populate_series(list_series,
                        csv_filename=Set.SELECTED_SA_FILE_NAME,
                        save_cea_results=False,
                        interval_type='c',
                        x_axis_multiplier=1 / 50,   # 50 years of simulation
                        y_axis_multiplier=y_axis_multiplier)

    # plot
    Cls.plot_series(series=list_series,
                    x_label=labels[0],
                    y_label=labels[1],
                    file_name=file_name,
                    show_only_on_frontier=False,
                    x_range=Set.X_RANGE,
                    y_range=Set.Y_RANGE,
                    show_error_bars=True
                    )


# change this to false to show M used
SHOW_EFFECTIVE_LIFE = True

if SHOW_EFFECTIVE_LIFE:
    Set.X_RANGE = (-5000, 5000)
    Set.Y_RANGE = (-3, 3)
    Cls.COST_MEASURE = 'Average ratio: Effective life of AB'
    Y_AXIS_MULTIPLIER = 50
    LABELS = ('Additional Gonorrhea Cases Averted Annually',
              'Increase in Effective Life of Drugs A and B (Years)')
else:
    Set.Y_RANGE = (-0.5, 0.5)
    Cls.COST_MEASURE = 'Total Cost'
    Y_AXIS_MULTIPLIER = 1 / 1e6
    LABELS = ('Additional Gonorrhea Cases Averted Annually',
              'Additional Drug M Used (Millions)')


# base vs. quarterly base
plot_series(list_series=[Set.base, Set.baseQuarterly],
            y_axis_multiplier=Y_AXIS_MULTIPLIER,
            labels=LABELS,
            file_name='Base vs. Quarterly Base.png')
# base vs. base with enhanced testing
plot_series(list_series=[Set.base, Set.baseEnhancedTesting],
            y_axis_multiplier=Y_AXIS_MULTIPLIER,
            labels=LABELS,
            file_name='Base vs. Base with Enhanced Testing.png')
# base vs. quarterly base with enhanced testing
plot_series(list_series=[Set.base, Set.baseQuarterlyEnhancedTesting],
            y_axis_multiplier=Y_AXIS_MULTIPLIER,
            labels=LABELS,
            file_name='Base vs. Quarterly Base with Enhanced Testing.png')

