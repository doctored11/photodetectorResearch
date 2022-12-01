import math

from logic.calcInitial import dictionary
from logic.calcNoise import calcFeuNoise, calcRadNoise, calcTemNoise, calcDiodNoise, calcDiodTemNoise, \
    calcResistTemNoise, calcCurrentNoise, getSum
from logic.calcPhoto import multiplyGraph, text
from logic.calcSensative import SpectralSensitivityFPUToLaserRadiation, calcMaxSensative, calcSeacht, calcSensative


def calcPhotoDetector(id, distributionX1, distributionX2, distributionY1, distributionY2, view=True):
    kacht = multiplyGraph(id, distributionX1, distributionY1, view)[0]
    ka = multiplyGraph(id, distributionX2, distributionY2, view)[0]
    if (kacht <= 0 or ka <= 0):
        print("приемник не подходит по спектру")
        return

    Sea = calcSensative(id)
    Seacht = calcSeacht(kacht, ka, Sea)
    Smax = calcMaxSensative(ka, Sea)
    Selaz = SpectralSensitivityFPUToLaserRadiation(1, Smax)
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
        Sum = getSum(sqIdr, sqIrad, sqITem)

    # шумы для диодов
    if (type == "Фотодиод"):
        sqIdr = calcDiodNoise(id, Seacht)
        sqIrad = calcRadNoise(id, Seacht)
        sqITem = calcDiodTemNoise(id)
        # print("to Sum")
        # print(sqIrad, sqITem, sqIdr,id,Seacht)
        Sum = getSum(sqIrad, sqITem, sqIdr)
        # для теплового шума нужна Rб - брать 1кОм

    # Шумы для резисторов
    if (type == "Фоторезистор"):
        sqIrad = calcRadNoise(id, Seacht)
        sqITem = calcResistTemNoise(id)
        sqIcur = calcCurrentNoise(id, dictionary['Fefpr'][0], Seacht)
        sqIgen = calcCurrentNoise(id, dictionary['Fefpr'][0], Seacht)
        Sum = getSum(sqIrad, sqITem, sqIcur, sqIgen)
        # и прочее

    Fpr = math.sqrt(Sum) / Selaz  # итоговая штука ( пороговый поток)

    # print("ka", ka)
    # print("kacht", kacht)
    # print(kacht, ka, Sea)
    # print(Seacht, "Seacht")
    # print(Smax, "SeMAx")
    # print(Selaz, "Selax")
    # print("----")
    # print(sqIdr, "sqIdr")
    # print("Irad", sqIrad)
    # print("sqITem", sqITem)
    print("----")
    print("id", id)
    print("Fpr: ", Fpr)
    print("----")
    return (id, Fpr)


def autoCalc(distributionY1, distributionX1, distributionY2, distributionX2):
    resultArr = []

    for i in range(1, len(text['info'])):
        dLam = text['info'][i - 1]['d-lam']
        minL = float(dLam.split('-')[0]) * math.pow(10, -6)
        maxL = float(dLam.split('-')[1]) * math.pow(10, -6)
        print(i, maxL, dictionary['lam'][0])
        if (dictionary['lam'][0] > minL and dictionary['lam'][0] < maxL):
            print('id - ', i, dictionary['lam'][0])
            result = calcPhotoDetector(i, distributionX1, distributionX2, distributionY1,
                                       distributionY2, False)  # тут только с 1 (0 не работает - см id в Json
            if (result != None):
                resultArr.append(result)
    return resultArr


def thrioCalc(arr, distrX1, distrX2, distrY1, distrY2):
    for i in range(0, len(arr)):
        dLam = text['info'][arr[i] - 1]['d-lam']
        minL = float(dLam.split('-')[0]) * math.pow(10, -6)
        maxL = float(dLam.split('-')[1]) * math.pow(10, -6)
        print('++++\n-----\n+++++\n_________\n---------')
        # print(arr[i], maxL, dictionary['lam'][0], dLam)
        # print("\n3 \n", distrX1, distrX2, distrY1, distrY2)
        if (dictionary['lam'][0] > minL and dictionary['lam'][0] < maxL):
            result = calcPhotoDetector(arr[i], distrX1, distrX2, distrY1, distrY2, True)
        else: print("не подходит по спектру")
