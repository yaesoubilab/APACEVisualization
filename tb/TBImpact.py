import apace.TrajectoriesClasses as Vis
from tb import TBSettings as Set

# specify the output (show, save as .jpg, or save as .pdf)
Vis.OUTPUT_TYPE = Vis.OutType.JPG
Vis.X_LABEL = 'Year'
Vis.X_RANGE = [Set.PROJ-2, Set.TIME_END+2]
Vis.X_TICKS = [Set.PROJ-1, 5]

list_plot_info = []     # list of plot infos

# TB incidence
list_plot_info.append(
    Vis.PlotTrajInfo(
        traj_name='Active TB Incidence | Per Pop.',
        y_range=[0, 2000],
        y_label='Incident TB cases per 100 000 population',
        y_multiplier=100000,
        title="TB Incidence\n(Per 100,000 Pop.)",
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
        figure_size=(4, 3.6),
        file_name='Impact-TBMortality')
)

eff = Vis.TrajImpact(
    scenarios_csv_files=[
        'csvfiles/TBTrajs0Base.csv',
        'csvfiles/TBTrajs1Yr1NoIPT.csv',
        'csvfiles/TBTrajs2AnnualNoIPT.csv',
        'csvfiles/TBTrajs3Yr1WithIPT.csv',
        'csvfiles/TBTrajs4AnnualWithIPT.csv'
    ],
    scenario_names=[
        'Baseline (no targeted intervention)',
        'First-year follow-up',
        'Annual follow-up',
        'First-year follow-up with limited IPT',
        'Annual follow-up with continuous IPT'
    ],
    fig_infos=list_plot_info,
    time_0=Set.TIME_0,
    warm_up=Set.PROJ-Set.TIME_0-2,
    period_length=1
)

eff.plot_all()
eff.plot_multi_panel()
