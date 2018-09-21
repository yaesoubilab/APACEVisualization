import apace.TrajectoriesClasses1 as Cls

Cls.OUTPUT_TYPE = Cls.OutType.JPG

Cls.compare_trajectories(
    'csvfiles/TB1TrajBase.csv',
    'csvfiles/TB1TrajInt.csv',
    ['Base', 'Intervention'],
    'comparing_trajs'
)
