import json
import math
from pprint import pprint
import collections
import numpy as np

from matplotlib import pyplot as plt

from logic.calcInitial import dictionary

minXInput = 0  # нм - макс и мин значения х в распознаваемом графике
maxXInput = 1000

with open('data/json-data/base.json', 'r', encoding='utf8') as file:
    text = json.load(file)



def printGraphВetector(checkArray, style):  # для отображения 1график =1 холст
    for txt in text['info']:
        if (txt['type'] == "ФЭУ") and int(txt['id']) in checkArray:
            # print(txt['name_'])

            # print(json.loads(txt['arrayX']))
            plt.plot(json.loads(txt['arrayX']), json.loads(txt['arrayY']), style)
            plt.show()


#             нужно будет сохранять с привязкой к id в имени

checkArray = [0, 1, 2]  # id тех что проверяем
printGraphВetector(checkArray, '-g')
def square(arrx,arry):
    S=0
    for step in range(len(arrx)):
        if (step>=1):
            S += ((arry[step-1]+ arry[step])/2) * ((arrx[step]-arrx[step-1])*math.pow(10,6)) #10 в 6 для перевода из м в мк - Почему не в СИ? - вопрос)
    return S


def multiplyGraph(id, arrX1, arrY1, view):

    for txt in text['info']:

        if (int(txt['id']) == id):
            print(txt['id'],id,'!!!!!!')
            print(json.loads(txt['arrayX']))
            # print(len(json.loads(txt['arrayX'])))
            txtX = [i * math.pow(10, -9) for i in json.loads(txt['arrayX'])]
            print(txtX)

            print('!-!')
            print(len(arrX1), len(txtX))
            txtY = json.loads(txt['arrayY'])
            if (len(arrX1) > len(txtX)):
                arrX1 = arrX1[:len(txtX)]
                arrY1 = arrY1[:len(txtX)]
            else:
                txtX = txtX[:len(arrX1)]
                txtY = txtY[:len(arrX1)]

            print(len(arrX1), len(txtX))
            print('!--!')

            multiplyX1 = np.array(arrX1)
            multiplyY1 = np.array(arrY1)
            multiplyX2 = np.array(txtX)
            multiplyY2 = np.array(txtY)
            if view == True:
                plt.clf()
                plt.plot(txtX, txtY, '-g')
                plt.plot(arrX1, arrY1, '-b')

            xy1 = dict(zip(multiplyX1, multiplyY1))
            xy2 = dict(zip(multiplyX2, multiplyY2))
            multipluResultX = []
            multipluResultY = []

            for x1 in range(len(multiplyX1)):
                for x2 in range(len(multiplyX2)):
                    if (round(multiplyX1[x1], 9) == round(multiplyX2[x2], 9)):# внимание практически волшебная девятка ( тепень из нм в м)
                        multipluResultX.append(multiplyX1[x1])
                        multipluResultY.append(multiplyY1[x1]*multiplyY2[x2])
            if view == True:
                plt.plot(multipluResultX, multipluResultY, '-r')

            # print(multipluResultX)
            # print(multipluResultY)
            Sq = square(multipluResultX,multipluResultY)
            print("Sq", Sq)
            print('show')
            plt.show()

            getArrX = multipluResultX
            getArrY = multipluResultY
            return [Sq, getArrX, getArrY]
