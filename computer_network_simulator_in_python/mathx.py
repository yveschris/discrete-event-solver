import numpy as np

def calc_closest_factors(c: int):

    if c // 1 != c:
        raise TypeError("c must be an integer.")

    a, b, i = 1, c, 0
    while a < b:
        i += 1
        if c % i == 0:
            a = i
            b = c // a

    return [b, a]

def issymmetric(matrix):
    return np.allclose(matrix, matrix.T)