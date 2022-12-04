import json
import math

from mpmath import mpf
import scipy.constants as constant

from logic.calcInitial import dictionary
from logic.calcPhoto import text


def calcFeuNoise(id, Sa, Sacht):
    for txt in text['info']:
        if (int(txt['id']) == id and (txt['type'] == "ФЭУ")):

            Svfk = convert(txt, 'Svfk')
            if (txt['Svfk-units'] == "мА/лм"):
                Svfk = float(Svfk) / 1000 * 16.6  # с

            It = convert(txt, 'It') * math.pow(10,-6)


            Iout = float(It)  + float(dictionary['Fefpr'][0]) * Sacht
            # тут еще проверить единицы измерения
            M = Sa / Svfk
            sqIdr = 2 * constant.e * float(Iout) * M * 2.5 * float(dictionary['df'][0])
            print("!!!-!")
            print(constant.e,float(It) )
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
    elif (txt[index]!="-"):
        It = float(txt[index])

    return It


def getSq(txt, index):
    if 'x' in txt[index]:
        a = float(txt[index].split('x')[0])
        b = float(txt[index].split('x')[1])
        Sq = a * math.pow(10, -3) * b * math.pow(10, -3)  # площадь в метрах
    else:
        Sq = (float(txt[index]) * math.pow(10, -3)) ** 2 * constant.pi  # площадь в метрах

    return Sq


def calcRadNoise(id, Sacht):
    print("k", constant.k)
    print(dictionary['Tf'][0],float(dictionary['Fefpr'][0]),Sacht ** 2)
    Irad = 8 * constant.k * dictionary['Tf'][0] * float(dictionary['Fefpr'][0]) * (Sacht ** 2) * float(
        dictionary['df'][0])
    return Irad


# проверить
def calcDiodNoise(id, Sacht):
    for txt in text['info']:
        if (int(txt['id']) == id and (txt['type'] == "Фотодиод")):

            It = convert(txt, 'It')* math.pow(10,-6)
            # Svfk = convert(txt, 'Svfk')
            Iout = float(It) * Sacht * float(dictionary['Fefpr'][0])
            sqIdr = 2 * constant.e * float(Iout) * float(dictionary['df'][0])

            print(sqIdr, "!!!sqIdr")
            return sqIdr


def calcTemNoise(id, M):
    for txt in text['info']:
        if (int(txt['id']) == id):



            print("Cn = 20пФ")
            print("(B+1 =2.5)")
            It = convert(txt, 'It') * math.pow(10,-6)
            RnTop = 1 / (2 * constant.pi * 20 * math.pow(10, -12) * dictionary["fTop"][0])
            RnBottom = 0.005 / (It * M * 2.5)
            print("Rn", RnTop, RnBottom)
            if ((0.8 * RnTop) > RnBottom):
                print("принебрегаем Rn")  # предупреждение
                sqITem = 4 * constant.k * float(
                    dictionary['df'][0]) * dictionary['Tf'][0]  # !подставил Тф, в методичке просто Т
            else:
                sqITem = (4 * constant.k * float(
                    dictionary['df'][0]) * dictionary['Tf'][0]) / RnBottom  # !подставил Тф, в методичке просто Т
            return sqITem


def calcDiodTemNoise(id):
    for txt in text['info']:
        if (int(txt['id']) == id):
            Rbase = 1000;
            Tk = 300;
            print('Rbase = ', Rbase, "Om\n", 'Tk = ', Tk)
            sqITem = (4 * constant.k * float(
                dictionary['df'][0]) * Tk) / Rbase
            return sqITem


def calcResistTemNoise(id):
    for txt in text['info']:
        if (int(txt['id']) == id):
            Tk = 300;
            Rt = convert(txt, 'Rt') * math.pow(10,6) #проверить потом нужна ли степень мега
            print('Tk = ', Tk)
            sqITem = (4 * constant.k * float(
                dictionary['df'][0]) * Tk) / Rt
            return sqITem


def calcCurrentNoise(id, Fefpr, Seacht):
    for txt in text['info']:
        if (int(txt['id']) == id):
            B = math.pow(10, -11)
            print("B = ", B)

            print("Iout", txt['It'], Fefpr, Seacht)
            Iout = (float(txt['It']) * math.pow(10, -6) + (float(Fefpr) * float(Seacht)))

            sqIcur = (B * (Iout ** 2) * float(
                dictionary['df'][0])) / float( dictionary['fTop'][0])
            return sqIcur


def cakcGenNoise(id, Fefpr, Seacht):
    for txt in text['info']:
        if (int(txt['id']) == id):
            mu = math.pow(10, -7)  # в м
            S = getSq(txt, 'Afcha')
            print('!Внимание Мю берется очень приблизительно: ', mu , 'мˆ2/(В*с)')
            G = txt['tc'] * (txt['Ur'] * mu) / (S ** 2)
            Iout = (txt['It'] * math.pow(10, -6) + Fefpr * Seacht)
            buffer = math.sqrt(1 + (2 * constant.pi * txt['tc'] * dictionary['dFtop'][0]) ** 2)
            buffer = 1 / buffer
            sqIgen = 4 * constant.e * Iout * G * buffer
            return sqIgen


def getSum(a, b, c=0, d=0, e=0):
    print("sum")
    print(a,b,c,d,e)
    return float(a) + float(b) + float(c) + float(d) + float(e)
