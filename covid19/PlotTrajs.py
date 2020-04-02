from apace import TrajectoriesClasses as Vis

# create a trajectory data frame
df = Vis.TrajsDataFrame('csv_files/Trajs.csv',
                        time0=0,
                        period_length=1,
                        warmup_sim_period=0,
                        warmup_sim_time=1,
                        warmp_obs_period=0,
                        warmup_epi_time=1
                        )

df.plot(
    plot_info=Vis.PlotTrajInfo(
        traj_name='Obs: To I',
        y_range=[0, 50000],
        x_label='Week',
        x_range=[0, 52],
        y_label='Weekly Number of Cases',
        title='',
        figure_size=(4, 3.2),
        file_name='figures/WeeklyCases'
    )
)
