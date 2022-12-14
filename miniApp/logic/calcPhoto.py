import json
import math
from pprint import pprint
import collections

import eel
import numpy as np

from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline

eel.init("web")

from logic.calcInitial import dictionary

# minXInput = 0     # нм - макс и мин значения х в распознаваемом графике --?возможно остаток от старой программы
# maxXInput = 1000

with open('data/json-data/base.json', 'r', encoding='utf8') as file:
    text = json.load(file)


# -!!!!!!!!
def printGraphVetector(checkArray, style):  # для отображения 1график =1 холст
    for txt in text['info']:
        if int(txt['id']) in checkArray:

            id = txt['id']
            plt.clf();

            plt.plot(json.loads(txt['arrayX']), json.loads(txt['arrayY']), style, label=txt['name_'])
            plt.legend(loc="upper left")
            plt.savefig(f'web/sourse/graphPhotoSolo{id}.png')
            buf = f'graphPhotoSolo{id}.png'
            eel.getGraph(buf, 'graph-img', id)
            plt.clf();


#             нужно будет сохранять с привязкой к id в имени


def square(arrx, arry):
    S = 0
    for step in range(len(arrx)):
        if (step >= 1):
            S += ((arry[step - 1] + arry[step]) / 2) * ((arrx[step] - arrx[step - 1]) * math.pow(10,
                                                                                                 6))  # 10 в 6 для перевода из м в мк - Почему не в СИ? - вопрос)
    return S


def listtodict(resultList, dic):
    dic = dict(resultList)

    return dic


def multiplyGraph(id, arrX1, arrY1, view, labelName='-_-', style='--b'):
    for txt in text['info']:

        if (int(txt['id']) == id):



            txtX = [i * math.pow(10, -9) for i in json.loads(txt['arrayX'])]



            txtY = json.loads(txt['arrayY'])


            if (len(arrX1) > len(txtX)):

                shortLengthTxt = len(txtX)
                shortLengthArr = len(arrX1)

                for x in range(len(txtX), len(arrX1)):
                    txtX.append(txtX[x - 1])

                while len(txtY) < len(txtX):
                    txtY.append(0)


            else:
                shortLengthTxt = len(txtX)
                shortLengthArr = len(arrX1)

                for x in range(len(arrX1), len(txtX)):
                    arrX1.append(arrX1[x - 1])

                while len(arrY1) < len(arrX1):
                    arrY1.append(0)



            multiplyX1 = np.array(arrX1)
            multiplyY1 = np.array(arrY1)
            multiplyX2 = np.array(txtX)
            multiplyY2 = np.array(txtY)
            if view == True:
                plt.clf()
                buff = 'φ' + labelName
                plt.plot(txtX, txtY, '--g', label='Sфпу')
                maxX = txtX[len(txtX) - 1]

                bufArrX1 = []
                for i in arrX1:
                    if i > 1.6 * maxX: break  # магическая цифра - масштаб ( 1- образать графики ровно по приемнику)
                    bufArrX1.append(i)
                bufArrY1 = multiplyY1[0:len(bufArrX1)]

                plt.plot(bufArrX1, bufArrY1, style, label=buff)  # !!!!

            xy1 = dict(zip(multiplyX1, multiplyY1))
            xy2 = dict(zip(multiplyX2, multiplyY2))
            multipluResultX = []
            multipluResultY = []

            for x1 in range(shortLengthArr):
                for x2 in range(shortLengthTxt):
                    if (round(multiplyX1[x1], 9) == round(multiplyX2[x2],
                                                          9)):  # внимание практически волшебная девятка ( тепень из нм в м)
                        multipluResultX.append(multiplyX1[x1])
                        multipluResultY.append(multiplyY1[x1] * multiplyY2[x2])
            if view == True:
                plt.plot(multipluResultX, multipluResultY, '-', color='orange', label='S*φ')
                plt.legend(loc="upper left")
                plt.savefig(f'web/sourse/graphSum{id}{style}.png')
                buf = f'graphSum{id}{style}.png'
                eel.getMultiplyGraph(buf, 'graph-img', id)


            Sq = square(multipluResultX, multipluResultY)

            plt.show()

            getArrX = multipluResultX
            getArrY = multipluResultY
            return [Sq, getArrX, getArrY]
