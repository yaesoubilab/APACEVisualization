from apace import TrajectoriesClasses as Vis
from tb import TBData as D
from tb import TBSettings as Set


# specify the default settings of the visualization module
Vis.OUTPUT_TYPE = Vis.OutType.JPG
Vis.TRAJ_TRANSPARENCY = 0.2
Vis.X_LABEL = 'Year'
Vis.X_RANGE = [Set.TIME_0+Set.WARMUP-1, Set.TIME_END+2]
Vis.X_TICKS = [Set.TIME_0+Set.WARMUP-1, 10]
Vis.DEFAULT_FONT_SIZE = 5.5
Vis.SUBPLOT_H_SPACE = 0.75

# create a trajectory data frame
df = Vis.TrajsDataFrame('csv_files/TBTrajs0Base.csv',
                        time0=Set.TIME_0,
                        period_length=1,
                        warmup_sim_period=Set.WARMUP,
                        warmup_sim_time=Set.WARMUP+1,
                        warmp_obs_period=Set.WARMUP,
                        warmup_epi_time=Set.WARMUP+1
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
            y_range=[9500, 12500]
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
            y_range=[2.7, 7.7]
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
            x_range=[Set.TIME_0 + Set.WARMUP + 1, Set.TIME_0 + Set.WARMUP + 7],
            y_range=[5.7, 13.7]
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
            x_range=[Set.TIME_0 + Set.WARMUP + 1, Set.TIME_0 + Set.WARMUP + 7],
            y_range=[0, 1.25]
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
            x_range=[Set.TIME_0 + Set.WARMUP + 1, Set.TIME_0 + Set.WARMUP + 7],
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
            y_range=[15, 50]
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
            y_range=[50, 100]
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
            x_range=[Set.TIME_0+Set.WARMUP+1, Set.TIME_0+Set.WARMUP+7],
            y_range=[10, 60]
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
