from scipy import stats
import numpy as np
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


class PolyRegressionFunction:
    def __init__(self):
        pass

    def get_X(self, x):
        pass


class QuadPolyRegFunction (PolyRegressionFunction):

    def get_X(self, x):
        X = np.column_stack((x, x ** 2))
        return sm.add_constant(X)


class CubicPolyRegFunction (PolyRegressionFunction):

    def get_X(self, x):
        X = np.column_stack((x, x ** 2, x**3))
        return sm.add_constant(X)


class SingleVarRegression:

    def __init__(self, x, y, poly_regression_function=CubicPolyRegFunction()):

        self.f = poly_regression_function
        self.x = x
        self.X = self.f.get_X(x)
        self.y = y
        model = sm.OLS(y, self.X)
        self.fitted = model.fit()

        #print(self.fitted.summary())

    def get_predicted_y(self, x_pred):

        X_pred = self.f.get_X(x_pred)
        return self.fitted.predict(X_pred)

    def get_predicted_y_CI(self, x_pred):

        # http://www2.stat.duke.edu/~tjl13/s101/slides/unit6lec3H.pdf
        y_hat = self.fitted.predict(self.X)     # predicted y at X
        y_err = self.y - y_hat                  # residuals
        mean_x = self.x.mean()             # mean of x
        n = len(self.X)                         # number of observations
        dof = n - self.fitted.df_model - 1      # degrees of freedom
        t = stats.t.ppf(1 - 0.025, df=dof)      # t-statistics
        s_err = np.sum(np.power(y_err, 2))      # sum of squared error
        conf = t * np.sqrt((s_err / (n - 2)) * (1.0 / n + (np.power((x_pred - mean_x), 2) /
                                                           ((np.sum(np.power(x_pred, 2))) - n * (
                                                               np.power(mean_x, 2))))))
        y_pred = self.get_predicted_y(x_pred)
        upper = y_pred + abs(conf)
        lower = y_pred - abs(conf)

        return lower, upper

    def get_predicted_y_PI(self, x):
        X_pred = self.f.get_X(x)
        sdev, lower, upper = wls_prediction_std(self.fitted, exog=X_pred, alpha=0.05)
        return lower, upper
