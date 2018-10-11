from scipy import stats
import numpy as np
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


class PolyRegFunction:
    # regression of form: 1 + x + x^2 + x^3 + ...

    def __init__(self, degree=1):
        """
        :param degree: degree of the polynomial function
        """
        if degree < 1:
            raise ValueError('Degree of the polynomial regression function should be greater than 0.')
        self.degree = degree

    def get_X(self, x):
        """
        :param x: (list or np.array) observed x values (x1, x2, x3, ..., xn)
        :return: (matrix) of X = [(1, x1'),
                                  (1, x2'),
                                  (1, x3'),
                                  ...,
                                  (1, xn')]
        """

        if self.degree == 1:
            # for degree 1, we only need to add constant vector 1 to x to get
            # [1, x1]
            # [1, x2] ...
            return sm.add_constant(x)
        else:
            col_x = [x]       # to build [x, x^2, x^3, ...]
            for i in range(2, self.degree+1):
                col_x.append(np.power(x, i))
            # turn [x, x^2, x^3, ...] to X
            X = np.column_stack(col_x)
            return sm.add_constant(X)


class SingleVarRegression:

    def __init__(self, x, y, degree=1):

        self.f = PolyRegFunction(degree)
        self.x = x
        self.X = self.f.get_X(x)
        self.y = y
        model = sm.OLS(self.y, self.X)
        self.fitted = model.fit()

    def get_predicted_y(self, x_pred):
        """ :returns predicted y values at the provided x values """

        X_pred = self.f.get_X(x_pred)
        return self.fitted.predict(X_pred)

    def get_predicted_y_CI(self, x_pred, alpha=0.05):
        """ :returns confidence interval of the predicted y at the provided x values """

        # http://www2.stat.duke.edu/~tjl13/s101/slides/unit6lec3H.pdf
        y_hat = self.fitted.predict(self.X)     # predicted y at X
        y_err = self.y - y_hat                  # residuals
        mean_x = self.x.mean()                  # mean of x
        n = len(self.X)                         # number of observations
        dof = n - self.fitted.df_model - 1      # degrees of freedom
        t = stats.t.ppf(1 - alpha/2, df=dof)      # t-statistics
        s_err = np.sum(np.power(y_err, 2))      # sum of squared error
        conf = t * np.sqrt((s_err / (n - 2)) * (1.0 / n + (np.power((x_pred - mean_x), 2) /
                                                           ((np.sum(np.power(x_pred, 2))) - n * (
                                                               np.power(mean_x, 2))))))
        y_pred = self.get_predicted_y(x_pred)
        upper = y_pred + abs(conf)
        lower = y_pred - abs(conf)

        return lower, upper

    def get_predicted_y_PI(self, x_pred, alpha=0.05):
        """ :returns prediction interval of the y at the provided x values """
        X_pred = self.f.get_X(x_pred)
        sdev, lower, upper = wls_prediction_std(self.fitted, exog=X_pred, alpha=alpha)
        return lower, upper
