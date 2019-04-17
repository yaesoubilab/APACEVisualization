import numpy as np
import matplotlib.pyplot as plt
from apace import helpers
import csv
from enum import Enum
import SimPy.EconEval as Econ
import SimPy.StatisticalClasses as Stat
import SimPy.RegressionClasses as Reg


ALPHA = 0.05    # confidence level
COST_MEASURE = 'Total Cost'
HEALTH_MEASURE = 'DALY'


class Interval(Enum):
    NONE = 0,
    CONFIDENCE = 1,
    PREDICTION = 2,


class Scenario:
    def __init__(self, name):
        """
        :param name: scenario's name
        """

        self.name = name
        self.variables = {}     # dictionary of variable values with their name as keys
        self.outcomes = {}      # dictionary of list of outcomes with their names as keys

    def add_variable(self, variable_name, value):
        """
        :param variable_name: (string) variable name
        :param value: value of variable
        """
        self.variables[variable_name] = value

    def add_all_outcomes(self, outcome_name, outcomes):
        """
        :param outcome_name: (string) name of outcome
        :param outcomes: (list) of outcomes
        """
        self.outcomes[outcome_name] = outcomes


class ScenarioDataFrame:
    def __init__(self, csv_file_name):
        """
        :param csv_file_name: csv file where scenarios and realizations of ourcomes are located
        """

        self.scenarios = {}  # dictionary of all scenarios with scenario names as keys

        # read csv file
        csv_file = open(csv_file_name, "r")
        col_headers = next(csv.reader(csv_file, delimiter=','))
        n_cols = len(col_headers)
        cols = helpers.read_csv_cols(csv_file_name, n_cols=n_cols, if_convert_float=True)

        # parse columns
        col_idx = 0
        names_and_bounds = []
        while col_idx < n_cols:

            if col_headers[col_idx] == "Scenario":

                # find the row boundaries of each scenario
                names_and_bounds = []
                for row_idx, scenario_name in enumerate(cols[col_idx]):
                    if scenario_name not in self.scenarios:
                        self.scenarios[scenario_name] = Scenario(scenario_name)
                        names_and_bounds.append((scenario_name, row_idx))

                names_and_bounds.append(("dummy", row_idx + 1))
                col_idx += 1

                # store variables
                while col_headers[col_idx] != "Objective Function":
                    for scenario_name, bound in names_and_bounds[:-1]:
                        self.scenarios[scenario_name].add_variable(col_headers[col_idx], cols[col_idx][bound])
                    col_idx += 1

            else:

                # store outcomes
                for i in range(len(names_and_bounds) - 1):
                    scenario_name = names_and_bounds[i][0]
                    outcomes = cols[col_idx][names_and_bounds[i][1]:names_and_bounds[i+1][1]]
                    self.scenarios[scenario_name].add_all_outcomes(col_headers[col_idx], outcomes)
                col_idx += 1

    def get_mean_interval(self, scenario_name, outcome_name, interval_type='c', deci=0, form=None):
        """
        :return: mean and percentile interval of the selected outcome for the selected scenario
        """

        stat = Stat.SummaryStat('', self.scenarios[scenario_name].outcomes[outcome_name])
        return helpers.get_mean_interval(stat, interval_type, deci, form)

    def get_relative_diff_mean_interval(self, scenario_name_base, scenario_names, outcome_name, deci=0, form=None):
        """
        :return: dictionary of mean and percentile interval of the relative difference of the selected outcome
        """

        if type(scenario_names) is not list:
            scenario_names = [scenario_names]

        list_mean_PI = {}
        for name in scenario_names:
            ratio_state = Stat.RelativeDifferencePaired(
                name='',
                x=self.scenarios[name].outcomes[outcome_name],
                y_ref=self.scenarios[scenario_name_base].outcomes[outcome_name],
                order=1)

            list_mean_PI[name] = helpers.get_mean_interval(
                stat=ratio_state, interval_type='p', deci=deci, form=form)

        if len(scenario_names) == 1:
            return list_mean_PI[scenario_names[0]]
        else:
            return list_mean_PI

    def plot_relative_diff_by_scenario(self,
                                       scenario_name_base,
                                       scenario_names,
                                       outcome_names,
                                       title=None, x_label=None,
                                       y_labels=None,
                                       markers=('o','D'),
                                       colors=('red','blue'),
                                       legend=('morbidity', 'mortality'),
                                       distance_from_axis=0.5,
                                       filename=None,
                                       ):

        bar_position = []
        if len(outcome_names) > 2:
            raise ValueError('Only up to 2 outcomes could be displayed.')
        elif len(outcome_names) == 2:
            bar_position = [-0.15, 0.15]
        else:
            bar_position = [0]

        plt.rc('font', size=8)  # fontsize of texts
        fig, ax = plt.subplots(figsize=(5.4, 3.4))


        # find y-values
        y_values = np.arange(len(scenario_names))

        # build series to display
        for k, outcome_name in enumerate(outcome_names):
            list_mean_pi = self.get_relative_diff_mean_interval(scenario_name_base, scenario_names, outcome_name)

            # find x-values
            x_values = []
            x_err_l = []
            x_err_u = []
            for scenario_name in scenario_names:
                x_value = list_mean_pi[scenario_name][0]
                x_pi = list_mean_pi[scenario_name][1]
                x_values.append(100*x_value)
                x_err_l.append(100*(x_value-x_pi[0]))
                x_err_u.append(100*(x_pi[1]-x_value))

            ax.errorbar(x_values, y_values + bar_position[k], xerr=[x_err_l, x_err_u],
                        fmt=markers[k], ecolor=colors[k],
                        elinewidth=1.5, capsize=0, markersize=6, markerfacecolor='white',
                        markeredgecolor=colors[k], markeredgewidth=1.5)

        ax.set_yticks(y_values)
        if y_labels is None:
            ax.set_yticklabels(scenario_names)
        else:
            ax.set_yticklabels(y_labels, horizontalalignment='left')

        ax.yaxis.set_tick_params(pad=150)

        ax.set_ylim(-distance_from_axis, len(scenario_names)-1+distance_from_axis)

        ax.invert_yaxis()  # labels read top-to-bottom
        if x_label:
            ax.set_xlabel(x_label)
        if title:
            ax.set_title(title)
        ax.legend(legend, fontsize='small')
        plt.axvline(x=0, linestyle='--', color='black', linewidth=1)
        plt.tight_layout()
        if filename is None:
            filename = 'RelativeDifference.png'

        plt.savefig(filename+'.png', dpi=300)


