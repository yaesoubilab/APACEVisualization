import SimPy.InOutFunctions as IO
import SimPy.FigureSupport as Fig
import SimPy.StatisticalClasses as Stat
import SimPy.FormatFunctions as F
import apace.helpers as helper
import copy
from enum import Enum


HISTOGRAM_FIG_SIZE = (4.2, 3.2)


class Column(Enum):
    ID = 0
    NAME = 1
    LB = 2
    UB = 3
    TITLE = 4
    MULTIPLIER = 5


class ParamInfo:
    # class to store information about a parameter (id, name, estimate and confidence/uncertainty interval)
    def __init__(self, idn, name, estimate, interval):
        self.row = idn
        self.name = name
        self.estimate = estimate
        self.interval = interval


class Parameters:
    # class to create a dictionary of parameters
    def __init__(self, csv_file_name):
        """
        :param csv_file_name: csv file where the parameter samples are located
        assumes that the first row of this csv file contains the parameter names
        to be used as the keys of the dictionary of parameters it creates
        """

        # create a dictionary of parameter samples
        self.dictOfParams = IO.read_csv_cols_to_dictionary(csv_file_name, ',', True)

    def plot_histogram(self, parameter_name, title, x_lable=None, y_lable=None, x_range=None):
        """ creates a histogram of one parameter """

        Fig.graph_histogram2(
            self.dictOfParams[parameter_name],
            title, x_lable, y_lable,
            x_range=x_range, figure_size=HISTOGRAM_FIG_SIZE,
            output_type=Fig.OutType.JPG, file_name='figures\Par-'+title
        )

    def plot_histograms(self, ids=None, csv_file_name_prior=None, posterior_fig_loc='figures'):
        """ creates histograms of parameters specified by ids
        :param ids: (list) list of parameter ids
        :param csv_file_name_prior: (string) filename where parameter prior ranges are located
        :param posterior_fig_loc: (string) location where posterior figures should be located
        """

        # clean the directory
        IO.delete_files('.png', posterior_fig_loc)

        # read prior distributions
        if csv_file_name_prior is not None:
            priors = IO.read_csv_rows(
                file_name=csv_file_name_prior,
                if_del_first_row=True,
                delimiter=',',
                if_convert_float=True
            )

        # for all parameters, read sampled parameter values and create the histogram
        par_id = 0
        for key, par_values in self.dictOfParams.items():

            # skip these columns
            if key in ['Simulation Replication', 'Random Seed']:
                continue

            # check if the histogram should be created for this parameter
            if_show = False
            if ids is None:
                if_show = True
            elif par_id in ids:
                if_show = True

            # create the histogram
            if if_show:
                # find prior range
                x_range = None
                if priors is not None:
                    try:
                        x_range = [float(priors[par_id][Column.LB.value]), float(priors[par_id][Column.UB.value])]
                    except:
                        print('Could not convert string to float to find the prior distribution of parameter:', par_id)
                else:
                    x_range = None

                # find the filename the histogram should be saved as
                file_name = posterior_fig_loc + '\Par-' + str(par_id) + ' ' + helper.proper_file_name(key)

                # find title
                if priors[par_id][Column.TITLE.value] == '':
                    title = priors[par_id][Column.NAME.value]
                else:
                    title = priors[par_id][Column.TITLE.value]

                # find multipler
                if priors[par_id][Column.MULTIPLIER.value] == '':
                    multiplier = 1
                else:
                    multiplier = float(priors[par_id][Column.MULTIPLIER.value])
                    x_range = [x*multiplier for x in x_range]
                    par_values = [v*multiplier for v in par_values]

                # plot histogram
                Fig.graph_histogram2(
                    data=par_values,
                    title=title.replace('!', '\n'),
                    x_range=x_range,
                    figure_size=HISTOGRAM_FIG_SIZE,
                    output_type=Fig.OutType.JPG,
                    file_name=file_name
                )

            # move to the next parameter
            par_id += 1

    def calculate_means_and_intervals(self, significance_level, ids=None):
        """ calculate the mean and credible intervals of parameters specified by ids """

        results = []  # list of parameter estimates and credible intervals

        par_id = 0
        for key, value in self.dictOfParams.items():

            # skip these columns
            if key in ['Simulation Replication', 'Random Seed']:
                continue

            # if estimates and credible intervals should be calculated for this parameter
            if_record = False
            if ids is None:
                if_record = True
            elif par_id in ids:
                if_record = True

            # record the calculated estimate and credible interval
            if if_record:
                sum_stat = Stat.SummaryStat(key, value)
                results.append(
                    [par_id, key, sum_stat.get_mean(), sum_stat.get_PI(significance_level)]
                )

            # next parameter
            par_id += 1

        # write parameter estimates and credible intervals
        IO.write_csv('ParameterEstimates.csv', results)

    def calculate_ratio(self, numerator_par_name, denominator_par_names,
                        title, x_label=None, x_range=None, posterior_fig_loc='figures'):

        # calculate sum of parameters in the denominator
        sum_denom = copy.deepcopy(self.dictOfParams[denominator_par_names[0]])
        for i in range(1, len(denominator_par_names)):
            sum_denom += self.dictOfParams[denominator_par_names[i]]

        # calculate realizations for ratio
        ratio = self.dictOfParams[numerator_par_name]/sum_denom

        file_name = posterior_fig_loc + '\Ratio-' + title

        # create the histogram of ratio
        Fig.graph_histogram2(
            ratio, title, x_range=x_range, figure_size=HISTOGRAM_FIG_SIZE,
            output_type=Fig.OutType.JPG,
            file_name=file_name)

        # print the ratio estimate and credible interval
        sum_stat = Stat.SummaryStat('', ratio)
        print(title, sum_stat.format_estimate_PI(0.05, 1, F.FormatNumber.PERCENTAGE))
