import json
import math

from mpmath import mpf
import scipy.constants as constant

from logic.calcInitial import dictionary
from logic.calcPhoto import text


def calcFeuNoise(id, Sa, Sacht):
    for txt in text['info']:
        if (int(txt['id']) == id and (txt['type'] == "ФЭУ")):
            It = convert(txt, 'It')
            Svfk = convert(txt, 'Svfk')

            Iout = float(It) * Sacht * float(dictionary['Fefpr'][0])
            # тут еще проверить единицы измерения
            M = Sa / Svfk
            sqIdr = 2 * constant.e * float(Iout) * M * 2.5 * float(dictionary['df'][0])
            print("!!!-!")
            print(float(It), Sacht, float(dictionary['Fefpr'][0]))
            print(M, "M")  # в консоль
            print(M, Sa, Svfk)

            print(sqIdr, "!!!sqIdr")
            return [sqIdr, M]


def convert(txt, index):
    if '|' in txt[index]:
        It = float(txt[index].split('|')[0])
        ten = int(txt[index].split('|')[1])
        deg = int(txt[index].split('|')[2])
        It = float(It) * math.pow(ten, deg)
    else:
        It = mpf(txt[index])

    return It


def calcRadNoise(id, Sacht):
    print("k", constant.k)
    Irad = 8 * constant.k * dictionary['Tf'][0] * float(dictionary['Fefpr'][0]) * (Sacht ** 2) * float(
        dictionary['df'][0])
    return Irad


# проверить
def calcDiodNoise(id, Sacht):
    for txt in text['info']:
        if (int(txt['id']) == id and (txt['type'] == "ФЭУ")):
            It = convert(txt, 'It')
            Svfk = convert(txt, 'Svfk')
            Iout = float(It) * Sacht * float(dictionary['Fefpr'][0])
            sqIdr = 2 * constant.e * float(Iout) * float(dictionary['df'][0])

            print(sqIdr, "!!!sqIdr")
            return sqIdr


def calcTemNoise(id, M):
    for txt in text['info']:
        if (int(txt['id']) == id):
            print("Cn = 20пФ")
            print("(B+1 =2.5)")
            It = convert(txt, 'It')
            RnTop = 1 / (2 * constant.pi * 20 * math.pow(10, -12) * dictionary["fTop"][0])
            RnBottom = 0.005 / (It * M * 2.5)
            print("Rn", RnTop, RnBottom)
            if ((0.8 * RnTop) > RnBottom):
                print("принебрегаем Rn")  # предупреждение
                sqITem = 4 * constant.k * float(
                    dictionary['df'][0]) * dictionary['Tf'][0] #!подставил Тф, в методичке просто Т
            else:
                sqITem = (4 * constant.k * float(
                    dictionary['df'][0]) * dictionary['Tf'][0]  ) / RnBottom #!подставил Тф, в методичке просто Т
            return sqITem