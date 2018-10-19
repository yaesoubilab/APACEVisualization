from apace import VisOptimClasses as Vis
import SimPy.InOutFunctions as IO

# delete existing figures
IO.delete_files('.png', '../gonorrhea/figures/optimization_figs/')

Vis.plot_all_opt_itrs(
    csv_directory='../gonorrhea/csvfiles/optimcsvfiles/',
    save_plots_directory='../gonorrhea/figures/optimization_figs/',
    f_range=[0, 5*10e8],
    x_ranges=[[0, 0.3], [0, 0.2]],
    y_axis_labels=[r'$f(\tau, \theta)$', r'$\tau$', r'$\theta$']
)
