from apace import VisOptimClasses as Vis
import SimPy.InOutFunctions as IO

# delete existing figures_national
IO.delete_files('.png', 'figures/optimization_figs/')

Vis.plot_all_opt_itrs(
    csv_directory='csv_files/optimization_csvs/',
    n_vars=3,
    save_plots_directory='figures/optimization_figs/',
    #f_range=[-1e6, 1e6],
    var_ranges=[[0, 10], [-2, 0], [0, 1], [-0.000025, 0]],
    y_axis_labels=[r'$f(\tau, \rho)$', r'$\tau_0$', r'$\tau_1$', r'$\rho_0$', r'$\rho_1$'], # , r'$\rho_1$'
    window=20
)
