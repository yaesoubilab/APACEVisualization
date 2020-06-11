import matplotlib.pyplot as plt
from enum import Enum
from apace import Support
import csv
import matplotlib.ticker as ticker
import SimPy.InOutFunctions as IO
import SimPy.StatisticalClasses as Stat
from SimPy.Plots.FigSupport import *
import string
import numpy as np
plt.rcParams['svg.fonttype'] = 'none'


class OutType(Enum):
    """output types for plotted figures_national"""
    SHOW = 1    # show
    JPG = 2     # save the figure as a jpg file
    PDF = 3     # save the figure as a pdf file


#####################################
#---------- Constants ---------------
#####################################
OUTPUT_TYPE = OutType.SHOW
DEFAULT_FONT_SIZE = 6
X_LABEL = 'Year'
X_RANGE = None
X_TICKS = None

TRAJ_TRANSPARENCY = 0.3         # transparency of trajectories
TRAJ_COLOR_CODE = '#808A87'     # color of trajectories
OBS_COLOR_CODE = '#006400'      # color of real observations
FEASIBLE_REGION_COLOR_CODE = '#E6E6FA', #'#DCDCDC',    # color of the feasible reagion

REMOVE_TOP_RIGHT_BORDERS = False        # set to True to remove top and right borders from figures_national
Y_LABEL_COORD_X = -0.25     # increase to move right
Y_LABEL_COORD_Y = 0.5       # increase to move up
SUBPLOT_W_SPACE = 0.5       # width reserved for space between subplots
SUBPLOT_H_SPACE = 0.5       # height reserved for space between subplots

####################################


class TrajOneOutcomeOneRep:
    # trajectory for one simulation outcome from one simulation replication
    def __init__(self):
        self.times = []
        self.obss = []

    def add_all_observations(self, times, observations):
        """
        :param times: (list) of time points when simulation observations are recorded
        :param observations: (list) of simulation observations
        """
        self.times = times
        self.obss = observations


class TrajOneOutcomeMultipleReps:
    # trajectories for one simulation outcome from multiple simulation replications
    def __init__(self):
        self.name = ""   # name of this simulation outcome
        self.trajs = []  # list of multiple TrajOneOutcomeOneRep

    def add_traj_from_one_rep(self, traj):
        """
        add a trajectory from one simulation replication
        :param traj: an instance of TrajOneOutcomeOneRep
        """
        self.trajs.append(traj)

    def get_obss(self, time_index):
        """
        :return: (list) observations at the specified time index
        """
        obss = []
        for traj in self.trajs:
            obss.append(traj.obss[time_index])

        return np.array(obss)

    def get_mean_PI(self, time_index, alpha, multiplier=1, deci=0, format=None):
        """
        :param format: additional formatting instruction.
            Use ',' to format as number, '%' to format as percentage, and '$' to format as currency
        :return: the mean and percentile interval of observations at the specified time index formatted as instructed
        """

        # find the estimate and percentile interval
        stat = Stat.SummaryStat('', self.get_obss(time_index)*multiplier)
        estimate, pi = stat.get_mean(), stat.get_PI(alpha)

        if format is None:
            return estimate, pi
        else:
            return F.format_estimate_interval(estimate=estimate, interval=pi, deci=deci, format=format)

    def get_relative_diff_mean_PI(self, time_index0, time_index1, order=0, deci=0, format=None):
        """
        :return: the mean relative difference of trajectories at two time indeces
        """
        stat = Stat.RelativeDifferencePaired(
            '',
            x=self.get_obss(time_index1),
            y_ref=self.get_obss(time_index0),
            order=order)

        if format is None:
            return stat.get_mean(), stat.get_PI(alpha=0.05)
        else:
            return stat.get_formatted_mean_and_interval(interval_type='p', alpha=0.05, deci=deci, form=format)

    def get_trajs_mean(self):
        """
        :return: (list) [times, means] the average outcome across all trajectories at each time point
        """
        means = []
        for i in range(len(self.trajs[0].times)):
            # get the observations at this time index
            obss = self.get_obss(i)
            # calculate the mean
            means.append(sum(obss)/len(obss))

        return [self.trajs[0].times, np.array(means)]

    def get_trajs_percentile_interval(self, alpha):
        """
        :param alpha: significance level (between 0 and 1)
        :return: (list) the qth percentile of the outcome at each time point, where q=100*alpha/2
        """
        intervals = []
        for i in range(len(self.trajs[0].times)):
            obss = []
            for traj in self.trajs:
                obss.append(traj.obss[i])
            interval = [np.percentile(obss, 100*alpha/2), np.percentile(obss, 100*(1-alpha/2))]
            intervals.append(interval)
        return intervals


