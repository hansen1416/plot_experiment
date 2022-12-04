import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


figsizes = np.array([[i*i] for i in range(1, 16)])
marksizes = [0.5, 2, 4.2, 8, 12, 18, 24, 32, 40, 50, 60, 72, 84, 96, 110]


def plot_result(X, y, y_pred, poly_reg, lin_reg, degree):

    X_grid = np.arange(min(X), max(X), 0.1)
    X_grid = X_grid.reshape((len(X_grid), 1))

    plt.scatter(X, y, color='red')
    plt.scatter(X, y_pred, color='green')

    plt.plot(X_grid, lin_reg.predict(
        poly_reg.fit_transform(X_grid)), color='black')

    plt.title('Polynomial Regression')
    plt.xlabel('Figsize')
    plt.ylabel('Mark size')

    plt.show()

    plt.savefig(os.path.join('regression_result', 'result_degree_{}.jpg'.format(degree)),
                dpi=200, format='jpg')


if __name__ == "__main__":

    degree = 3

    poly_reg = PolynomialFeatures(degree=degree)
    X_poly = poly_reg.fit_transform(figsizes)

    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, marksizes)

    y_pred = lin_reg.predict(X_poly)

    plot_result(figsizes, marksizes, y_pred, poly_reg, lin_reg, degree)

    grid2D = {
        "j0": 1751622.5000000084,
        "k0": 5947162.5000000652,
        "numJ": 273,
        "numK": 189,
        "deltaJ": 5.0,
        "deltaK": 5.0
    }

    x_test = poly_reg.fit_transform(np.array([[grid2D['numJ']/i * grid2D['numK']/i]
                                              for i in [5, 10, 20]]))

    y_test_pred = lin_reg.predict(x_test)

    print(y_test_pred)
    # [-5380.83891977   188.51132623    64.24455428]
