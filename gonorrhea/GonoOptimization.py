from apace import VisOptimClasses as Vis
import SimPy.InOutFunctions as IO

# delete existing figures
IO.delete_files('.png', '../gonorrhea/figures/optimization_figs/')

Vis.plot_all_opt_itrs(
    csv_directory='../gonorrhea/csvfiles/optimcsvfiles/',
    n_vars=4,
    save_plots_directory='../gonorrhea/figures/optimization_figs/',
    f_range=[-1e6, 1e6],
    var_ranges=[[0, 2], [-1, 0], [0, 0.5], [-0.05, 0.05]],
    y_axis_labels=[r'$f(\tau, \rho)$', r'$\tau_0$', r'$\tau_1$', r'$\rho_0$', r'$\rho_1$'],
    window=50
)
