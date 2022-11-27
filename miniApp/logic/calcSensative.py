import json
import math

from logic.calcInitial import dictionary
from logic.calcPhoto import text


def calcSensative(id):
    for txt in text['info']:
        if (int(txt['id']) == id and (txt['type'] == "ФЭУ")):
            if (txt['Sva-units'] == "мА/лм"):
                Sea = int((txt['Sva']))/1000 * 16.6 #сначала перевод в Амперы
                print(Sea, (txt['Sva-units']), "!!!")  # предупреждение
            else:
                Sea = int((txt['Sva']))
            return float(Sea)


def calcSeacht(k1, k2, Sea):
    print(k1,k2,Sea)
    return float(Sea) * ( float(k1) / float(k2))


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
    for x in range(len(arrX)):
        if x != 0:
            if round(arrX[x - 1], 0) < round(dictionary['lam'][0] * math.pow(10, 9), 0) \
                    and round(arrX[x], 0) >= round(dictionary['lam'][0] * math.pow(10, 9), 0):
                Slaz = arrY[x]
        # print("=")
        # print(round(arrX[x], 0), round(dictionary['lam'][0]*math.pow(10,9), 0) )

    print('Slaz', Slaz)
    S = Smax * Slaz
    print('S', S)
    return S
