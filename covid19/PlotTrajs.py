from apace import TrajectoriesClasses as Vis

# create a trajectory data frame
df = Vis.TrajsDataFrame('csv_files/Trajs.csv',
                        time0=0,
                        period_length=1,
                        warmup_sim_period=0,
                        warmup_sim_time=0,
                        warmp_obs_period=0,
                        warmup_epi_time=0
                        )

df.plot(
    plot_info=Vis.PlotTrajInfo(
        traj_name='Obs: Incident',
        y_range=[0, 40],
        y_multiplier=0.001,
        x_label='Week',
        x_range=[0, 52],
        y_label='Weekly Number of Cases\n(Thousands)',
        title='',
        figure_size=(4, 3.2),
        file_name='figures/WeeklyCases.png'
    )
)

Vis.FEASIBLE_REGION_COLOR_CODE='pink'
df.plot(
    plot_info=Vis.PlotTrajInfo(
        traj_name='Waiting for or in ICU',
        y_range=[0, 161],
        #y_multiplier=0.001,
        x_label='Week',
        x_range=[0, 52],
        x_multiplier=52,
        y_label='Number of individuals\nrequiring critical care\n(Per 100,000 population)',
        title='',
        figure_size=(4, 3.2),
        file_name='figures/ICU.png'
    ),
    calibration_info=Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=[],
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[0, 52], y_range=[0, 10.34]
        )
    )
)
