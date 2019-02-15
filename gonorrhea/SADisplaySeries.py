import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set


def plot_series(list_series,
                effect_multiplier=1.0,
                cost_multiplier=1.0,
                switch_cost_effect_on_figure=False,
                wtp_multiplier=1.0,
                labels=('', ''),
                file_name='fig.png'):
    """    
    :param list_series: (list) of series to display on the CE plane
    :param effect_multiplier: the x-axis multiplier
    :param cost_multiplier: the y-axis multiplier
    :param switch_cost_effect_on_figure: displays cost on the x-axis and effect on the y-axis
    :param wtp_multiplier: wtp multiplier
    :param labels: (tuple) x_ and y-axis labels
    :param file_name: (string) the file name to save the plot as
    """

    # populate series
    Cls.populate_series(list_series,
                        save_cea_results=False,
                        interval_type='c',
                        effect_multiplier=effect_multiplier,
                        cost_multiplier=cost_multiplier,
                        switch_cost_effect_on_figure=switch_cost_effect_on_figure)

    # plot
    Cls.single_plot_series(series=list_series,
                           x_label=labels[0],
                           y_label=labels[1],
                           file_name=file_name,
                           show_only_on_frontier=False,
                           x_range=Set.X_RANGE,
                           y_range=Set.Y_RANGE,
                           show_error_bars=True,
                           wtp_multiplier=wtp_multiplier
                           )


# change this to false to show M used
SHOW_EFFECTIVE_LIFE = True
SIM_LENGTH = 50     # years
POP_RATE = 0.1e6/5e6

if SHOW_EFFECTIVE_LIFE:
    Cls.HEALTH_MEASURE = 'DALY'
    Cls.COST_MEASURE = 'Average ratio: Effective life of AB'
    effect_mult = -1 / SIM_LENGTH * POP_RATE
    cost_mult = SIM_LENGTH
    switch_cost_effect = True
    Set.X_RANGE = (-3, 3)
    Set.Y_RANGE = (-50, 75)
    labels = ('Increase in Effective Life of Drugs A and B (Years)',
              'Increase in Annual Gonorrhea Cases\n(Per 100,000 MSM Population)')
else:
    Cls.HEALTH_MEASURE = 'DALY'  # 'Average ratio: Annual rate of gonorrhea cases'
    Cls.COST_MEASURE = 'Total Cost'
    effect_mult = 1 / SIM_LENGTH * POP_RATE
    cost_mult = 1 / 1e6
    switch_cost_effect = False
    Set.X_RANGE = (-100, 100)
    Set.Y_RANGE = (-0.6, 0.6)
    labels = ('Additional Gonorrhea Cases Averted Annually\nPer 100,000 MSM Population',
              'Additional Drug M Used (Millions)')

# find the wtp multiplier
wtp_mult = effect_mult / cost_mult


# base vs. quarterly base
plot_series(list_series=[Set.base, Set.baseQuarterly],
            effect_multiplier=effect_mult,
            cost_multiplier=cost_mult,
            switch_cost_effect_on_figure=switch_cost_effect,
            wtp_multiplier=wtp_mult,
            labels=labels,
            file_name='Base vs. Quarterly Base.png')

# base vs. A
plot_series(list_series=[Set.base, Set.policyA],
            effect_multiplier=effect_mult,
            cost_multiplier=cost_mult,
            switch_cost_effect_on_figure=switch_cost_effect,
            wtp_multiplier=wtp_mult,
            labels=labels,
            file_name='Base vs. A.png')

# base vs. quarterly A
plot_series(list_series=[Set.base, Set.policyAQuart],
            effect_multiplier=effect_mult,
            cost_multiplier=cost_mult,
            switch_cost_effect_on_figure=switch_cost_effect,
            wtp_multiplier=wtp_mult,
            labels=labels,
            file_name='Base vs. Quarterly A.png')


included = False
if included:
    # base vs. base with enhanced testing
    plot_series(list_series=[Set.base, Set.baseEnhancedTesting],
                effect_multiplier=effect_mult,
                cost_multiplier=cost_mult,
                switch_cost_effect_on_figure=switch_cost_effect,
                wtp_multiplier=wtp_mult,
                labels=labels,
                file_name='Base vs. Base with Enhanced Testing.png')
    # base vs. quarterly base with enhanced testing
    plot_series(list_series=[Set.base, Set.baseQuarterlyEnhancedTesting],
                effect_multiplier=effect_mult,
                cost_multiplier=cost_mult,
                switch_cost_effect_on_figure=switch_cost_effect,
                wtp_multiplier=wtp_mult,
                labels=labels,
                file_name='Base vs. Quarterly Base with Enhanced Testing.png')

