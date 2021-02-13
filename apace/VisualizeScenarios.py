import apace.ScenariosClasses as Cls


def plot_sets_of_scenarios(list_of_scenario_sets,
                           x_range=None, y_range=None,
                           effect_multiplier=1.0,
                           cost_multiplier=1.0,
                           switch_cost_effect_on_figure=False,
                           wtp_multiplier=1.0,
                           labels=('', ''),
                           title='fig.png',
                           fig_size=None,
                           l_b_r_t=None,
                           file_name=None):
    """
    :param list_of_scenario_sets: (list) of sets of scenarios to display on the CE plane
    :param x_range: x range
    :param y_range: y range
    :param effect_multiplier: the x-axis multiplier
    :param cost_multiplier: the y-axis multiplier
    :param switch_cost_effect_on_figure: displays cost on the x-axis and effect on the y-axis
    :param wtp_multiplier: wtp multiplier
    :param labels: (tuple) x_ and y-axis labels
    :param title: (string) title of the graph
    :param fig_size: (tuple) figure size
    :param file_name: (string) file name
    """

    # populate series
    Cls.SetOfScenarios.populate_sets_of_scenarios(
        list_of_scenario_sets=list_of_scenario_sets,
        save_cea_results=False,
        interval_type='c',
        effect_multiplier=effect_multiplier,
        cost_multiplier=cost_multiplier,
        switch_cost_effect_on_figure=switch_cost_effect_on_figure)

    # plot
    Cls.SetOfScenarios.plot_list_of_scenario_sets(
        list_of_scenario_sets=list_of_scenario_sets,
        x_label=labels[0],
        y_label=labels[1],
        title=title,
        show_only_on_frontier=False,
        x_range=x_range,
        y_range=y_range,
        show_error_bars=True,
        wtp_multiplier=wtp_multiplier,
        fig_size=fig_size,
        l_b_r_t=l_b_r_t,
        file_name=file_name)


def multi_plot_series(list_list_series,
                      list_of_titles,
                      x_range, y_range,
                      effect_multiplier=1.0,
                      cost_multiplier=1.0,
                      switch_cost_effect_on_figure=False,
                      wtp_multiplier=1.0,
                      labels=('', ''),
                      fig_size=None,
                      l_b_r_t=None,
                      file_name='fig.png'):
    """
    :param list_list_series: (list) of list of series to display on the multiple CE plane
    :param x_range: x range
    :param y_range: y range
    :param effect_multiplier: the x-axis multiplier
    :param cost_multiplier: the y-axis multiplier
    :param switch_cost_effect_on_figure: displays cost on the x-axis and effect on the y-axis
    :param wtp_multiplier: wtp multiplier
    :param labels: (tuple) x_ and y-axis labels
    :param fig_size: (tuple) figure size
    :param file_name: (string) the file name to save the plot as
    """

    # populate series
    for list_series in list_list_series:
        Cls.SetOfScenarios.populate_sets_of_scenarios(
            list_of_scenario_sets=list_series,
            save_cea_results=False,
            interval_type='c',
            effect_multiplier=effect_multiplier,
            cost_multiplier=cost_multiplier,
            switch_cost_effect_on_figure=switch_cost_effect_on_figure)
    # plot
    Cls.SetOfScenarios.multi_plot_scenario_sets(
        list_of_plots=list_list_series,
        list_of_titles=list_of_titles,
        x_label=labels[0],
        y_label=labels[1],
        file_name=file_name,
        show_only_on_frontier=False,
        x_range=x_range,
        y_range=y_range,
        show_error_bars=True,
        wtp_multiplier=wtp_multiplier,
        fig_size=fig_size,
        l_b_r_t=l_b_r_t
    )