class TrajsDataFrame:
    # parses the entire csv files containing the simulated trajectories

    def __init__(self,
                 csv_file_name,
                 time0=0,
                 period_length=1,
                 warmup_sim_period=0,
                 warmup_sim_time=0,
                 warmp_obs_period=0,
                 warmup_epi_time=0
                 ):
        """
        :param csv_file_name: file name of the csv file
        """
        self.NumOfSims = 0
        self.allTrajs ={}  # maps trajectory names to instances of TrajOneOutcomeMultipleReps

        # read csv file
        csv_file = open(csv_file_name, "r")
        traj_names = next(csv.reader(csv_file, delimiter=','))
        n_cols = len(traj_names)
        cols = Support.read_csv_cols(csv_file_name, n_cols=n_cols, if_convert_float=True)

        # parse columns
        x_axes = {"Simulation Period": warmup_sim_period+1,
                  "Simulation Time": warmup_sim_time,
                  "Observation Period": warmp_obs_period+1,
                  "Epidemic Time": warmup_epi_time}
        col_idx = 0
        n_reps = 0
        while col_idx < n_cols:

            if traj_names[col_idx] == "Replication":

                # find the number of replications
                n_reps = int(max(cols[col_idx]) + 1) # replication starts from 0

                # find the row boundaries of each replication
                bounds = [0]
                row = 0
                n_rows = len(cols[col_idx])
                for n_rep in range(n_reps):
                    while row < n_rows and cols[col_idx][row] == n_rep:
                        row += 1
                    bounds.append(row)
                col_idx += 1

            elif traj_names[col_idx] in x_axes:

                # x-axis encountered
                x_i = col_idx
                col_idx += 1

                # ignore x = 0 for period x-axes
                offset = 0
                if traj_names[x_i].split()[1] == "Simulation Period":
                    offset = 1

                # generate trajectories with specific x-axis
                while col_idx < n_cols and traj_names[col_idx] not in x_axes and traj_names[col_idx] != "Replication":
                    if traj_names[col_idx] != "Code of Next Action":
                        traj = TrajOneOutcomeMultipleReps()
                        for repIdx in range(n_reps):
                            rep = TrajOneOutcomeOneRep()
                            times = cols[x_i][bounds[repIdx] + offset:bounds[repIdx + 1]]
                            observations = cols[col_idx][bounds[repIdx] + offset:bounds[repIdx + 1]]

                            # limit trajectory to warmup period
                            times = times[np.where(times >= x_axes[traj_names[x_i]])]
                            observations = observations[len(observations) - len(times):]
                            # print(traj_names[col_idx], observations)

                            # shift x-axis based on x-axis type
                            if traj_names[x_i].split()[1] == "Time":
                                times = np.array(times) + time0
                            elif traj_names[x_i].split()[1] == "Period":
                                times = np.array(times) * period_length + time0

                            rep.add_all_observations(times, observations)
                            traj.add_traj_from_one_rep(rep)
                        self.allTrajs[traj_names[col_idx]] = traj
                    col_idx += 1

            else:
                col_idx += 1

        self.NumOfSims = n_reps

    def add_to_ax(self, ax, plot_info, calibration_info=None, trajs_ids_to_display=None):
        """
        plots multiple trajectories of a simulated outcome in a single panel
        :param ax: Axes object
        :param plot_info: plot information
        :param calibration_info: calibration information
        :param trajs_ids_to_display: list of trajectory ids to display
        """

        # title and labels
        ax.set(xlabel=plot_info.xLabel, ylabel=plot_info.yLabel)
        ax.set_title(plot_info.title, loc='left')

        trajs_to_display = []
        if trajs_ids_to_display is None:
            trajs_to_display = self.allTrajs[plot_info.trajName].trajs
        else:
            for i in trajs_ids_to_display:
                trajs_to_display.append(self.allTrajs[plot_info.trajName].trajs[i])

        # plot trajectories
        for traj in trajs_to_display:
            if plot_info.ifSameColor:
                ax.plot(plot_info.xMultiplier * traj.times,
                        plot_info.yMultiplier * traj.obss,
                        plot_info.commonColorCode,
                        linewidth=1,
                        alpha=plot_info.transparency,
                        zorder=1)
            else:
                ax.plot(plot_info.xMultiplier * traj.times,
                        plot_info.yMultiplier * traj.obss,
                        alpha=plot_info.transparency)

        # add axes information
        add_axes_info(
            ax=ax,
            x_range=plot_info.xRange,
            y_range=plot_info.yRange,
            x_ticks=plot_info.xTicks,
            y_ticks=plot_info.yTicks,
            is_x_integer=plot_info.isXInteger
        )

        # plot calibration information
        if calibration_info:
            # feasible ranges
            if calibration_info.feasibleRangeInfo:
                # draw vertical feasible range lines
                ax.axvline(calibration_info.feasibleRangeInfo.xRange[0], ls='--', lw=0.75, color='k', alpha=0.5)
                ax.axvline(calibration_info.feasibleRangeInfo.xRange[1], ls='--', lw=0.75, color='k', alpha=0.5)
                # shade feasible range
                if calibration_info.feasibleRangeInfo.fillBetween:
                    ax.fill_between(
                        calibration_info.feasibleRangeInfo.xRange,
                        calibration_info.feasibleRangeInfo.yRange[0],
                        calibration_info.feasibleRangeInfo.yRange[1],
                        color=FEASIBLE_REGION_COLOR_CODE,
                        alpha=1)

            x_arr = [obs.t for obs in calibration_info.obsOutcomes]
            y_arr = [obs.y for obs in calibration_info.obsOutcomes]
            lower_error = [obs.y - obs.lb for obs in calibration_info.obsOutcomes if obs.lb]
            upper_error = [obs.ub - obs.y for obs in calibration_info.obsOutcomes if obs.ub]
            linestyle = '-' if calibration_info.ifConnectObss else 'none'
            capsize = 2 if calibration_info.ifShowCaps else 0

            ax.plot(x_arr, y_arr,
                    marker='o', markersize=3, ls=linestyle, lw=1, color=calibration_info.colorCode, zorder=2)
            if lower_error and upper_error:
                error_arr = [lower_error, upper_error]
                ax.errorbar(x_arr, y_arr,
                            yerr=error_arr, fmt='none', capsize=capsize, color=calibration_info.colorCode, zorder=2)

        # remove top and right border
        if REMOVE_TOP_RIGHT_BORDERS:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

    def plot(self, plot_info, calibration_info=None):
        """
        plots a figure with a single panel
        :param plot_info: plot information
        :param calibration_info: calibration information
        """

        fig, ax = plt.subplots(figsize=plot_info.figureSize) # figure size
        self.add_to_ax(ax,
                       plot_info=plot_info,
                       calibration_info=calibration_info)

        plt.tight_layout() # auto adjusts subplots to fit into figure area

        if plot_info.fileName is None:
            output_figure(plt, plot_info.title)
        else:
            output_figure(plt, plot_info.fileName)

    def plot_multi_panel(self, n_rows, n_cols, file_name,
                         list_plot_info, trajs_ids_to_display=None,
                         list_calib_info=None, show_subplot_labels=False,
                         share_x=False, share_y=False, figure_size=None,
                         l_b_r_t=(0.1, 0.1, 0.95, 0.9)):
        """
        plots a figure with multiple panels
        :param n_rows: number of rows
        :param n_cols: number of columns
        :param trajs_ids_to_display: list of trajectory ids to display
        :param list_plot_info: list of plot information
        :param list_calib_info: list of calibration information
        :param show_subplot_labels: set True to label subplots as A), B), ...
        :param share_x: share x-axis among all subplots
        :param share_y: share y-axis among all subplots
        :param figure_size: (tuple) figure size
        """

        # to get the current backend use: print('Previous Backend:', plt.get_backend())
        # change the current backend
        plt.switch_backend('TkAgg')

        # set default properties
        plt.rc('font', size=DEFAULT_FONT_SIZE) # fontsize of texts
        plt.rc('axes', titlesize=DEFAULT_FONT_SIZE)  # fontsize of the figure title
        plt.rc('axes', titleweight='semibold')  # fontweight of the figure title

        # plot each panel
        f, axarr = plt.subplots(n_rows, n_cols, sharex=share_x, sharey=share_y, figsize=figure_size)

        # show subplot labels
        if show_subplot_labels:
            axs = axarr.flat
            for n, ax in enumerate(axs):
                ax.text(Y_LABEL_COORD_X-0.05, 1.05, string.ascii_uppercase[n]+')', transform=ax.transAxes,
                        size=DEFAULT_FONT_SIZE+1, weight='bold')

        for i in range(n_rows):
            for j in range(n_cols):
                # get current Axes
                if n_rows == 1 or n_cols == 1:
                    ax = axarr[i * n_cols + j]
                else:
                    ax = axarr[i, j]

                # plot subplot, or hide extra subplots
                if i * n_cols + j >= len(list_plot_info):
                    ax.axis('off')
                else:
                    plot_info = list_plot_info[i * n_cols + j]
                    calib_info = list_calib_info[i * n_cols + j] if list_calib_info else None
                    self.add_to_ax(ax, plot_info, calib_info, trajs_ids_to_display)

                # remove unnecessary labels for shared axis
                if share_x and i < n_rows - 1:
                    ax.set(xlabel='')
                if share_y and j > 0:
                    ax.set(ylabel='')
                # coordinates of labels on the y-axis
                ax.get_yaxis().set_label_coords(x=Y_LABEL_COORD_X, y=Y_LABEL_COORD_Y)

        # plt.tight_layout() # auto adjusts subplots to fit into figure area
        # plt.tight_layout() is an experimental feature and doesn't always work
        # manually adjust the margins of and spacing between subplots instead

        plt.subplots_adjust(left=l_b_r_t[0], bottom=l_b_r_t[1], right=l_b_r_t[2], top=l_b_r_t[3],
                            wspace=SUBPLOT_W_SPACE, hspace=SUBPLOT_H_SPACE)
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize()) # maximize window

        plt.tight_layout()

        output_figure(plt, file_name)


