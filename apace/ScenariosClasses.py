import numpy as np
import matplotlib.pyplot as plt
from apace import helpers
import csv
from enum import Enum
import SimPy.EconEvalClasses as Econ
import SimPy.StatisticalClasses as Stat
import SimPy.RegressionClasses as Reg


ALPHA = 0.05    # confidence level


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

        list_mean_PI={}
        for name in scenario_names:
            ratio_state = Stat.RelativeDifferencePaired(
                name='',
                x=self.scenarios[name].outcomes[outcome_name],
                y_ref=self.scenarios[scenario_name_base].outcomes[outcome_name],
                order=1)

            list_mean_PI[name] = helpers.get_mean_interval(ratio_state, deci, form)

        if len(scenario_names) == 1:
            return list_mean_PI[scenario_names[0]]
        else:
            return list_mean_PI

    def plot_relative_diff_by_scenario(self,
                                       scenario_name_base,
                                       scenario_names,
                                       outcome_names,
                                       title, x_label,
                                       y_labels=None,
                                       markers=('o' ,'D'),
                                       colors=('red' ,'blue'),
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
            ax.set_yticklabels(y_labels)

        ax.set_ylim(-distance_from_axis, len(scenario_names)-1+distance_from_axis)

        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel(x_label)
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


class Series:
    """ a series consists of a number of scenarios that meet certain conditions """

    def __init__(self,
                 name,
                 color,  # color of this series on the CE plane
                 variable_conditions,  # list of variable conditions
                 if_find_frontier=True,  # select True if CE frontier should be calculated
                 labels_shift_x=0,
                 labels_shift_y=0,
                 ):

        self.name = name
        self.color = color
        self.ifFindFrontier = if_find_frontier
        self.varConditions = variable_conditions
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
        self.legend = []

    def if_acceptable(self, scenario):
        """ :returns True if this scenario meets the conditions to be on this series """

        for condition in self.varConditions:
            if condition.values is None:
                if scenario.variables[condition.varName] < condition.min \
                        or scenario.variables[condition.varName] > condition.max:
                    return False
            else:
                if not(scenario.variables[condition.varName] in condition.values):
                    return False

        return True

    def do_CEA(self,
               save_cea_results=False,
               interval=Econ.Interval.NO_INTERVAL,
               x_axis_multiplier=1,
               y_axis_multiplier=1):

        # cost-effectiveness analysis
        self.CEA = Econ.CEA(self.strategies,
                            if_paired=True,
                            health_measure=Econ.HealthMeasure.DISUTILITY)

        # if to save the results of the CEA
        if save_cea_results:
            self.CEA.build_CE_table(interval=interval,
                                    file_name='CEA Table-'+self.name,
                                    cost_multiplier=y_axis_multiplier,
                                    effect_multiplier=x_axis_multiplier,
                                    effect_digits=0)

        # find the list of strategies excluding the base
        shifted_strategies = self.CEA.get_shifted_strategies()
        del shifted_strategies[0]  # remove the base strategy

        # find the (x, y) values of strategies to display on CE plane
        for idx, shiftedStr in enumerate(shifted_strategies):
            self.allDeltaEffects = np.append(self.allDeltaEffects, shiftedStr.effectObs*x_axis_multiplier)
            self.allDeltaCosts = np.append(self.allDeltaCosts, shiftedStr.costObs*y_axis_multiplier)
            self.xValues.append(shiftedStr.aveEffect*x_axis_multiplier)
            self.yValues.append(shiftedStr.aveCost*y_axis_multiplier)
            self.yLabels.append(shiftedStr.name)

            if interval is not Econ.Interval.NO_INTERVAL:
                x_interval = shiftedStr.get_effect_interval(interval, ALPHA)
                y_interval = shiftedStr.get_cost_interval(interval, ALPHA)
                self.xIntervals.append([x*x_axis_multiplier for x in x_interval])
                self.yIntervals.append([y*y_axis_multiplier for y in y_interval])

        # find the (x, y)'s of strategies on the frontier
        for idx, shiftedStr in enumerate(self.CEA.get_shifted_strategies_on_frontier()):
            self.frontierXValues.append(shiftedStr.aveEffect*x_axis_multiplier)
            self.frontierYValues.append(shiftedStr.aveCost*y_axis_multiplier)
            self.frontierLabels.append(shiftedStr.name)

            if interval is not Econ.Interval.NO_INTERVAL:
                x_interval = shiftedStr.get_effect_interval(interval, ALPHA)
                y_interval = shiftedStr.get_cost_interval(interval, ALPHA)
                self.frontierXIntervals.append([x*x_axis_multiplier for x in x_interval])
                self.frontierYIntervals.append([y*y_axis_multiplier for y in y_interval])

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
                    csv_filename,
                    save_cea_results=False,
                    interval=Econ.Interval.NO_INTERVAL,
                    x_axis_multiplier=1,
                    y_axis_multiplier=1):
    """
    :param series_list:
    :param csv_filename:
    :param save_cea_results: set it to True if the CE table should be generated
    :param interval: select from Econ.Interval (no interval, CI, or PI)
    :param x_axis_multiplier:
    :param y_axis_multiplier:
    :return:
    """

    # data frame for scenario analysis
    df = ScenarioDataFrame(csv_filename)

    # create the base strategy
    scn = df.scenarios['Base']
    base_strategy = Econ.Strategy(
        name='Base',
        cost_obs=scn.outcomes['Total Cost'],
        effect_obs=scn.outcomes['DALY'])

    # populate series to display on the cost-effectiveness plane
    for i, ser in enumerate(series_list):
        # add base
        ser.strategies = [base_strategy]
        # add other scenarios
        for key, scenario in df.scenarios.items():
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
                            label_list.append(varCon.get_label(value) + ', ')

                label = ''.join(str(x) for x in label_list)[:-1]

                # legends
                ser.legend.append(label)

                ser.strategies.append(
                    Econ.Strategy(
                        name=label,
                        cost_obs=scenario.outcomes['Total Cost'],
                        effect_obs=scenario.outcomes['DALY'])
                )

        # do CEA on this series
        ser.do_CEA(save_cea_results, interval, x_axis_multiplier, y_axis_multiplier)


