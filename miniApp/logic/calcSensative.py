import json
import math

import eel

from logic.calcInitial import dictionary
from logic.calcNoise import convert
from logic.calcPhoto import text


def calcSensative(id):
    for txt in text['info']:
        if (int(txt['id']) == id and ((txt['type'] == "ФЭУ") or (txt['type'] == "Фотодиод"))):
            Sva = convert(txt, 'Sva')
            if (txt['Sva-units'] == "мА/лм"):

                Sea = float(Sva) / 1000 * 16.6  # сначала перевод в Амперы
                print(Sea, (txt['Sva-units']), "!!!")  # предупреждение
                eel.consoleLog([f'{id}: Sea = {Sea} {txt["Sva-units"]}'],'requer' )
            else:
                Sea = float((Sva))
            return float(Sea)
        if (float(txt['id']) == id and (txt['type'] == "Фоторезистор")):
            if (txt['Sva'] != "-"):
                Sva = convert(txt, 'Sva')
                Sea = float(Sva)
            else:
                Icommon = convert(txt, 'Icommon') * math.pow(10,-6)
                It = convert(txt, 'It') * math.pow(10,-6)
                print('Sea')
                print(Icommon,It,float(txt['E']),float(dictionary['D'][0]))

                if (float(Icommon) == float(It)): Icommon = float(Icommon) + 0.1
                Sea = (float(Icommon) - float(It)) / (
                            (float(txt['E'])) * (math.pi * math.pow(float(dictionary['D'][0]) / 2, 2)))
                Sea= Sea* 16.6
            return float(Sea)


def calcSeacht(k1, k2, Sea):
    print('SeaSea')
    print(k1, k2, Sea)
    return float(Sea) * (float(k1) / float(k2))


def calcMaxSensative(k, Sea):
    print("Sea = ", Sea, ";k= ", k)

    return float(Sea) / float(k)


def SpectralSensitivityFPUToLaserRadiation(id, Smax):
    arrX = []
    arrY = []
    for txt in text['info']:
        if int(txt['id']) == id:
            arrX = json.loads(txt['arrayX'])
            arrY = json.loads(txt['arrayY'])
    print(arrX)
    print("lam")
    print(dictionary['lam'][0] * math.pow(10, 9))
    Slaz = 0.55
    for x in range(len(arrX)):
        if x != 0:
            print(id,round(arrX[x - 1], 0),round(dictionary['lam'][0] * math.pow(10, 9), 0),round(arrX[x], 0))
            if round(arrX[x - 1], 0) <= round(dictionary['lam'][0] * math.pow(10, 9), 0) \
                    and round(arrX[x], 0) >= round(dictionary['lam'][0] * math.pow(10, 9), 0):
                Slaz = arrY[x]
                print('выбрал',arrY[x])

        # print("=")
        # print(round(arrX[x], 0), round(dictionary['lam'][0]*math.pow(10,9), 0) )

    eel.consoleLog([f'{id}: Slaz = {Slaz}'], 'txt')
    S = Smax * Slaz
    print('S', S)
    return S
