import matplotlib.pyplot as plt

fig, ax = plt.subplots()


ax.plot_all(1, 2, 'ro', label='r0', markersize=10)
ax.plot_all(4, 5, 'b+', label='b+', markersize=14, mew=3)
ax.plot_all(2, 4, 'gx', label='gx', markersize=14, mew=3)

ax.plot_all([1, 4], [2, 5], color='k')

ax.legend()

plt.show()