import SimPy.InOutFunctions as IO
import SimPy.FigureSupport as Fig
import matplotlib.pyplot as plt
import os


def plot_all_opt_itrs(csv_directory, n_vars, save_plots_directory,
                      f_range=None, x_ranges=None, y_axis_labels=None, window=2):

    for name in os.listdir(csv_directory):
        plot_opt_itrs(
            path=csv_directory,
            csv_file=name,
            n_vars=n_vars,
            save_path=save_plots_directory,
            f_range=f_range,
            x_ranges=x_ranges,
            y_axis_labels=y_axis_labels,
            window=window
        )


def plot_opt_itrs(path, csv_file, n_vars, save_path, f_range=None, x_ranges=None, y_axis_labels=None, window = 2):

    cols = IO.read_csv_cols(path+csv_file,
                            n_cols=2*n_vars+4,
                            if_ignore_first_row=True,
                            delimiter=',',
                            if_convert_float=True)

    # objective function
    f, axarr = plt.subplots(n_vars+1, 1, sharex=True, figsize=(6, 6))
    axarr[0].set(title=csv_file)
    axarr[0].plot(cols[0], cols[1])#, color=ser.color, alpha=0.5)
    axarr[0].plot(cols[0], Fig.get_moving_average(cols[1], window=window), 'ko', markersize=1)

    if y_axis_labels is None:
        axarr[0].set(ylabel='f(x)')
    else:
        axarr[0].set(ylabel=y_axis_labels[0])
    if f_range is not None:
        axarr[0].set(ylim=f_range)
    axarr[0].axhline(y=0, linestyle='-', color='black', linewidth=0.4)

    # variables
    for i in range(n_vars):
        axarr[1+i].plot(cols[0], cols[2+i])#, color=ser.color, alpha=0.5)
        axarr[1+i].plot(cols[0], Fig.get_moving_average(cols[2+i], window=window),'ko', markersize=1)
        if y_axis_labels is None:
            axarr[1+i].set(ylabel='x'+str(i))
        else:
            axarr[1+i].set(ylabel=y_axis_labels[i+1])
        if x_ranges is not None:
            axarr[1+i].set(ylim=x_ranges[i])

    # label the x-axis of the last figure
    axarr[n_vars].set(xlabel='Iteration')

    # align y labels
    f.align_ylabels()
    #
    plt.subplots_adjust(left=0.14, bottom=0.1, right=0.97, top=0.9,
                        wspace=0, hspace=0.5)

    plt.savefig(save_path+csv_file+'.png')
