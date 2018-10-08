import apace.TrajectoriesClasses as Cls

Cls.OUTPUT_TYPE = Cls.OutType.JPG

Cls.compare_trajectories(
    'csvfiles/TrajsDebug.csv',
    'csvfiles/TrajsDebug.csv',
    ['Base', 'Intervention'],
    'comparing_trajs'
)