class PlotTrajInfo:
    def __init__(self,
                 traj_name,         # name of the simulation outcome to visualize
                 title="",          # title of the plot
                 x_label=X_LABEL,   # x-axis label
                 y_label="",        # y-axis label
                 x_multiplier=1,    # multiplier to multiply the x-axis values by
                 y_multiplier=1,    # multiplier to multiply the y-axis values by
                 x_range=None,      # (list) range of x-axis
                 y_range=None,      # (list) range of y-axis
                 x_ticks=None,      # (list) start location and distance between x-ticks
                 y_ticks=None,      # (list) start location and distance between y-ticks
                 is_x_integer=False,   # set to True if x-axis only takes integer values
                 if_same_color=True,    # set to True if the same color should be used for all trajectories
                 common_color_code=TRAJ_COLOR_CODE,  # the color code of trajectories
                 transparency=TRAJ_TRANSPARENCY,  # transparency of trajectories (0, transparent; 1, opaque)
                 figure_size=(5, 5),    # figure size
                 file_name=None         # file name if to be saved
                 ):

        self.trajName = traj_name
        self.title = title
        self.xMultiplier = x_multiplier
        self.yMultiplier = y_multiplier
        self.xLabel = x_label
        self.yLabel = y_label
        self.xRange = x_range if x_range is not None else X_RANGE
        self.yRange = y_range
        self.xTicks = x_ticks if x_ticks is not None else X_TICKS
        self.yTicks = y_ticks
        self.isXInteger = is_x_integer
        self.ifSameColor = if_same_color
        self.commonColorCode = common_color_code
        self.transparency = transparency
        self.figureSize = figure_size
        self.fileName = file_name


