## http://markthegraph.blogspot.com/2015/05/using-python-statsmodels-for-ols-linear.html

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


class SingleVarPolyReg:

    def __init__(self, x, y):
        pass

    def get_predicted_y(self, x):
        pass

    def get_CI_y(self, x):
        pass

    def get_PI_y(self, x):
        pass



x = np.random.randn(100)
y = x*x + np.random.randn(100)
fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(x, y, alpha=0.5, color='orchid')
fig.suptitle('Example Scatter Plot')
fig.tight_layout(pad=2);
ax.grid(True)


X = np.column_stack((x, x ** 2))
X = sm.add_constant(X) # constant intercept term

# Model: y ~ x + c

model = sm.OLS(y, X)
fitted = model.fit()
x_pred = np.linspace(x.min(), x.max(), 50)
X_pred = np.column_stack((x_pred, x_pred ** 2))
X_pred = sm.add_constant(X_pred)
y_pred = fitted.predict(X_pred)
ax.plot(x_pred, y_pred, '-', color='darkorchid', linewidth=2)

y_hat = fitted.predict(X) # x is an array from line 12 above

y_err = y - y_hat

mean_x = x.T[1].mean()

n = len(x)

dof = n - fitted.df_model - 1

from scipy import stats

t = stats.t.ppf(1-0.025, df=dof)
s_err = np.sum(np.power(y_err, 2))
conf = t * np.sqrt((s_err/(n-2))*(1.0/n + (np.power((x_pred-mean_x),2) /
    ((np.sum(np.power(x_pred,2))) - n*(np.power(mean_x,2))))))

upper = y_pred + abs(conf)
lower = y_pred - abs(conf)

ax.fill_between(x_pred, lower, upper, color='#888888', alpha=0.4)


sdev, lower, upper = wls_prediction_std(fitted, exog=X_pred, alpha=0.05)

ax.fill_between(x_pred, lower, upper, color='#888888', alpha=0.1)



#fig.savefig('filename4.png', dpi=125)


plt.show()