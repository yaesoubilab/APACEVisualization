import apace.TrajectoriesClasses as Cls

Cls.OUTPUT_TYPE = Cls.OutType.JPG

Cls.compare_trajectories(
    'csvfiles/TrajsDebugBase.csv',
    'csvfiles/TrajsDebugIntr.csv',
    ['Base', 'Intervention'],
    'comparing_trajs'
)
