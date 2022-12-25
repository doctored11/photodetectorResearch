import math

import eel

from logic.calcInitial import dictionary
from logic.calcNoise import calcFeuNoise, calcRadNoise, calcTemNoise, calcDiodNoise, calcDiodTemNoise, \
    calcResistTemNoise, calcCurrentNoise, getSum, calcGenNoise
from logic.calcPhoto import multiplyGraph, text, printGraphVetector
from logic.calcSensative import SpectralSensitivityFPUToLaserRadiation, calcMaxSensative, calcSeacht, calcSensative


def calcPhotoDetector(id, distributionX1, distributionX2, distributionY1, distributionY2, view=True):
    kacht = multiplyGraph(id, distributionX1, distributionY1, view, 'ачт', '--r')[0]
    ka = multiplyGraph(id, distributionX2, distributionY2, view, 'a', '--b')[0]
    if (kacht <= 0 or ka <= 0):
        print("приемник не подходит по спектру")
        return

    Sea = calcSensative(id,view)
    Seacht = calcSeacht(kacht, ka, Sea)
    Smax = calcMaxSensative(ka, Sea)
    Selaz = SpectralSensitivityFPUToLaserRadiation(id, Smax,view)
    # if ( Selaz ==0 ): Selaz = math.pow(10,-9)
    type = "none"
    for txt in text['info']:
        if (int(txt['id']) == id):
            type = (txt['type'])
    # шумы  ФЭУ
    Sum = 0
    if (type == "ФЭУ"):
        sqIdr = calcFeuNoise(id, Sea, Seacht)[0]
        sqIrad = calcRadNoise(id, Seacht)
        sqITem = calcTemNoise(id, calcFeuNoise(id, Sea, Seacht)[1])
        sqIcur = '-'
        sqIgen = '-'
        Sum = getSum(sqIdr, sqIrad, sqITem)

    # шумы для диодов
    if (type == "Фотодиод"):
        sqIdr = calcDiodNoise(id, Seacht)
        sqIrad = calcRadNoise(id, Seacht)
        sqITem = calcDiodTemNoise(id,view)

        sqIcur = '-'
        sqIgen = '-'
        Sum = getSum(sqIrad, sqITem, sqIdr)
        # для теплового шума нужна Rб - брать 1кОм

    # Шумы для резисторов
    if (type == "Фоторезистор"):
        sqIdr = '-'
        sqIrad = calcRadNoise(id, Seacht)
        sqITem = calcResistTemNoise(id)
        sqIcur = calcCurrentNoise(id, dictionary['Fefpr'][0], Seacht)
        sqIgen = calcGenNoise(id, dictionary['Fefpr'][0], Seacht)
        Sum = getSum(sqIrad, sqITem, sqIcur, sqIgen)


    Fpr = math.sqrt(Sum) / Selaz  # итоговая штука ( пороговый поток)



    resultArr = [
        ("id", str(id)),
        ("ka", str(ka)),
        ("kacht", str(kacht)),
        ("Seacht", str(Seacht)),
        ("SeMAx", str(Smax)),
        ("Selaz", str(Selaz)),
        ("sqIdr", str(sqIdr)),
        ("Irad", str(sqIrad)),
        ("sqITem", str(sqITem)),
        ('sqIcur', str(sqIcur)),
        ('sqIgen', str(sqIgen)),
        ("Fpr", str(Fpr))
    ]


    return (id, resultArr)


def autoCalc(distributionX1, distributionX2, distributionY1, distributionY2):
    resultArr = []

    num = len(text['info'])
    # num =22;
    for i in range(1, num):

        eel.clearAll()
        eel.consoleLog([f'step {i}/{num}'],'txt')

        dLam = text['info'][i - 1]['d-lam']
        minL = float(dLam.split('-')[0]) * math.pow(10, -6)
        maxL = float(dLam.split('-')[1]) * math.pow(10, -6)

        if (dictionary['lam'][0] > minL and dictionary['lam'][0] < maxL):

            try:
                result = calcPhotoDetector(i, distributionX1, distributionX2, distributionY1,
                                           distributionY2, False)[1]  # тут только с 1 (0 не работает - см id в Json
            except TypeError:

                result = None
                eel.consoleLog([f'Что то пошло не так id: {i}'], 'error')

            if (result != None):
                resultArr.append((i, result[len(result) - 1][1]))



    return resultArr


def thrioCalc(arr, distrX1, distrX2, distrY1, distrY2):
    printGraphVetector(arr, '--g')#//--g
    for i in range(0, len(arr)):
        dLam = text['info'][arr[i] - 1]['d-lam']
        minL = float(dLam.split('-')[0]) * math.pow(10, -6)
        maxL = float(dLam.split('-')[1]) * math.pow(10, -6)

        if (dictionary['lam'][0] > minL and dictionary['lam'][0] < maxL):
            try:
                result = calcPhotoDetector(arr[i], distrX1, distrX2, distrY1, distrY2, True)[1]
                eel.getCalcResult(arr[i], result)
            except TypeError:
                eel.consoleLog([f'Что то пошло не так id: {arr[i]}'], 'error')

        else:
            print("не подходит по спектру")
    eel.getUnblock()
