import math

import eel
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import scipy
from mpmath import *
import scipy.constants as constant

from logic.calcInitial import *
from logic.calcMath import PlankLow
from logic.calcNoise import calcFeuNoise, calcRadNoise, calcDiodNoise, calcTemNoise
from logic.calcPhoto import multiplyGraph, text
from logic.calcPhotoDerector import calcPhotoDetector, autoCalc
from logic.calcSensative import calcSensative, calcSeacht, calcMaxSensative, SpectralSensitivityFPUToLaserRadiation
from logic.delit import dellAll

# from mpmath import mpf, mpc, mp
eel.init("web")

mp.dps = 16  # 16 или 8  - не трогать!

# перевод Си
# из
readyAr = []

def calculationOfGeneralParameters():
    dellAll()
    readyAr = []
    Sin = math.pi * math.pow(dictionary['D'][0] / 2, 2)
    if dictionary['k'][0] == 'none': dictionary['k'][0] = 1
    for key, v in dictionary.items():
        if v[0] != 'none':
            v[0] *= conversion[v[1]]
    # print(dictionary)
    readyAr.append('в СИ')
    # 1)
    if (dictionary['fBottom'][0] == 'none' and dictionary['fTop'][0] != 'none' and dictionary['df'][0] == 'none'):
        dictionary['df'][0] = dictionary['fTop'][0]
        bufExcept = []
        bufExcept.append('df = fTop (упрощение)')
        eel.consoleLog(bufExcept, 'requer');
    if dictionary['fBottom'][0] == 'none' and dictionary['fTop'][0] == 'none' and dictionary['df'][0] == 'none':
        if dictionary['tImp'][0] == 'none':
            readyAr.append("мало входных данных f ")
        else:
            dictionary['fTop'][0] = 1 / dictionary['tImp'][0]

    if dictionary['fBottom'][0] == 'none' and dictionary['df'][0] == 'none':
        dictionary['df'][0] = dictionary['fTop'][0]

    if dictionary['df'][0] == 'none':
        dictionary['df'][0] = dictionary['fTop'][0] - dictionary['fBottom'][0]  # \кГц

    # print(dictionary['df'][0])
    readyAr.append('1) Полоса частот:' + str(dictionary['df'][0]))

    # 2)
    if dictionary['Fel'][0] == 'none':
        if dictionary['Wel'][0] == 'none' or dictionary['tImp'][0] == 'none':
            print("error step 2 - мало входных данных")
        else:
            dictionary['Fel'][0] = dictionary['Wel'][0] / dictionary['tImp'][
                0]  # ! - возможна проблема в разрядах (кГц)
    readyAr.append('2) Поток излучения: ' + str(dictionary['Fel'][0]))

    # 3)

    if dictionary['Fefpr'][0] == 'none':

        if dictionary['Rf'][0] == 'none' \
                or dictionary['Fef'][0] == 'none' \
                or dictionary['D'][0] == 'none':
            readyAr.append("error step 3 - мало входных данных")

        else:

            Sin = math.pi * math.pow(dictionary['D'][0] / 2, 2)
            dictionary['Fefpr'][0] = dictionary['Fef'][0] * (
                    Sin /
                    (4 * math.pi * math.pow(dictionary['Rf'][0], 2))) \
                                     * dictionary['k'][0]

    readyAr.append('3) Поток фона на приемнике: ' + str(dictionary['Fefpr'][0]))

    # 4)

    # ! если дано расстояние от приемника до лазера
    if dictionary['Rl'][0] != 'none':
        dictionary['Felpr'][0] = dictionary['Fel'][0] * \
                                 (Sin * math.pow(math.tan(math.degrees(dictionary['dFi'][0])), 2)
                                  / (math.pi * math.pow(dictionary['Rl'][0], 2))) * \
                                 dictionary['k'][0]
        readyAr.append('4) поток от лазерного истчоника излучения на приемнике: ' + str(dictionary['Felpr'][0]))

    # 5) - построить график где lamBuff это длина волны от 1 нм до +-2500 нм а Y  buffer = numerator/ denominator
    plt.clf()

    distributionY1, distributionX1, distributionY2, distributionX2 = [[], [], [], []]
    PlankLow(dictionary['Tf'][0], 20400000 / dictionary['Tf'][0], 20400000 / dictionary['Tf'][0] * math.pow(10, -3),
             distributionX1, distributionY1, "-r", 'Поток Fачт')  # лучше через color="#ff"
    PlankLow(dictionary['Ta'][0], 20400000 / dictionary['Tf'][0], 20400000 / dictionary['Tf'][0] * math.pow(10, -3),
             distributionX2, distributionY2, "--b", 'Поток Fа')

    D['distrY1'] = distributionY1
    D['distrX1'] = distributionX1
    D['distrY2'] = distributionY2
    D['distrX2'] = distributionX2
    plt.xlabel('λ')
    plt.savefig('web/sourse/savedFigure.png')
    eel.getFromPython('savedFigure.png', 'graph-img')

    # getDists(distributionX1, distributionX2, distributionY1,
    #          distributionY2)  # передача графика в main   -_-

    # цифра 1 это id

    # plt.show()
    readyAr.append(
        '5-6) Построены нормированные графики спектральной плотности потока АЧТ и спектральной характеристики источника типа А')
    eel.getResultsStep1(readyAr);

    # автоподсчет ! - по клику на отдельную кнопку 
    # resultList = autoCalc(distributionY1, distributionX1, distributionY2, distributionX2)  # авто подбор
    # print("LIST!: \n", resultList)
    #

    #
    # resultDict = {}
    # streamList = listtodict(resultList, resultDict)
    # streamListSorted = dict(sorted(streamList.items(), key=lambda item: item[1]))
    # print(streamList, "\n", streamListSorted)

    # ___---
    return (distributionY1, distributionX1, distributionY2, distributionX2)
