from apace import TrajectoriesClasses1 as Vis

# specify the output (show, save as .jpg, or save as .pdf)
Vis.OUTPUT_TYPE = Vis.OutType.SHOW

# create a trajectory data frame
df = Vis.TrajsDataFrame('TrajsWithDR.csv')

# plot incidence
df.plot(Vis.PlotTrajInfo(
    traj_name='Incidence',
    x_label='Day',
    #x_range=[0, 20],
    y_range=[0, 100],
    title="Daily Influenza Cases",
    if_same_color=True,
    common_color_code='b',
    transparency=0.5,
    figure_size=(4, 3)
    )
)

# plot I
df.plot(Vis.PlotTrajInfo(
    traj_name='In: I',
    x_label='Day',
    #x_range=[0, 20],
    y_range=[0, 400],
    x_multiplier=364,
    title="Infected Cases",
    if_same_color=True,
    common_color_code='b',
    transparency=0.5,
    figure_size=(4, 3))
)

df.plot(Vis.PlotTrajInfo(
    traj_name='Obs: Incidence',
    x_label='Week',
    # x_range=[0, 7*7],
    y_range=[0, 500],
    title="Weekly Influenza Cases",
    is_x_integer= True,
    if_same_color=True,
    common_color_code='b',
    transparency=0.5,
    figure_size=(4, 3))
)

exit(0)