class VariableCondition:
    def __init__(self, var_name, minimum=0, maximum=1, values=None,
                 if_included_in_label=False, label_format='', label_rules=None):
        """
        :param var_name: variable name as appears in the scenario csv file
        :param minimum: minimum acceptable value for this variable
        :param maximum: maximum acceptable value for this variable
        :param values: (tuple) of acceptable values
        :param if_included_in_label: if the value of this variable should be included in labels to display on CE plane
        :param label_format: (string) format of this variable values to display on CE plane
        :param label_rules: (list of tuples): to convert variable's value to labels
        for example: [(0, 'A'), (1, 'B')] replaces variable value 0 with A and 1 with B when creating labels
        """
        self.varName = var_name
        self.min = minimum
        self.max = maximum
        self.values = values
        self.ifIncludedInLabel = if_included_in_label
        self.labelFormat = label_format
        self.labelRules = label_rules

    def get_label(self, value):
        """ :returns the label associated to this value of the parameter """
        for rule in self.labelRules:
            if rule[0] == value:
                return rule[1]


class SetOfScenarios:
    """ a set of scenarios that meet certain conditions """

    def __init__(self,
                 name,
                 scenario_df,
                 color,
                 scenario_names=None,
                 conditions=None,
                 if_find_frontier=True,
                 labels_shift_x=0,
                 labels_shift_y=0,
                 ):
        """
        :param name: name of this set of strategies
        :param scenario_df: scenario data frame to pull the data from
        :param color: color of this series on the CE plane
        :param scenario_names: (list) names of scenarios to include in this set
        :param conditions: list of variable conditions
        :param if_find_frontier: # select True if CE frontier should be calculated
        :param labels_shift_x:
        :param labels_shift_y:
        """

        self.name = name
        self.ifPopulated = False
        self.scenarioDF = scenario_df
        self.color = color
        self.ifFindFrontier = if_find_frontier
        self.scenarioNames = scenario_names
        self.varConditions = conditions
        self.labelsShiftX = labels_shift_x
        self.labelsShiftY = labels_shift_y

        # delta costs and delta effects
        self.allDeltaCosts = np.array([])
        self.allDeltaEffects = np.array([])

        # (x, y) values
        self.xValues = []
        self.yValues = []
        # confidence or prediction intervals
        self.xIntervals = []
        self.yIntervals = []
        # y labels
        self.yLabels = []

        # frontier values
        self.frontierXValues = []
        self.frontierYValues = []
        self.frontierLabels = []
        # confidence or prediction intervals
        self.frontierXIntervals = []
        self.frontierYIntervals = []

        self.strategies = []    # list of strategies on this series
        self.CEA = None
        self.CBA = None
        self.legend = []

    def if_acceptable(self, scenario):
        """ :returns True if this scenario meets the conditions to be on this series """

        if self.scenarioNames is not None:
            # if the name of this scenario is included
            if scenario.name in self.scenarioNames:
                return True
        else:

            for condition in self.varConditions:
                if condition.values is None:
                    if scenario.variables[condition.varName] < condition.min \
                            or scenario.variables[condition.varName] > condition.max:
                        return False
                else:
                    if not(scenario.variables[condition.varName] in condition.values):
                        return False

        return True

    def build_CE_curve(self,
                       save_cea_results=False,
                       interval_type='n',
                       effect_multiplier=1,
                       cost_multiplier=1,
                       switch_cost_effect_on_figure=False):

        # cost-effectiveness analysis
        self.CEA = Econ.CEA(self.strategies,
                            if_paired=True,
                            health_measure='d')

        # CBA
        self.CBA = Econ.CBA(self.strategies,
                            if_paired=True,
                            health_measure='d')

        # if to save the results of the CEA
        if save_cea_results:
            self.CEA.build_CE_table(interval_type=interval_type,
                                    file_name='CEA Table-'+self.name+'.csv',
                                    cost_multiplier=cost_multiplier,
                                    effect_multiplier=effect_multiplier,
                                    effect_digits=0)

        # if the CE frontier should be calculated
        if self.ifFindFrontier:
            # find the (x, y)'s of strategies on the frontier
            for idx, strategy in enumerate(self.CEA.get_strategies_on_frontier()):
                if switch_cost_effect_on_figure:
                    self.frontierXValues.append(strategy.dCost.get_mean() * cost_multiplier)
                    self.frontierYValues.append(strategy.dEffect.get_mean() * effect_multiplier)
                else:
                    self.frontierXValues.append(strategy.dEffect.get_mean() * effect_multiplier)
                    self.frontierYValues.append(strategy.dCost.get_mean() * cost_multiplier)

                self.frontierLabels.append(strategy.name)

                if interval_type != 'n':
                    effect_interval = strategy.dEffect.get_interval(interval_type=interval_type,
                                                                     alpha=ALPHA,
                                                                     multiplier=effect_multiplier)
                    cost_interval = strategy.dCost.get_interval(interval_type=interval_type,
                                                                alpha=ALPHA,
                                                                multiplier=effect_multiplier)

                    if switch_cost_effect_on_figure:
                        self.frontierYIntervals.append(effect_interval)
                        self.frontierXIntervals.append(cost_interval)
                    else:
                        self.frontierXIntervals.append(effect_interval)
                        self.frontierYIntervals.append(cost_interval)

        #else:  # the CE frontier needs not to be calculated

        # find the (x, y) values of strategies to display on CE plane
        # remove the base strategy
        for strategy in [s for s in self.CEA.strategies if s.idx > 0]:
            if switch_cost_effect_on_figure:
                self.allDeltaEffects = np.append(self.allDeltaEffects,
                                                 strategy.effectObs * effect_multiplier)
                self.allDeltaCosts = np.append(self.allDeltaCosts,
                                               strategy.costObs * cost_multiplier)
                self.xValues.append(strategy.dCost.get_mean() * cost_multiplier)
                self.yValues.append(strategy.dEffect.get_mean() * effect_multiplier)
            else:
                self.allDeltaEffects = np.append(self.allDeltaEffects,
                                                 strategy.effectObs * effect_multiplier)
                self.allDeltaCosts = np.append(self.allDeltaCosts,
                                               strategy.costObs * cost_multiplier)
                self.xValues.append(strategy.dEffect.get_mean() * effect_multiplier)
                self.yValues.append(strategy.dCost.get_mean() * cost_multiplier)

            self.yLabels.append(strategy.name)

            if interval_type != 'n':
                effect_interval = strategy.dEffect.get_interval(interval_type=interval_type,
                                                                alpha=ALPHA,
                                                                multiplier=effect_multiplier)
                cost_interval = strategy.dCost.get_interval(interval_type=interval_type,
                                                            alpha=ALPHA,
                                                            multiplier=effect_multiplier)
                if switch_cost_effect_on_figure:
                    self.yIntervals.append(effect_interval)
                    self.xIntervals.append(cost_interval)
                else:
                    self.xIntervals.append(effect_interval)
                    self.yIntervals.append(cost_interval)

    def get_frontier_x_err(self):

        lower_err = [self.frontierXValues[i]-self.frontierXIntervals[i][0] for i in range(len(self.frontierXValues))]
        upper_err = [self.frontierXIntervals[i][1]-self.frontierXValues[i] for i in range(len(self.frontierXValues))]

        return [lower_err, upper_err]

    def get_x_err(self):

        lower_err = [self.xValues[i]-self.xIntervals[i][0] for i in range(len(self.xValues))]
        upper_err = [self.xIntervals[i][1]-self.xValues[i] for i in range(len(self.xValues))]

        return [lower_err, upper_err]

    def get_frontier_y_err(self):

        lower_err = [self.frontierYValues[i] - self.frontierYIntervals[i][0] for i in range(len(self.frontierYValues))]
        upper_err = [self.frontierYIntervals[i][1] - self.frontierYValues[i] for i in range(len(self.frontierYValues))]

        return [lower_err, upper_err]

    def get_y_err(self):

        lower_err = [self.yValues[i] - self.yIntervals[i][0] for i in range(len(self.yValues))]
        upper_err = [self.yIntervals[i][1] - self.yValues[i] for i in range(len(self.yValues))]

        return [lower_err, upper_err]


