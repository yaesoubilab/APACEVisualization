from apace import VisOptimClasses as Vis
import SimPy.InOutFunctions as IO

# delete existing figures_national
IO.delete_files('.png', 'figures/optimization_figs/')

Vis.plot_all_opt_itrs(
    csv_directory='csv_files/optimization_csvs/',
    n_vars=6,
    save_plots_directory='figures/optimization_figs/',
    show_titles=False,
    #f_range=[-1e6, 1e6],
    var_ranges=[[0, 4], [-1, 0], [0, 0.5], [0, 1], [-1, 0], [0, 1]],
    y_axis_labels=[r'$f$', r'$\tau_0$', r'$\tau_1$', r'$\rho_0$', r'$\rho_1$', '', ''], # , r'$\rho_1$'
    window=20
)
