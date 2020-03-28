from apace import VisOptimClasses as Vis
import SimPy.InOutFunctions as IO

# delete existing figures_national
IO.delete_files('.png', 'figures/optimization_figs/')

Vis.plot_all_opt_itrs(
    csv_directory='csv_files/optimization_csvs/',
    n_vars=4,
    save_plots_directory='figures/optimization_figs/',
    #f_range=[-1e6, 1e6],
    var_ranges=[[0, 5], [-0.0005, 0], [0, 5], [-0.0005, 0]],
    y_axis_labels=[r'$f(\tau, \rho)$', r'$\tau_0$', r'$\tau_1$', r'$\rho_0$', r'$\rho_1$'], # , r'$\rho_1$'
    window=20
)