class FeasibleRangeInfo:
    def __init__(self, x_range, y_range, fill_between=True):
        self.xRange = x_range           # range of feasible x-axis values
        self.yRange = y_range           # range of feasible y-axis values
        self.fillBetween = fill_between # set to True to shade feasible region


class ObservedOutcome:
    def __init__(self, time, obs, lower=None, upper=None):
        self.t = time       # time of observation
        self.y = obs        # observation
        self.lb = lower     # lower bound
        self.ub = upper     # upper bound


class PlotCalibrationInfo:
    def __init__(self,
                 list_of_observed_outcomes, # list of ObservedOutcome objects
                 if_connect_obss=False,     # set to True if observation points should be connected
                 if_show_caps=True,         # set to False if error bars should not have caps
                 color_code=OBS_COLOR_CODE, # color code
                 feasible_range_info=None):   # information of feasible range
        self.obsOutcomes = list_of_observed_outcomes
        self.ifConnectObss = if_connect_obss
        self.ifShowCaps = if_show_caps
        self.colorCode = color_code
        self.feasibleRangeInfo = feasible_range_info


class ProjectedTrajectories:
    def __init__(self,
                 scenarios_csv_files,
                 scenario_names,
                 fig_infos,
                 time_0=0,
                 warm_up=0,
                 period_length=1,
                 scenario_colors=None,
                 show_intervals=False, alpha=0.05
                 ):
        """
        :param scenarios_csv_files: (list of strings) list of csv files for each scenarios
        :param scenario_names: (list of strings) list of scenario names
        :param fig_infos: (list) list of figure info
        :param scenario_colors: (list) of colors
        :param show_intervals: set true to show uncertainty intervals
        """

        self.figInfos = fig_infos   # list of figure information
        self.scenarioNames = scenario_names
        self.scenarioColors = scenario_colors
        self.dictTrajMeans = {}         # dictionary of projected [times, means]
        self.dictTrajIntervals = {}     # dictionary of intervals for projected means

        # initialize dictionaries of impact measures
        for info in fig_infos:
            self.dictTrajMeans[info.trajName] = {}
            self.dictTrajIntervals[info.trajName] = {}

        for i, csv_file in enumerate(scenarios_csv_files):
            df = TrajsDataFrame(csv_file,
                                time0=time_0,
                                period_length=period_length,
                                warmup_sim_period=warm_up,
                                warmup_sim_time=warm_up+1,
                                warmp_obs_period=warm_up,
                                warmup_epi_time=warm_up+1)

            for info in fig_infos:
                self.dictTrajMeans[info.trajName][scenario_names[i]] \
                    = df.allTrajs[info.trajName].get_trajs_mean()
                if show_intervals:
                    self.dictTrajIntervals[info.trajName][scenario_names[i]] \
                        = df.allTrajs[info.trajName].get_trajs_percentile_interval(alpha=alpha)

    def plot_all(self, fig_folder='figures/'):

        # set default properties
        plt.rc('font', size=8)  # fontsize of texts
        #plt.rc('axes', titlesize=DEFAULT_FONT_SIZE)  # fontsize of the figure title
        #plt.rc('axes', titleweight='semibold')  # fontweight of the figure title

        panel_idx = 0
        for key, dict_mean_trajs in self.dictTrajMeans.items():

            legends = []
            fig, ax = plt.subplots(figsize=self.figInfos[panel_idx].figureSize)

            # title and labels
            ax.set(
                title=self.figInfos[panel_idx].title,
                xlabel=self.figInfos[panel_idx].xLabel,
                ylabel=self.figInfos[panel_idx].yLabel)

            # plot trajectories
            i = 0
            for scenario_name, value in dict_mean_trajs.items():
                legends.append(scenario_name)
                times = value[0]
                means = value[1]
                ax.plot(
                    self.figInfos[panel_idx].xMultiplier * times,
                    self.figInfos[panel_idx].yMultiplier * means,
                    color=self.scenarioColors[i],
                    label=legends[i]
                )

                # plot intervals
                if len(self.dictTrajIntervals[key]) > 0:

                    ls = []
                    us = []
                    series = self.dictTrajIntervals[key][scenario_name]
                    for j in range(len(series)):
                        ls.append(series[j][0] * self.figInfos[panel_idx].yMultiplier)
                        us.append(series[j][1] * self.figInfos[panel_idx].yMultiplier)

                    ax.plot(
                        self.figInfos[panel_idx].xMultiplier * times,
                        us,
                        color=self.scenarioColors[i],
                        linestyle='--', linewidth=.75, alpha=0.8
                    )
                    ax.plot(
                        self.figInfos[panel_idx].xMultiplier * times,
                        ls,
                        color=self.scenarioColors[i],
                        linestyle='--', linewidth=.75, alpha=0.8
                    )

                    # ax.fill_between(self.figInfos[panel_idx].xMultiplier * times,
                    #                 ls, us,
                    #                 color=self.scenarioColors[i],
                    #                 alpha=0.2)

                i += 1

            ax.legend(fontsize=7) #legends

            # add axes information
            add_axes_info(
                ax=ax,
                x_range=self.figInfos[panel_idx].xRange,
                y_range=self.figInfos[panel_idx].yRange,
                x_ticks=self.figInfos[panel_idx].xTicks,
                y_ticks=self.figInfos[panel_idx].yTicks,
                is_x_integer=self.figInfos[panel_idx].isXInteger,
                y_label=self.figInfos[panel_idx].yLabel
            )

            plt.tight_layout()

            # save this figure
            output_figure(plt, fig_folder+key+'.pdf')

            # next figure
            panel_idx += 1

    def plot_multi_panel(self, file_name):

        # plot each panel
        n_cols = len(self.dictTrajMeans.items())
        f, axarr = plt.subplots(1, n_cols)

        panel_idx = 0
        for key, dict_mean_trajs in self.dictTrajMeans.items():
            # title and labels
            axarr[panel_idx].set(
                title=self.figInfos[panel_idx].title,
                xlabel=self.figInfos[panel_idx].xLabel,
                ylabel=self.figInfos[panel_idx].yLabel)

            # plot trajectories
            for scenario_name, value in dict_mean_trajs.items():
                times = value[0]
                means = value[1]
                axarr[panel_idx].plot(
                    self.figInfos[panel_idx].xMultiplier * times,
                    self.figInfos[panel_idx].yMultiplier * means)

            # add axes information
            add_axes_info(
                ax=axarr[panel_idx],
                x_range=self.figInfos[panel_idx].xRange,
                y_range=self.figInfos[panel_idx].yRange,
                x_ticks=self.figInfos[panel_idx].xTicks,
                is_x_integer=self.figInfos[panel_idx].isXInteger
            )

            # next panel
            panel_idx += 1


        # include legend
        # OPTION #1: above subplots, stretched horizontally
        axarr[0].legend(self.scenarioNames,
                        bbox_to_anchor=(0., 1.2, 3.9, .102), # anchors legend to arbitrary location above axes
                        loc=3,           # anchors legend at its 'lower left'
                        ncol=2,          # number of columns in the legend
                        mode="expand",   # horizontally expands the legend to fill the size specified in bbox_to_anchor
                        borderaxespad=0.)

        # OPTION #2: to the right of subplots
        # plt.legend(self.scenarioNames, bbox_to_anchor=(1, 1))

        # OPTION $3: below subplots
        # axarr[n_cols // 2].legend(self.scenarioNames,
        #                           loc='upper center',
        #                           bbox_to_anchor=(0.5,-0.18),
        #                           ncol=2)

        plt.tight_layout()
        plt.subplots_adjust(wspace=0.4)

        # save this figure
        output_figure(plt, filename=file_name)


