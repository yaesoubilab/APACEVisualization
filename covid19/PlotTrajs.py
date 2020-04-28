from apace import TrajectoriesClasses as Vis

Vis.FEASIBLE_REGION_COLOR_CODE='pink'

# create a trajectory data frame
df = Vis.TrajsDataFrame('csv_files/Trajs.csv',
                        time0=0,
                        period_length=1,
                        warmup_sim_period=0,
                        warmup_sim_time=0,
                        warmp_obs_period=0,
                        warmup_epi_time=0
                        )

plotInfoIncidence = Vis.PlotTrajInfo(
        traj_name='Obs: Incident',
        y_range=[0, 40],
        y_multiplier=0.001,
        x_label='Week',
        x_range=[0, 52],
        y_label='\nWeekly incidence (Thousands)',
        title='',
        figure_size=(4, 3.2),
        file_name='figures/WeeklyCases.png')

plotInforICU = Vis.PlotTrajInfo(
        traj_name='Waiting for or in ICU',
        y_range=[0, 161],
        #y_multiplier=0.001,
        x_label='Week',
        x_range=[0, 52],
        x_multiplier=52,
        y_label='\nIndividuals requiring critical care\n(Per 100,000 population)',
        title='',
        figure_size=(4, 3.2),
        file_name='figures/ICU.png')
calibInfoICU = Vis.PlotCalibrationInfo(
    list_of_observed_outcomes=[],
    feasible_range_info=Vis.FeasibleRangeInfo(
        x_range=[0, 52], y_range=[0, 10.34]
    )
)

Vis.SUBPLOT_W_SPACE=0.1
df.plot_multi_panel(
    n_rows=1,
    n_cols=2,
    file_name='figures/Validation.png',
    list_plot_info=[plotInfoIncidence, plotInforICU],
    list_calib_info=[None, calibInfoICU],
    figure_size=(4.5, 2.25), l_b_r_t=(0.3, 0.1, 0.9, 0.9),
    show_subplot_labels=True)

df.plot(plot_info= plotInfoIncidence)


df.plot(plot_info=plotInforICU, calibration_info=calibInfoICU)