def populate_series(series_list,
                    save_cea_results=False,
                    colors_of_strategies=None,
                    interval_type='n',
                    effect_multiplier=1,
                    cost_multiplier=1,
                    switch_cost_effect_on_figure=False):
    """
    :param series_list:
    :param save_cea_results: set it to True if the CE table should be generated
    :param colors_of_strategies: (dictionary) of colors for strategies on this series
    :param interval_type: select from Econ.Interval (no interval, CI, or PI)
    :param effect_multiplier:
    :param cost_multiplier:
    :param switch_cost_effect_on_figure: displays cost on the x-axis and effect on the y-axis
    """

    # populate series to display on the cost-effectiveness plane
    for i, ser in enumerate(series_list):

        if ser.ifPopulated:
            continue

        # create the base strategy
        scn = ser.scenarioDF.scenarios['Base']
        base_strategy = Econ.Strategy(
            name='Base',
            cost_obs=scn.outcomes[COST_MEASURE],
            effect_obs=scn.outcomes[HEALTH_MEASURE],
            color=None if colors_of_strategies is None else colors_of_strategies[0]
        )

        # add base
        ser.strategies = [base_strategy]
        # add other scenarios
        i = 0
        for key, scenario in ser.scenarioDF.scenarios.items():
            # add only non-Base strategies that can be on this series
            if scenario.name != 'Base' and ser.if_acceptable(scenario):

                # find labels of each strategy
                label_list = []
                for varCon in ser.varConditions:
                    if varCon.ifIncludedInLabel:

                        # value of this variable
                        value = scenario.variables[varCon.varName]
                        # if there is not label rules
                        if varCon.labelRules is None:
                            if varCon.labelFormat == '':
                                label_list.append(str(value)+',')
                            else:
                                label_list.append(varCon.labelFormat.format(value) + ',')
                        else:
                            label = varCon.get_label(value)
                            if label == '':
                                pass
                            else:
                                label_list.append(label + ', ')

                label = ''.join(str(x) for x in label_list)

                if label[-1] == ' ' or label[-1] == ',':
                    label = label[:-1]
                if label[-1] == ' ' or label[-1] == ',':
                    label = label[:-1]

                # legends
                ser.legend.append(label)

                # color of this strategy
                color = None
                if colors_of_strategies is not None:
                    color = colors_of_strategies[i+1]

                ser.strategies.append(
                    Econ.Strategy(
                        name=label,
                        cost_obs=scenario.outcomes[COST_MEASURE],
                        effect_obs=scenario.outcomes[HEALTH_MEASURE],
                        color=color)
                )
                i += 1

        # do CEA on this series
        ser.build_CE_curve(save_cea_results,
                           interval_type,
                           effect_multiplier=effect_multiplier,
                           cost_multiplier=cost_multiplier,
                           switch_cost_effect_on_figure=switch_cost_effect_on_figure)

        ser.ifPopulated = True


