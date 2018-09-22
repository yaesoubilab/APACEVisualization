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
      traj_df.allTrajs['Active TB Incidence | Per Pop.'].get_fromatted_mean_PI(
        time_index=Set.INDEX_PROJ, alpha=Set.ALPHA, multiplier=100000, deci=0, format=','))

print('TB incidence among naive in 2018 (per 100,000 population):',
      traj_df.allTrajs['Active TB Incidence | Naive Adults | Per Pop.'].get_fromatted_mean_PI(
        time_index=Set.INDEX_PROJ, alpha=Set.ALPHA, multiplier=100000, deci=0, format=','))

print('TB incidence among experienced in 2018 (per 100,000 population):',
      traj_df.allTrajs['Active TB Incidence | Experienced Adults | Per Pop.'].get_fromatted_mean_PI(
        time_index=Set.INDEX_PROJ, alpha=Set.ALPHA, multiplier=100000, deci=0, format=','))

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

