from apace import VisOptimClasses as Vis
import SimPy.InOutFunctions as IO

# delete existing figures
IO.delete_files('.png', '../tests/VisualizeOptimization/optimization_figures/')


Vis.plot_all_opt_itrs(
    csv_directory='../tests/VisualizeOptimization/optimization_csvfiles/',
    save_plots_directory='../tests/VisualizeOptimization/optimization_figures/',
    #f_range=[0, 5*10e7],
    #x_ranges=[[0, 0.3], [0, 0.2]],
    #y_axis_labels=[r'$f(\tau, \theta)$', r'$\tau$', r'$\theta$']
)
