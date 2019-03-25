import SimPy.Optimization as opt


opt.plot_step_size(a0s=[0.1],
                   bs=[10, 25, 50, 75],
                   c0s=[0.05],
                   nItrs=1000)
