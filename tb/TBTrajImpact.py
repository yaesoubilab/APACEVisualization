import apace.TrajectoriesClasses as Vis
from tb import TBSettings as Set

SHOW_INTERVALS = False

# specify the output (show, save as .jpg, or save as .pdf)
Vis.OUTPUT_TYPE = Vis.OutType.JPG
Vis.X_LABEL = 'Year'
Vis.X_RANGE = [Set.PROJ-2, Set.TIME_END+1]
Vis.X_TICKS = [Set.PROJ-1, 5]

list_plot_info = []     # list of plot infos

# TB incidence
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Active TB Incidence | Per Pop.',
        y_range=[0, 2500], # 2000
        y_label='Incident TB cases per 100 000 population',
        y_multiplier=100000,
        # title="TB Incidence\n(Per 100,000 Pop.)",
        x_range=Vis.X_RANGE,
        figure_size=(4, 3.6),
        file_name='Impact-TBIncidence')
)

# TB prevalence
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Active TB (Ratio)',
        y_range=[0, 1000],
        y_label='TB Prevalence cases per 100 000 population',
        y_multiplier=100000,
        title="TB Prevalence\n(Per 100,000 Pop.)",
        x_range=Vis.X_RANGE,
        figure_size=(4, 3.6),
        file_name='Impact-TBPrevalence')
)

# TB mortality
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='TB Deaths | Per Pop.',
        y_range=[0, 350],
        y_label='TB Deaths per 100 000 population',
        y_multiplier=100000,
        title="TB Mortality\n(Per 100,000 Pop.)",
        x_range=Vis.X_RANGE,
        figure_size=(4, 3.6),
        file_name='Impact-TBMortality')
)

eff = Vis.ProjectedTrajectories(
    scenarios_csv_files=[
        'csv_files/TBTrajs0Base.csv',
        'csv_files/TBTrajs1Yr1NoIPT.csv',
        'csv_files/TBTrajs2AnnualNoIPT.csv',
        'csv_files/TBTrajs3Yr1WithIPT.csv',
        'csv_files/TBTrajs4AnnualWithIPT.csv'
    ],
    scenario_names=[
        'Base case (no targeted intervention)',
        'First-year follow-up',
        'Annual follow-up',
        'First-year follow-up with limited 2°IPT',
        'Annual follow-up with continuous 2°IPT'
    ],
    fig_infos=list_plot_info,
    time_0=Set.TIME_0,
    warm_up=Set.PROJ-Set.TIME_0-2,
    period_length=1,
    scenario_colors=['gray', 'red', 'blue', 'green', 'orange'],
    show_intervals=SHOW_INTERVALS, alpha=0.1
)

eff.plot_all(fig_folder='results/impact_time_series/')
eff.plot_multi_panel(file_name='results/impact_time_series/all.png')
