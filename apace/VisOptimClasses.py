import SimPy.InOutFunctions as IO
import matplotlib.pyplot as plt
import os


def plot_all_opt_itrs(csv_directory, save_plots_directory, f_range=None, x_ranges=None):

    for name in os.listdir(csv_directory):
        plot_opt_itrs(
            path=csv_directory,
            csv_file=name,
            save_path=save_plots_directory,
            f_range=f_range,
            x_ranges=x_ranges
        )


def plot_opt_itrs(path, csv_file, save_path, f_range=None, x_ranges=None):

    cols = IO.read_csv_cols(path+csv_file,
                            n_cols=6,
                            if_ignore_first_row=True,
                            delimiter=',',
                            if_convert_float=True)

    # objective function
    f, axarr = plt.subplots(3, 1, sharex=True)
    axarr[0].set(title=csv_file)
    axarr[0].plot(cols[0], cols[1])#, color=ser.color, alpha=0.5)
    axarr[0].set(ylabel='f(x)')

    if f_range is not None:
        axarr[0].set(ylim=f_range)

    # variables
    nVars = int((len(cols)-2)/2)
    for i in range(nVars):
        axarr[1+i].plot(cols[0], cols[2+i])#, color=ser.color, alpha=0.5)
        axarr[1+i].set(ylabel='x'+str(i))
        if x_ranges is not None:
            axarr[1+i].set(ylim=x_ranges[i])

    axarr[nVars-1].set(xlabel='Iteration')

    plt.savefig(save_path+csv_file+'.png')
