from apace import TrajectoriesClasses1 as Vis

# specify the output (show, save as .jpg, or save as .pdf)
Vis.OUTPUT_TYPE = Vis.OutType.SHOW

# create a trajectory data frame
df = Vis.TrajsDataFrame("tests\Trajectories.csv")

traj_names = ["To: I", "Incidence", "In: S", "In: I", "In: R", "Obs: Incidence"]
list_plot_info = []
for traj_name in traj_names:
    list_plot_info.append(Vis.PlotTrajInfo(
        traj_name=traj_name,
        x_label='Week',
        title="Influenza Cases",
        transparency=0.4,
        figure_size=(6, 4))
    )
df.plot_multi_panel(2, 3, list_plot_info)


exit(0)
