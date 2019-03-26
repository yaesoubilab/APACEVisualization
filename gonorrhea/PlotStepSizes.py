import SimPy.Optimization as opt


opt.plot_step_size(a0s=[0.1, 0.05],
                   bs=[10, 25, 50],
                   c0s=[0.05],
                   nItrs=1000)