def compare_trajectories(csv_file_1, csv_file_2, legends, figure_location):

    # clean the directory
    IO.delete_files('.png', figure_location)

    df1 = TrajsDataFrame(csv_file_1)
    df2 = TrajsDataFrame(csv_file_2)

    # for all trajectories
    i = 0
    for key, trajs_one_outcome in df1.allTrajs.items():

        fig, ax = plt.subplots(figsize=(5, 5))  # figure size
        ax.set(title=key)  # title and labels

        # first (base)
        for traj in trajs_one_outcome.trajs:
            ax.plot(traj.times, traj.obss, 'g', alpha=1, zorder=2)

        # second (intervention)
        for traj in df2.allTrajs[key].trajs:
            ax.plot(traj.times, traj.obss, 'b', alpha=1, zorder=1)

        plt.legend(legends) #[::-1]

        file_name = figure_location+'/'+str(i)+' '+key
        output_figure(plt, file_name)

        i += 1


def convert_data_to_list_of_observed_outcomes(data):
    """
    :param data: list of [time, estimate, lower bound, upper bound]
    """
    obss = []
    for row in data:
        if len(row) == 2:
            obss.append(ObservedOutcome(
                time=row[0],
                obs=row[1])
            )
        elif len(row) == 4:
            obss.append(ObservedOutcome(
                time=row[0],
                obs=row[1],
                lower=row[2],
                upper=row[3])
            )

    return obss


