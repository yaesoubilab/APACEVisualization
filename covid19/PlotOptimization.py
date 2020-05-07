from apace import VisOptimClasses as Vis
import SimPy.InOutFunctions as IO

# delete existing figures_national
IO.delete_files('.png', 'figures/optimization_figs/')

Vis.plot_all_opt_itrs(
    csv_directory='csv_files/optimization_csvs/',
    n_vars=4,
    save_plots_directory='figures/optimization_figs/',
    show_titles=False,
    #f_range=[-1e6, 1e6],
    #var_ranges=[[0, 5], [-1, 0], [0, 0.5], [0, 1000], [-1, 0], [0, 1]],
    y_axis_labels=[r'$f$',
                   r'$R: \tau_0$', r'$R: \tau_1$', r'$R: \rho$',
                   r'$\%I: \tau_0$', r'$\%I: \tau_1$', r'$\%I: rho$'], # , r'$\rho_1$'
    window=20
)
