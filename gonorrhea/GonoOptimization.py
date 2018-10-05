from apace import VisOptimClasses as Vis


Vis.plot_all_opt_itrs(
    csv_directory='../gonorrhea/csvfiles/optimcsvfiles/',
    save_plots_directory='../gonorrhea/figures/optimization_figs/',
    f_range=[0, 10e8],
    x_ranges=[[0, 0.3], [0, 0.2]]
)