def plot_series(series, x_label, y_label, file_name,
                show_only_on_frontier=False,
                x_range=None,
                y_range=None,
                show_error_bars=False):

    fig, ax = plt.subplots(figsize=(6, 5))

    for i, ser in enumerate(series):

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
                    plt.annotate(
                        txt,
                        (ser.frontierXValues[j] + ser.labelsShiftX, ser.frontierYValues[j] + ser.labelsShiftY),
                        color=ser.color
                    )

        else:  # show all points

            # scatter plot for all points
            ax.scatter(ser.xValues, ser.yValues, color=ser.color, alpha=0.5, zorder=10, s=15, label=ser.name)
            #ax.scatter(ser.allDeltaEffects, ser.allDeltaCosts, color=ser.color, alpha=.5, zorder=10, s=5, label=ser.name)

            # error bars
            if show_error_bars:
                ax.errorbar(ser.xValues, ser.yValues,
                            xerr=ser.get_x_err(),
                            yerr=ser.get_y_err(),
                            fmt='none', color='k', linewidth=1, alpha=0.25, zorder=5)

            # y-value labels
            for j, txt in enumerate(ser.yLabels):
                if txt is not 'Base':
                    plt.annotate(
                        txt,
                        (ser.xValues[j] + ser.labelsShiftX, ser.yValues[j] + ser.labelsShiftY),
                        fontsize=6.5,
                        color=ser.color,
                    )

            # fit a quadratic function to the curve.
            y = np.array(ser.yValues) #allDeltaCosts)
            x = np.array(ser.xValues) #allDeltaEffects)
            quad_reg = Reg.SingleVarRegression(x, y, degree=2)

            # print derivatives at
            print('WTP at min dCost', 1000 * quad_reg.get_derivative(x=ser.xValues[len(ser.xValues)-1]))
            print('WTP at dCost = 0:', 1000 * quad_reg.get_derivative(x=0))
            print('WTP at max dCost:', 1000 * quad_reg.get_derivative(x=ser.xValues[0]))

            xs = np.linspace(min(x), max(x), 50)
            predicted = quad_reg.get_predicted_y(xs)
            iv_l, iv_u = quad_reg.get_predicted_y_CI(xs)

            ax.plot(xs, predicted, '--', linewidth=1, color=ser.color)  # results.fittedvalues
            #ax.plot(xs, iv_u, '-', color=ser.color, linewidth=0.5, alpha=0.1)  # '#E0EEEE'
            #ax.plot(xs, iv_l, '-', color=ser.color, linewidth=0.5, alpha=0.1)
            #ax.fill_between(xs, iv_l, iv_u, linewidth=1, color=ser.color, alpha=0.05)

    # labels and legend
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc=2)

    # x and y ranges
    if x_range is not None:
        plt.xlim(x_range)
    if y_range is not None:
        plt.ylim(y_range)

    # origin
    plt.axvline(x=0, linestyle='-', color='black', linewidth=0.4)
    plt.axhline(y=0, linestyle='-', color='black', linewidth=0.4)

    plt.savefig('figures/' + file_name, dpm=300)