def add_axes_info(ax, x_range, y_range, x_ticks=None, y_ticks=None, is_x_integer=False, y_label=None):

    # x-axis range
    if x_range:  # auto-scale if no range specified
        ax.set_xlim(x_range)  # x-axis range
    else:
        ax.set_xlim(xmin=0)  # x_axis has always minimum of 0

    # y-axis range
    if y_range:
        ax.set_ylim(y_range)  # y-axis range
    else:
        ax.set_ylim(ymin=0)  # y-axis has always minimum of 0

    if y_label:
        ax.set_ylabel(y_label)

    # x-ticks
    if x_ticks:
        x_ticks = np.arange(start=x_ticks[0], stop=ax.get_xlim()[1], step=x_ticks[1],
                            dtype=np.int32)
        # print(plot_info.xTicks[0], ax.get_xlim()[1], plot_info.xTicks[1], x_ticks)
        ax.set_xticks(x_ticks, minor=False)
        ax.set_xticklabels(x_ticks, fontdict=None, minor=False)
    else:
        # x-axis format, integer ticks
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins='auto', integer=is_x_integer))

    # y-ticks
    if y_ticks:
        y_ticks = np.arange(start=y_ticks[0], stop=ax.get_ylim()[1], step=y_ticks[1],
                            dtype=np.int32)
        ax.set_yticks(y_ticks, minor=False)
        ax.set_yticklabels(y_ticks, fontdict=None, minor=False)
