import apace.TrajectoriesClasses as Cls

Cls.OUTPUT_TYPE = Cls.OutType.JPG

Cls.compare_trajectories(
    'csv_files/TB1TrajBase.csv',
    'csv_files/TB1TrajInt.csv',
    ['Base', 'Intervention'],
    'comparing_trajs'
)
