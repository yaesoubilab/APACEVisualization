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
Vis.DEFAULT_FONT_SIZE = 5.5
Vis.SUBPLOT_H_SPACE = 0.75

# create a trajectory data frame
df = Vis.TrajsDataFrame('csvfiles/TBTrajs0Base.csv',
                        time0=TIME_0,
                        period_length=1,
                        warmup_sim_period=WARMUP,
                        warmup_sim_time=WARMUP+1,
                        warmp_obs_period=WARMUP,
                        warmup_epi_time=WARMUP+1
                        )

list_plot_info = []
list_plot_calib_info = []

######### ROW 1 #################
# Notified TB, Children
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.NotifiedTBChildren)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Notified TB Cases | Children',
        y_range=[0, 300],
        y_label='Number of case notifications',
        title="Annual number of TB notifications \namong children",
        figure_size=(4, 3.2),
        file_name='Notified Cases (Children)'
    )
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=None,
            fill_between=False
        )
    )
)

# Notified TB, Naive
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.NotifiedTBNaiveAdults)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Notified TB Cases | Naive Adults',
        y_range=[0, 600],
        y_label='Number of case notifications',
        title="Annual number of TB notifications \namong treatment-naïve adults",
        figure_size=(4, 3.2),
        file_name='Notified Cases (Naive)')
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=None,
            fill_between=False
        )
    )
)

# Notified TB, Experienced
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.NotifiedTBExpAdults)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Notified TB Cases | Experienced Adults',
        y_range=[0, 400],
        y_label='Number of case notifications',
        title="Annual number of TB notifications \namong treatment-experienced adults",
        figure_size=(4, 3.2),
        file_name='Notified Cases (Experienced)')
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=None,
            fill_between=False
        )
    )
)

######### ROW 2 #################
# Children Population
# data
obs = Vis.convert_data_to_list_of_observed_outcomes(D.PopChildren)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Population | Children',
        y_range=[8000, 15000],
        y_multiplier=1,
        y_label='Number of individuals',
        title="Number of children",
        figure_size=(4, 3.2),
        file_name='Children Population')
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obs,
        if_connect_obss=False,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=[9000, 13000]
        )
    )
)

# Adults Population
# data
obs = Vis.convert_data_to_list_of_observed_outcomes(D.PopAdults)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Population | Adults',
        y_range=[20000, 35000],
        y_multiplier=1,
        y_label='Number of individuals',
        title="Number of adults",
        figure_size=(4, 3.2),
        file_name='Adults Population')
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obs,
        if_connect_obss=False,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=[24000, 30000]
        )
    )
)

# HIV Prevalence
# data
obs = Vis.convert_data_to_list_of_observed_outcomes(D.PrevHIV)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='HIV Prevalence (Ratio)',
        y_range=[0, 15],
        y_multiplier=100,
        y_label='Prevalence (%)',
        title="HIV prevalence among adults",
        figure_size=(4, 3.2),
        file_name='HIV Prevalence')
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obs,
        if_connect_obss=False,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=[2.6, 10.5]
        )
    )
)

######### ROW 3 #################
# Prevalence of Treatment Experienced Adults
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PrevExpAdult)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Experienced Adults Prevalence (Ratio)',
        y_range=[0, 25],
        y_multiplier=100,
        y_label='Percentage',
        title="Percentage of adults with \nprevious treatment",
        figure_size=(4, 3.2),
        file_name='Treatment-Experienced Adults')
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0 + WARMUP + 1, TIME_0 + WARMUP + 7],
            y_range=[5, 15]
        )
    )
)

# TB Prevalence among Treatment-Naive Adults
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PrevTBNaiveAdult)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Active TB among Naive Adults (Ratio)',
        y_range=[0, 2],
        y_multiplier=100,
        y_label='Tuberculosis prevalence (%)',
        title="TB prevalence among \ntreatment-naïve adults",
        figure_size=(4, 3.2),
        file_name='TB among Treatment-Native Adults')
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0 + WARMUP + 1, TIME_0 + WARMUP + 7],
            y_range=[0, 1.5]
        )
    )
)

# TB Prevalence among Treatment-Experienced Adults
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PrevTBExpAdult)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Active TB among Experienced Adults (Ratio)',
        y_range=[0, 10],
        y_multiplier=100,
        y_label='Tuberculosis prevalence (%)',
        title="TB prevalence among \ntreatment-experienced adults",
        figure_size=(4, 3.2),
        file_name='TB among Treatment-Experienced Adults')
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0 + WARMUP + 1, TIME_0 + WARMUP + 7],
            y_range=[0, 6]
        )
    )
)

######### ROW 4 #################
# % recurrent TB in year 1
# data
obss = Vis.convert_data_to_list_of_observed_outcomes(D.PrecRecTBInYr1)
# plot
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='% <1 |Incident To: I| Tc<1 or >1 |HIV-',
        y_range=[0, 50],
        y_multiplier=100,
        title="Percentage of recurrent TB cases\noccurring within a year of\nprevious 'successful' treatment",
        y_label="Percentage"
    )
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=None,
            fill_between=False
        )
    )
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
        title="Percentage of recurrences within\n1 year of previous treatment\nthat are due to reactivation",
        y_label="Percentage"
    )
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=None,
            fill_between=False
        )
    )
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
        title="Percentage of recurrences occurring"
              "\ngreater that 1 year after previous\ntreatment that are due to reactivation",
        y_label="Percentage"
    )
)
list_plot_calib_info.append(
    Vis.PlotCalibrationInfo(
        list_of_observed_outcomes=obss,
        if_connect_obss=True,
        feasible_range_info=Vis.FeasibleRangeInfo(
            x_range=[TIME_0+WARMUP+1, TIME_0+WARMUP+7],
            y_range=None,
            fill_between=False
        )
    )
)

################

# plot multi_plot
df.plot_multi_panel(4, 3,
                    file_name='Calibration',
                    list_plot_info=list_plot_info,
                    list_calib_info=list_plot_calib_info,
                    figure_size=(6.4, 7),
                    share_x=True)
