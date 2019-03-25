import SimPy.InOutFunctions as IO
import SimPy.FigureSupport as Fig
import matplotlib.pyplot as plt
import os


def plot_all_opt_itrs(csv_directory, n_vars, save_plots_directory,
                      f_range=None, var_ranges=None, y_axis_labels=None, window=2):

    for name in os.listdir(csv_directory):
        plot_optimization_itrs(
            csv_directory=csv_directory,
            csv_filename=name,
            n_vars=n_vars,
            directory_save_plot=save_plots_directory,
            f_range=f_range,
            var_ranges=var_ranges,
            y_axis_labels=y_axis_labels,
            moving_ave_window=window
        )


def plot_optimization_itrs(csv_directory,
                           csv_filename,
                           n_vars,
                           directory_save_plot,
                           y_axis_labels,
                           f_range=None,
                           var_ranges=None,
                           moving_ave_window=2):
    """
    :param csv_directory: directory where the csv file is located
    :param csv_filename: name of the csv file
    :param n_vars: number of variables
    :param directory_save_plot: directory where the plot should be saved
    :param y_axis_labels: (list) of y-axis labels
    :param f_range: range of f
    :param var_ranges: (list) of ranges for variables
    :param moving_ave_window: (int) moving average window
    """

    # read the optimization iterations into columns
    cols = IO.read_csv_cols(csv_directory + csv_filename,
                            n_cols=2*n_vars+4, # variables (n_var), derivatives (n_var), iteration, f, step_Df, step_GH
                            if_ignore_first_row=True,
                            delimiter=',',
                            if_convert_float=True)

    # create plot for f and variables
    f_and_var_plot, axarr = plt.subplots(n_vars+1, 1, sharex=True, figsize=(6, 6))
    axarr[0].set(title=csv_filename)

    # objective function
    add_f(axarr=axarr,
          cols=cols,
          f_range=f_range,
          moving_ave_window=moving_ave_window,
          f_label=y_axis_labels[0])

    # plot variables
    add_var_or_dvar(what_to_add='var',
                    axarr=axarr,
                    cols=cols,
                    n_vars=n_vars,
                    var_ranges=var_ranges,
                    y_axis_labels=y_axis_labels,
                    moving_ave_window=moving_ave_window)

    # align y labels
    f_and_var_plot.align_ylabels()
    # adjust the plot
    f_and_var_plot.subplots_adjust(left=0.2, bottom=0.1, right=0.97, top=0.9,
                                   wspace=0, hspace=0.5)
    # save the plot
    f_and_var_plot.savefig(directory_save_plot + csv_filename + '.png')

    ######################
    # create plot for Df
    df_plot, axarr = plt.subplots(n_vars, 1, sharex=True, figsize=(6, 6))
    axarr[0].set(title='Df(x) - '+csv_filename)

    # plot variables
    add_var_or_dvar(what_to_add='dvar',
                    axarr=axarr,
                    cols=cols,
                    n_vars=n_vars,
                    y_axis_labels=y_axis_labels,
                    moving_ave_window=moving_ave_window)

    # align y labels
    df_plot.align_ylabels()
    # adjust the plot
    df_plot.subplots_adjust(left=0.2, bottom=0.1, right=0.97, top=0.9,
                            wspace=0, hspace=0.5)
    # save the plot
    df_plot.savefig(directory_save_plot + 'Df-' +csv_filename + '.png')

def add_f(axarr, cols, f_range, moving_ave_window, f_label=None):

    # plot objective function
    axarr[0].plot(cols[0], cols[1])
    # moving average of the objective function
    axarr[0].plot(cols[0], Fig.get_moving_average(cols[1], window=moving_ave_window), 'ko', markersize=1)
    # y-axis label
    axarr[0].set(ylabel=f_label)
    # y-axis range
    if f_range is not None:
        axarr[0].set(ylim=f_range)
    # horizontal line at 0
    axarr[0].axhline(y=0, linestyle='-', color='black', linewidth=0.4)


def add_var_or_dvar(what_to_add, axarr, cols, n_vars, y_axis_labels, moving_ave_window, var_ranges=None):

    if what_to_add == 'var':
        ax_indx = 1
        col_indx = 2
    elif what_to_add == 'dvar':
        ax_indx = 0
        col_indx = 2 + n_vars
        y_range = (-1, 1)
    else:
        pass # error

    for i in range(n_vars):
        # variable values
        axarr[ax_indx+i].plot(cols[0], cols[col_indx+i])
        # moving average
        if what_to_add == 'var':
            axarr[ax_indx+i].plot(cols[0],
                                  Fig.get_moving_average(cols[col_indx+i], window=moving_ave_window),
                                  'ko', markersize=1)
        # horizontal line at 0
        if what_to_add == 'dvar':
            axarr[ax_indx+i].axhline(y=0, linestyle='-', color='black', linewidth=0.4)
        # y-axis label
        axarr[ax_indx+i].set(ylabel=y_axis_labels[i+1])
        # y-axis range
        #if var_ranges is not None:
        if what_to_add == 'var':
            y_range = var_ranges[i]
        axarr[ax_indx+i].set(ylim=y_range)

    # label the x-axis of the last figure
    axarr[n_vars+ax_indx-1].set(xlabel='Iteration')



