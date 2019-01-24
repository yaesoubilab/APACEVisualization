from tb import TBSettings as Set
from apace import TrajectoriesClasses as Vis
from apace import ParametersClasses as Param
from apace import ScenariosClasses as Sce

scenario_names = ['Baseline',
                  'Follow-up at yr 1, No IPT',
                  'Annual follow-up, No IPT',
                  'Follow-up at yr 1, With IPT',
                  'Annual follow-up, With IPT']

scenario_keys = ['75% PTFU | No >1 FU | Drop % | No IPT',
                 '75% PTFU | With >1 FU | Drop 15% | No IPT',
                 '75% PTFU | No >1 FU | Drop % | With IPT',
                 '75% PTFU | With >1 FU | Drop 15% | With IPT']

csvfiles_trajs = ['csvfiles/TBTrajs0Base.csv',
                  'csvfiles/TBTrajs1Yr1NoIPT.csv',
                  'csvfiles/TBTrajs2AnnualNoIPT.csv',
                  'csvfiles/TBTrajs3Yr1WithIPT.csv',
                  'csvfiles/TBTrajs4AnnualWithIPT.csv'
                  ]

# create trajectory data frames
traj_data_frames = []
for file_name in csvfiles_trajs:
    traj_data_frames.append(
        Vis.TrajsDataFrame(csv_file_name=file_name,
                           time0=Set.TIME_0,
                           period_length=1,
                           warmup_sim_period=Set.WARMUP,
                           warmup_sim_time=Set.WARMUP + 1,
                           warmp_obs_period=Set.WARMUP,
                           warmup_epi_time=Set.WARMUP + 1
                           )
    )

# create a dictionary of parameters
param_df = Param.Parameters('csvfiles\SampledParams.csv')

# data frame for scenario analysis
scenario_df = Sce.ScenarioDataFrame('csvfiles\TBScenarios.csv')

# ---------------------------------------------
# Epidemiological characteristics at base line
# ---------------------------------------------
print('')
print('TB incidence in 2018 (per 100,000 population):',
      traj_data_frames[0].allTrajs['Active TB Incidence | Per Pop.'].get_mean_PI(
        time_index=2018-Set.TIME_0-Set.WARMUP, alpha=Set.ALPHA, multiplier=1, deci=1, format='%'))

print('TB incidence among naive in 2018 (per 100,000 population):',
      traj_data_frames[0].allTrajs['Active TB Incidence | Naive Adults | Per Pop.'].get_mean_PI(
        time_index=2018-Set.TIME_0-Set.WARMUP, alpha=Set.ALPHA, multiplier=1, deci=1, format='%'))

print('TB incidence among experienced in 2018 (per 100,000 population):',
      traj_data_frames[0].allTrajs['Active TB Incidence | Experienced Adults | Per Pop.'].get_mean_PI(
        time_index=2018-Set.TIME_0-Set.WARMUP, alpha=Set.ALPHA, multiplier=1, deci=1, format='%'))

# ---------------------------------------------
# Decline in TB incidence between 2018 and 2027
# ---------------------------------------------
print('')
for i, traj_df in enumerate(traj_data_frames):
    print('Decline in tuberculosis incidence between 2018 and 2028 ({0}):'.format(scenario_names[i]),
          traj_df.allTrajs['Active TB Incidence | Per Pop.'].get_relative_diff_mean_PI(
              time_index0=2018-Set.TIME_0-Set.WARMUP,
              time_index1=Set.TIME_END-Set.TIME_0-Set.WARMUP-1, order=1, deci=1, format='%'))

# ---------------------------------------------
# Parameter posterior at base line
# ---------------------------------------------
print('')
# print('Prob of progression following reinfection after complete TB treatment to latently infected and treatment-naive:',
#       param_df.get_ratio_mean_interval(
#           numerator_par_name='Prob: If progress | L | Tc <1| HIV -',
#           denominator_par_names='Prob: If progress | L | Tn| HIV -', deci=1, form=','))

print('Rate of reactivation (relapse) after treatment completion in the first year post-treatment :',
      param_df.get_mean_interval('Rate: TB Reactivation | L | Tc <1| HIV -', 4, form=','))

print('Rate of reactivation (relapse) after treatment completion after the first year post-treatment :',
      param_df.get_mean_interval('Rate: TB Reactivation | L | Tc >1| HIV -', 4, form=','))

print('% incident TB cases due to reactivation occurring among those who had completed TB treatment:',
      scenario_df.get_mean_interval(
          scenario_name='Base',
          outcome_name='Average ratio: % reactivation |Incident To: I| Tc<1 or >1 |HIV-',
          deci=0, form='%'))

# ---------------------------------------------
# TB incidence and death averted under each scenario
# ---------------------------------------------
print('')
print('% incident TB averted:',
      scenario_df.get_relative_diff_mean_interval(
          scenario_names=scenario_keys,
          scenario_name_base='Base',
          outcome_name='Total: Active TB Incidence',
          deci=1, form='%'))

print('% TB deaths averted:',
      scenario_df.get_relative_diff_mean_interval(
          scenario_names=scenario_keys,
          scenario_name_base='Base',
          outcome_name='Total: TB Deaths',
          deci=1, form='%'))

scenario_df.plot_relative_diff_by_scenario(
    scenario_name_base='Base',
    scenario_names=scenario_keys,
    outcome_names=['Total: Active TB Incidence', 'Total: TB Deaths'],
    title='Percentage of incidence TB cases\nand deaths averted',
    x_label='Percentage (%)',
    y_labels=[
        'Follow-up at yr 1, No IPT',
        'Annual follow-up, No IPT',
        'Follow-up at yr 1, With IPT',
        'Annual follow-up, With IPT'],
    legend=('TB Incidence', 'TB Death'),
    distance_from_axis=0.6,
    filename='figures/cea/ComparativeEffect'
)
