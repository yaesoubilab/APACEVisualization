from apace import TrajectoriesClasses as Vis
import matplotlib.pyplot as plt
import os


def get_dfs(csv_file_names):
    dfs = []
    for name in csv_file_names:
        # create a trajectory data frame
        dfs.append(Vis.TrajsDataFrame(
            'csv_files/switches_on_trajs/'+name,
            time0=0,
            period_length=1,
            warmup_sim_period=0,
            warmup_sim_time=1,
            warmp_obs_period=0,
            warmup_epi_time=1))
    return dfs


dfs = get_dfs(csv_file_names=['No.csv', 'WTP100.csv', 'WTP200.csv'])

os.chdir('..')
fig, axes = plt.subplots(3, 1, figsize=(7.5, 7)) #sharex=True)

for i, df in enumerate(dfs):
    df.add_to_ax(
        ax=axes[i],
        plot_info=Vis.PlotTrajInfo(
            traj_name='Obs: To I',
            y_range=[0, 20],
            y_multiplier=0.001,
            x_label='Week',
            x_range=[0, 52],
            y_label='Weekly Number of Cases\n(Thousands)',
            title='',
            common_color_code='blue',
            transparency=1),
        trajs_ids_to_display=[0]
    )

fig.tight_layout()
fig.savefig('covid19/figures/SwitchesOnTrajs.png', dpi=300, bbox_inches='tight')
fig.show()
