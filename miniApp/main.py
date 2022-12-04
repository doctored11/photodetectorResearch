import eel
from mpmath import mpf
# from numpy.distutils.fcompiler import none

from logic.calcInitial import dictionary, D
from logic.calcPhoto import text
from logic.calcPhotoDerector import thrioCalc
# from logic.unifier import mathStart
from logic.mainCalc import calculationOfGeneralParameters
from logic.delit import  dellAll
eel.init("web")

# ________________________
# dictionary['df'][0] = 'none'
# print(dictionary['df'][0] == 'none', dictionary['df'][0], 'none')
#
# z = 2
# eel.getFromPython(z)
jsInputArray = []


# print("1", D['distrX1'], D['distrX2'], D['distrY1'], D['distrY2'])


def mathStart():
    # print(dictionary)
    buf = calculationOfGeneralParameters()
    # return buf

    # D['distrY1'] = buf[0]
    # D['distrX1'] = buf[1]
    # D['distrY2'] = buf[2]
    # D['distrX2'] = buf[3]
    # print("_2", D['distrX1'], D['distrX2'], D['distrY1'], D['distrY2'])


@eel.expose
def callJson():
    eel.getJson(text)


@eel.expose
def callFromJstoPy(x):
    jsInputArray = x
    for i in range(0, len(jsInputArray)):
        if ((list(jsInputArray[i].values())[1]) != ''):
            dictionary[list(jsInputArray[i].values())[0]][0] = mpf((list(jsInputArray[i].values())[1]))

        else:
            dictionary[list(jsInputArray[i].values())[0]][0] = 'none'


    mathStart()
    # print("2.3", D['distrX1'], D['distrX2'], D['distrY1'], D['distrY2'])


@eel.expose
def getArray3toCalc(arr):
    # print("2.5", D['distrX1'], D['distrX2'], D['distrY1'], D['distrY2'])
    dellAll()
    thrioCalc(arr, D['distrX1'], D['distrX2'], D['distrY1'], D['distrY2'])


# _________________________


eel.start("index.html", size=(1100, 600),
          cmdline_args=['-–disable-plugins', ' -–ash-enable-night-light', '-–start-maximized'])
