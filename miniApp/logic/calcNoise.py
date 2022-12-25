import json
import math

import eel
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

            M = Sa / Svfk
            sqIdr = 2 * constant.e * float(Iout) * M * 2.5 * float(dictionary['df'][0])

            eel.consoleLog([f'{id}: M = {M}'],'txt')

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


            return sqIdr


def calcTemNoise(id, M):
    for txt in text['info']:
        if (int(txt['id']) == id):


            eel.consoleLog()
            eel.consoleLog([f'{id} Cn = 20пФ'],'txt')
            eel.consoleLog([f'{id} (B+1 =2.5)'],'txt')
            It = convert(txt, 'It') * math.pow(10,-6)
            RnTop = 1 / (2 * constant.pi * 20 * math.pow(10, -12) * dictionary["fTop"][0])
            RnBottom = 0.005 / (It * M * 2.5)

            if ( RnTop >= RnBottom):

                eel.consoleLog(["принебрегаем sqITem", ("RnTop ="+ str(RnTop) ), (" >= RnBottom ="+ str(RnBottom))], 'requer')

                sqITem = 0;

                # sqITem = 4 * constant.k * float(
                #     dictionary['df'][0]) * dictionary['Tf'][0]  # !подставил Тф, в методичке просто Т
            else:
                eel.consoleLog([("RnTop ="+ str(RnTop)), (" < RnBottom =" + str(RnBottom))], 'requer')
                sqITem = (4 * constant.k * float(
                    dictionary['df'][0]) * dictionary['Tf'][0]) / RnBottom  # !подставил Тф, в методичке просто Т
            return sqITem


def calcDiodTemNoise(id, view = True):
    for txt in text['info']:
        if (int(txt['id']) == id):
            Rbase = 1000;
            Tk = 300;
            if (view):
                eel.consoleLog([f'{id}: Rbase ={Rbase}'], 'txt')
                eel.consoleLog([f'{id}: Tk ={Tk}'], 'txt')
            sqITem = (4 * constant.k * float(
                dictionary['df'][0]) * Tk) / Rbase
            return sqITem


def calcResistTemNoise(id):
    for txt in text['info']:
        if (int(txt['id']) == id):
            Tk = 300;
            Rt = convert(txt, 'Rt') * math.pow(10,6) #проверить потом нужна ли степень мега

            sqITem = (4 * constant.k * float(
                dictionary['df'][0]) * Tk) / Rt
            return sqITem


def calcCurrentNoise(id, Fefpr, Seacht):
    for txt in text['info']:
        if (int(txt['id']) == id):
            B = math.pow(10, -11)



            Iout = (float(txt['It']) * math.pow(10, -6) + (float(Fefpr) * float(Seacht)))

            sqIcur = (B * (Iout ** 2) * float(
                dictionary['df'][0])) / float( dictionary['fTop'][0])
            return sqIcur


def calcGenNoise(id, Fefpr, Seacht):
    for txt in text['info']:
        if (int(txt['id']) == id):
            mu = math.pow(10, -7)  # в м
            S = float(getSq(txt, 'Afcha'))
            eel.consoleLog([f'!Внимание Мю берется очень приблизительно:  {mu} мˆ2/(В*с)'],'requer')
            G = float( txt['tc']) * (float(txt['Ur']) * mu) / (S ** 2)
            Iout = (float(txt['It']) * math.pow(10, -6) + Fefpr * Seacht)
            buffer = math.sqrt(1 + (2 * constant.pi * float( txt['tc']) * float(dictionary['fTop'][0])) ** 2)
            if buffer == 0: buffer =1
            buffer = 1 / buffer
            sqIgen = 4 * constant.e * Iout * G * buffer

            return sqIgen


def getSum(a, b, c=0, d=0, e=0):

    return float(a) + float(b) + float(c) + float(d) + float(e)
