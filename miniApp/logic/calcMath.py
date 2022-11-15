import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from mpmath import *
import scipy.constants as constant

numerator = 2 * math.pi * constant.h * math.pow(constant.c, 2)


def PlankLow(T, maxlam, step, arrayX, arrayY, style , heading):
    lamPrev = 2

    # max
    lamMaxACT = 2898 / T * 1000  # м возможно домножить на 1000 над
    # print(lamMaxACT)
    lamMaxACT *= math.pow(10, -9)

    denominatorMax = math.pow(lamMaxACT, 5) * (
            math.pow(math.e,
                     constant.h * constant.c /
                     (lamMaxACT * constant.k * T)
                     ) - 1
    )
    FeMax = numerator / denominatorMax
    # step lam

    while lamPrev < maxlam:
        lam = lamPrev * math.pow(10, -9)  # м

        denominator = math.pow(lam, 5) * (
                mpf(math.e) ** (
                constant.h * constant.c /
                (lam * constant.k * mpf(T))
        ) - 1
        )
        Fe = numerator / denominator
        lamPrev += step
        arrayY.append(Fe / FeMax)
        arrayX.append(lam)

    plt.plot(arrayX, arrayY, style, label=heading)
    plt.legend()
