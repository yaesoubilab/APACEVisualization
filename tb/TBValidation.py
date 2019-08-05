from apace import TrajectoriesClasses1 as Vis
from tb import TBData as D

WARMUP = 10
TIME_0 = 1991
TIME_END = TIME_0 + 34


# specify the output (show, save as .jpg, or save as .pdf)
Vis.OUTPUT_TYPE = Vis.OutType.JPG
Vis.X_LABEL = 'Year'
Vis.X_RANGE = [TIME_0+WARMUP-1, TIME_END+2]
Vis.X_TICKS = [TIME_0+WARMUP-1, 10]
# coordinates of y-axis labels
Vis.Y_LABEL_COORD_X = -0.15
Vis.SUBPLOT_W_SPACE = 0.7

# create a trajectory data frame
df = Vis.TrajsDataFrame('csv_files/TBTrajs0Base.csv',
                        time0=TIME_0,
                        period_length=1,
                        warmup_sim_period=WARMUP,
                        warmup_sim_time=WARMUP+1,
                        warmp_obs_period=WARMUP,
                        warmup_epi_time=WARMUP+1
                        )

list_plot_info = []
list_plot_obs_info = []
list_feasible_range_info = []

######### ROW 1 #################
# % recurrent TB in year 1
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PrecRecTBInYr1)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='% <1 |Incident To: I| Tc<1 or >1 |HIV-',
        y_range=[0, 50],
        y_multiplier=100,
        title="Recurrent TB after successful \ncompletion of TB treatment",
        y_label="Occurred within a year (%)"
    )
)
list_plot_obs_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True)
)
list_feasible_range_info.append(
    Vis.FeasibleRangeInfo(
        x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
        y_range=None,
        fill_between=False)
)

# % recurrent TB in year 1 due to reactivation
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PrecRecTBYr1DueReact)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='% reactivation |Incident To: I | Tc <1| HIV -',
        y_range=[0, 100],
        y_multiplier=100,
        title="Recurrent TB within 1 year \nafter successful completion \nof TB treatment",
        y_label="Occurred due to TB reactivation (%)"
    )
)
list_plot_obs_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True)
)
list_feasible_range_info.append(
    Vis.FeasibleRangeInfo(
        x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
        y_range=None,
        fill_between=False)
)

# % recurrent TB after year 1 due to reactivation
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PrecRecTBAfterYr1DueReact)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='% reactivation |Incident To: I | Tc >1| HIV -',
        y_range=[0, 100],
        y_multiplier=100,
        title="Recurrent TB in >1 years \nafter successful completion \nof TB treatment",
        y_label="Occurred due to TB reactivation (%)"
    )
)
list_plot_obs_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True)
)
list_feasible_range_info.append(
    Vis.FeasibleRangeInfo(
        x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
        y_range=None,
        fill_between=False)
)


################

# plot multi_plot
df.plot_multi_panel(1, 3,
                    file_name='Validation',
                    list_plot_info=list_plot_info,
                    list_calib_info=list_plot_obs_info,
                    list_feas_range_info=list_feasible_range_info,
                    figure_size=(6.4, 2),
                    share_x=True)
