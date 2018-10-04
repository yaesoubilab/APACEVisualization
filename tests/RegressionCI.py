#https://www.statsmodels.org/dev/examples/notebooks/generated/ols.html

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

# fit a quadratic function to data and display confidence
#

N_SAMPLES = 100
ERR_VAR = 1

########
np.random.seed(0)

# true quadratic function: y = 1 - 8x + 4x^2
beta = np.array([1, -8, 4])

# sample x values
x = np.linspace(0, 2, N_SAMPLES)

# create the matrix X (of least square)
X = np.column_stack((x, x**2))
X = sm.add_constant(X)  # add constant to X

# sample errors
e = np.random.normal(0, ERR_VAR, size=N_SAMPLES)

# y = beta*X + error
y = np.dot(X, beta) + e

# create the regression model
model = sm.OLS(y, X)

# fit the model
results = model.fit()

# read predicted values along with prediction interval
prstd, iv_l, iv_u = wls_prediction_std(results)

# print results
print(results.summary())
print('Parameters: ', results.params)
print('R2: ', results.rsquared)

# plot
fig, ax = plt.subplots(figsize=(8,6))
ax.plot(x, y, 'o', label="data")
#ax.plot(x, y_true, 'b-', label="True")
ax.plot(x, results.fittedvalues, 'r--.', label="OLS")
ax.plot(x, iv_u, 'r--')
ax.plot(x, iv_l, 'r--')
ax.fill_between(x, iv_l, iv_u, color='#888888', alpha=0.1)
ax.legend(loc='best')
plt.show()