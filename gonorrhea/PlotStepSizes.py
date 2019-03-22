import SimPy.Optimization as opt


opt.plot_step_size(a0s=[0.05, 0.1],
                   bs=[25, 50],
                   c0s=[0.05],
                   nItrs=500)