def plot_sub_fig(ax, list_of_series,
                 title,
                 show_only_on_frontier=False,
                 x_range=None,
                 y_range=None,
                 show_error_bars=False,
                 wtp_multiplier=1):

    incr_eff_life = []

    for i, ser in enumerate(list_of_series):

        # if only points on frontier should be displayed
        if show_only_on_frontier:
            # scatter plot for points on the frontier
            ax.scatter(ser.frontierXValues, ser.frontierYValues, color=ser.color, alpha=0.5, label=ser.name)
            # line plot for frontier line
            ax.plot(ser.frontierXValues, ser.frontierYValues, color=ser.color, alpha=0.5)

            # error bars
            if show_error_bars:
                ax.errorbar(ser.frontierXValues, ser.frontierYValues,
                            xerr=ser.get_frontier_x_err(),
                            yerr=ser.get_frontier_y_err(),
                            fmt='none', color='k', linewidth=1, alpha=0.4)

            # y-value labels
            for j, txt in enumerate(ser.frontierLabels):
                if txt is not 'Base':
                    ax.annotate(
                        txt,
                        (ser.frontierXValues[j] + ser.labelsShiftX,
                         ser.frontierYValues[j] + ser.labelsShiftY),
                        color=ser.color
                    )

        else:  # show all points

            # scatter plot for all points
            ax.scatter(ser.xValues, ser.yValues, color=ser.color, alpha=0.5, zorder=10, s=15, label=ser.name)
            # ax.scatter(ser.allDeltaEffects, ser.allDeltaCosts, color=ser.color, alpha=.5,
            # zorder=10, s=5, label=ser.name)

            # error bars
            if show_error_bars:
                ax.errorbar(ser.xValues, ser.yValues,
                            xerr=ser.get_x_err(),
                            yerr=ser.get_y_err(),
                            fmt='none', color='k', linewidth=1, alpha=0.25, zorder=5)

            # y-value labels
            for j, txt in enumerate(ser.yLabels):
                if txt is not 'Base':
                    ax.annotate(
                        txt,
                        (ser.xValues[j] + ser.labelsShiftX*(x_range[1]-x_range[0]),
                         ser.yValues[j] + ser.labelsShiftY*(y_range[1]-y_range[0])),
                        fontsize=6.5,
                        color=ser.color,
                    )

            # fit a quadratic function to the curve.
            y = np.array(ser.yValues)  # allDeltaCosts)
            x = np.array(ser.xValues)  # allDeltaEffects)
            degree = 2
            quad_reg = Reg.SingleVarRegression(x, y, degree=degree)

            # print derivatives at
            print()
            print(title, ' | ', ser.name)
            print('WTP at min dCost', wtp_multiplier * quad_reg.get_derivative(x=ser.xValues[-1]))
            print('WTP at dCost = 0:', wtp_multiplier * quad_reg.get_derivative(x=quad_reg.get_zero()[degree-1]))
            print('WTP at max dCost:', wtp_multiplier * quad_reg.get_derivative(x=ser.xValues[0]))

            # store root
            incr_eff_life.append(quad_reg.get_zero()[degree-1])
            if i > 0:
                print('Increase in effective life of A and B:', round(incr_eff_life[i]-incr_eff_life[0], 2))

            xs = np.linspace(min(x), max(x), 50)
            predicted = quad_reg.get_predicted_y(xs)
            iv_l, iv_u = quad_reg.get_predicted_y_CI(xs)

            ax.plot(xs, predicted, '--', linewidth=1, color=ser.color)  # results.fittedvalues

            # if show error region:
            show_error_region = False
            if show_error_region:
                ax.plot(xs, iv_u, '-', color=ser.color, linewidth=0.5, alpha=0.1)  # '#E0EEEE'
                ax.plot(xs, iv_l, '-', color=ser.color, linewidth=0.5, alpha=0.1)
                ax.fill_between(xs, iv_l, iv_u, linewidth=1, color=ser.color, alpha=0.05)

    ax.set_title(title)
    ax.legend(loc=2)

    # x and y ranges
    if x_range is not None:
        ax.set_xlim(x_range)
    if y_range is not None:
        ax.set_ylim(y_range)

    # origin
    ax.axvline(x=0, linestyle='-', color='black', linewidth=0.4)
    ax.axhline(y=0, linestyle='-', color='black', linewidth=0.4)


