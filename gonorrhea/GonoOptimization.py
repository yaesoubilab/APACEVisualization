from apace import VisOptimClasses as Vis
import SimPy.InOutFunctions as IO

# delete existing figures
IO.delete_files('.png', '../gonorrhea/figures/optimization_figs/')

Vis.plot_all_opt_itrs(
    csv_directory='../gonorrhea/csvfiles/optimcsvfiles/',
    n_vars=4,
    save_plots_directory='../gonorrhea/figures/optimization_figs/',
    f_range=[-10e6, 10e6],
    x_ranges=[[0, 0.5], [-0.5, 0.5], [0, 1], [-0.25, 0.25]],
    y_axis_labels=[r'$f(\tau, \theta)$', r'$\tau_1$', r'$\tau_2$', r'$\theta_1$', r'$\theta_2$']
)
