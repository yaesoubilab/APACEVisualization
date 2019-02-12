import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111)
x = np.linspace(-20,20, 1000)
line_cosh, = ax.plot(x, x**3)
line_quad, = ax.plot(x, x**2/2)
ax.set_xlabel('test')
ax.set_ylabel('test')
plt.show()