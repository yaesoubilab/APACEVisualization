from tb import TBSettings as Set
from apace import TrajectoriesClasses as Vis


# create a trajectory data frame
df = Vis.TrajsDataFrame('csvfiles/TBTrajs0Base.csv',
                        time0=Set.TIME_0,
                        period_length=1,
                        warmup_sim_period=Set.WARMUP,
                        warmup_sim_time=Set.WARMUP+1,
                        warmp_obs_period=Set.WARMUP,
                        warmup_epi_time=Set.WARMUP+1
                        )

# report incidence of TB in 2018
print(df.allTrajs['Active TB Incidence | Per Pop.'].get_mean_PI(Set.INDEX_PROJ, Set.ALPHA, multiplier=100))


