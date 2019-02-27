from apace import TrajectoriesClasses as Vis
from gonorrhea import GonoData as D
from gonorrhea import GonoSettings as Set

SIM_LENGTH = 25+1+25  # simulation length in years

Vis.OUTPUT_TYPE = Vis.OutType.JPG    # figure output
Vis.X_LABEL = 'Year'
Vis.X_RANGE = [-1, SIM_LENGTH]
Vis.X_TICKS = [0, 10]
Vis.DEFAULT_FONT_SIZE = 7
Vis.Y_LABEL_COORD_X = -0.3
Vis.SUBPLOT_W_SPACE = 1
Vis.SUBPLOT_H_SPACE = 0.7

RESIST_PROFILE = ['A', 'B', 'AB']       # resistant profiles

# create a trajectory data frame
df = Vis.TrajsDataFrame(Set.SELECTED_CALIB_FILE_NAME)

list_plot_info = []
list_plot_calib_info = []

# plot prevalence
obss = Vis.convert_data_to_list_of_observed_outcomes(D.Prevalence)
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Prevalence G',
        y_range=[0, 5],
        is_x_integer=True,
        y_multiplier=100,
        figure_size=(4, 3.2),
        title="Gonorrhea prevalence",
        y_label='Prevalence (%)'
    )
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=False,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[1, 10],
            y_range=[2, 2],
            fill_between=False)
    )
)

# Rate of gonorrhea cases
obss = Vis.convert_data_to_list_of_observed_outcomes(D.GonorrheaRate)
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Annual rate of gonorrhea cases',
        y_range=[0, 9000],
        is_x_integer=True,
        y_multiplier=100000,
        figure_size=(4, 3.2),
        title="Annual gonorrhea rate",
        y_label='Cases per 100,000 MSM population'
    )
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=False,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[1, 10],
            y_range=[0.01*100000, 0.06*100000],
            fill_between=False
        )
    )
)

# % symptomatic cases
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PercSymtomatic)
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='% Received 1st Tx & Symptomatic',
        y_range=[0, 100],
        is_x_integer=True,
        y_multiplier=100,
        figure_size=(4, 3.2),
        title="Proportion of detected\ncases that are symptomatic",
        y_label='Percentage (%)'
    )
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=False,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[1, 10],
            y_range=[50, 100],
            fill_between=False
        )
    )
)

# plot resistant to A, B, AB among those who received 1st-line treatment
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PercentCiprofloxacinResistant)
for r in RESIST_PROFILE:
    obsInfo = None
    # if r == 'A':
    #     obsInfo = Vis.PlotCalibrationInfo(
    #         list_of_observed_outcomes=obss,
    #         if_connect_obss=False,
    #         feasible_range_info=Vis.FeasibleRangeInfo(
    #             x_range=[1, 5],
    #             y_range=[0, 0]
    #         )
    #     )
    list_plot_calib_info.append(obsInfo)

    if r == 'AB':
        y_range = [0, 40]
    else:
        y_range = [0, 40]

    list_plot_info.append(
        Vis.PlotTrajInfo(
            traj_name='Obs: % Received 1st Tx & Rst to {0}'.format(r),
            y_range=y_range,
            is_x_integer=True,
            y_multiplier=100,
            title='Proportion of gonorrhea\ncases resistant to {0}'.format(r),
            y_label='Percentage (%)',
            file_name='Traj-Resistant to ' + r)
    )


################
# plot multi_plot
df.plot_multi_panel(2, 3,
                    file_name='Calibration',
                    list_plot_info=list_plot_info,
                    list_calib_info=list_plot_calib_info,
                    show_subplot_labels=True,
                    share_x=True)
