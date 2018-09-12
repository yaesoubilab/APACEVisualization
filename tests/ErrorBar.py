import numpy as np
import matplotlib.pyplot as plt


x = [1, 2]
y = [3, 4]
x_err_l = [0.5, 1]
x_err_u = [1, 2]
y_err_l = [1, 2]
y_err_u = [3, 5]

x_err = [x_err_l, x_err_u]
y_err = [y_err_l, y_err_u]

fig, axs = plt.subplots(1, 1)
axs.plot(x, y, 'o')

#axs.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='none', color='k', linewidth=1)
axs.errorbar(1, 2, xerr=[[1],[2]], yerr=[[2], [4]], fmt='none', color='k', linewidth=1)

plt.show()