def single_plot_series(list_of_series, x_label, y_label, title,
                       show_only_on_frontier=False,
                       x_range=None,
                       y_range=None,
                       show_error_bars=False,
                       wtp_multiplier=1):

    fig = plt.figure(figsize=(5, 4.6))
    ax = fig.add_subplot(111)

    plot_sub_fig(ax=ax, list_of_series=list_of_series,
                 title=title,
                 show_only_on_frontier=show_only_on_frontier,
                 x_range=x_range,
                 y_range=y_range,
                 show_error_bars=show_error_bars,
                 wtp_multiplier=wtp_multiplier)

    # labels and legend
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    #plt.tight_layout()
    fig.subplots_adjust(bottom=0.125, left=0.175)

    fig.savefig('figures/' + title +'.png', dpm=300) # read more about 'bbox_inches = "tight"'
    fig.show()


def multi_plot_series(list_of_plots,
                      list_of_titles,
                      x_label, y_label,
                      file_name,
                      show_only_on_frontier=False,
                      x_range=None,
                      y_range=None,
                      show_error_bars=False,
                      wtp_multiplier=1):
    # set default properties
    plt.rc('font', size=8)  # fontsize of texts
    plt.rc('axes', titlesize=8)  # fontsize of the figure title
    labels = ['A)', 'B)', 'C)']

    n_cols = len(list_of_plots)
    f, axarr = plt.subplots(1, n_cols, sharey=True, figsize=(7.5, 3))

    for i, fig in enumerate(list_of_plots):

        axarr[i].set_title(labels[i], loc='left', fontweight='bold')

        # title and labels
        if i == 0:
            axarr[i].set(
                ylabel=y_label)
        if i == 1:
            axarr[i].set(
                xlabel=x_label)

        # plot
        plot_sub_fig(ax=axarr[i],
                     list_of_series=fig,
                     title=list_of_titles[i],
                     show_only_on_frontier=show_only_on_frontier,
                     x_range=x_range,
                     y_range=y_range,
                     show_error_bars=show_error_bars,
                     wtp_multiplier=wtp_multiplier)

    # plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=0.15, right=0.97, top=0.9,
                        wspace=0.1, hspace=0)
    plt.savefig('figures/' + file_name + '.png', dpm=300)
    # plt.show()
