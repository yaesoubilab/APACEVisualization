from tb import TBSettings as Set
from apace import TrajectoriesClasses as Vis
from apace import ParametersClasses as Param
from apace import ScenariosClasses as Sce


# create a trajectory data frame
traj_df = Vis.TrajsDataFrame('csvfiles/TBTrajs0Base.csv',
                             time0=Set.TIME_0,
                             period_length=1,
                             warmup_sim_period=Set.WARMUP,
                             warmup_sim_time=Set.WARMUP+1,
                             warmp_obs_period=Set.WARMUP,
                             warmup_epi_time=Set.WARMUP+1
                             )
print('')

print('TB incidence in 2018 (per 100,000 population):',
      traj_df.allTrajs['Active TB Incidence | Per Pop.'].get_mean_PI(
        time_index=Set.INDEX_PROJ, alpha=Set.ALPHA, multiplier=100000, deci=0, format=','))

print('TB incidence among naive in 2018 (per 100,000 population):',
      traj_df.allTrajs['Active TB Incidence | Naive Adults | Per Pop.'].get_mean_PI(
        time_index=Set.INDEX_PROJ, alpha=Set.ALPHA, multiplier=100000, deci=0, format=','))

print('TB incidence among experienced in 2018 (per 100,000 population):',
      traj_df.allTrajs['Active TB Incidence | Experienced Adults | Per Pop.'].get_mean_PI(
        time_index=Set.INDEX_PROJ, alpha=Set.ALPHA, multiplier=100000, deci=0, format=','))

print('Decline in tuberculosis incidence between 2018 and 2027:',
      traj_df.allTrajs['Active TB Incidence | Per Pop.'].get_relative_diff_mean_PI(
        time_index0=Set.INDEX_PROJ-1, time_index1=Set.INDEX_PROJ+10-2, order=1, deci=1, format='%'))

# create a dictionary of parameters
param_df = Param.Parameters('csvfiles\SampledParams.csv')
print('')

print('Prob of progression following reinfection after complete TB treatment to latently infected and treatment-naive:',
      param_df.get_ratio_mean_interval(
          numerator_par_name='Prob: If progress | L | Tc <1| HIV -',
          denominator_par_names='Prob: If progress | L | Tn| HIV -', deci=1, form=','))

print('Rate of reactivation (relapse) after treatment completion in the first year post-treatment :',
      param_df.get_mean_interval('Rate: TB Reactivation | L | Tc <1| HIV -', 4, form=','))

print('Rate of reactivation (relapse) after treatment completion after the first year post-treatment :',
      param_df.get_mean_interval('Rate: TB Reactivation | L | Tc >1| HIV -', 4, form=','))

# data frame for scenario analysis
scenario_df = Sce.ScenarioDataFrame('csvfiles\TBScenarios.csv')
print('')
print('% incident TB cases due to reactivation occurring among those who had completed TB treatment:',
      scenario_df.get_mean_interval(
          scenario_name='Base',
          outcome_name='Average ratio: % reactivation |Incident To: I| Tc<1 or >1 |HIV-',
          deci=1, form='%'))

print('% incident TB averted:',
      scenario_df.get_relative_diff_mean_interval(
          scenario_names=['75% PTFU | No >1 FU | No IPT',
                          '75% PTFU | With >1 FU | No IPT',
                          '75% PTFU | No >1 FU | With IPT',
                          '75% PTFU | With >1 FU | With IPT'],
          scenario_name_base='Base',
          outcome_name='Total: Active TB Incidence',
          deci=1, form='%'))

print('% TB deaths averted:',
      scenario_df.get_relative_diff_mean_interval(
          scenario_names=['75% PTFU | No >1 FU | No IPT',
                          '75% PTFU | With >1 FU | No IPT',
                          '75% PTFU | No >1 FU | With IPT',
                          '75% PTFU | With >1 FU | With IPT'],
          scenario_name_base='Base',
          outcome_name='Total: TB Deaths',
          deci=1, form='%'))
