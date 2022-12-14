import eel
import numpy
from mpmath import mpf
# from numpy.distutils.fcompiler import none

from logic.calcInitial import dictionary, D
from logic.calcPhoto import text, listtodict
from logic.calcPhotoDerector import thrioCalc, autoCalc
# from logic.unifier import mathStart
from logic.mainCalc import calculationOfGeneralParameters
from logic.delit import dellAll
import itertools
eel.init("web")

# ________________________

jsInputArray = []


def mathStart():
    # print(dictionary)
    buf = calculationOfGeneralParameters()



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



@eel.expose
def getArray3toCalc(arr):
    dellAll()
    thrioCalc(arr, D['distrX1'], D['distrX2'], D['distrY1'], D['distrY2'])


@eel.expose
def autoCalcAll():
    di = {}
    dellAll()
    resultArr=[]
    resultArr = autoCalc(D['distrX1'], D['distrX2'], D['distrY1'], D['distrY2'])
    di =  listtodict(resultArr, di)
    di = {int(k): float(v) for k, v in di.items()}
    buffdict  = dict(sorted(di.items(), key=lambda item: item[1]))
    shortDi = {}
    if (len(buffdict) > 10):
        for i in range(10):

            shortDi = dict(itertools.islice(buffdict.items(), 10))
    else:
        shortDi = buffdict

    finishArr =['автоподбор, id:',]
    print(finishArr)
    for i in shortDi.keys():
        buff = 'id: '+ str(i)
        finishArr.append(buff)

    eel.clearAll()
    # eel.consoleLog({'автоподбор, id:'}, 'succes')
    eel.consoleLog(finishArr,'succes')


# _________________________


eel.start("index.html", size=(1100, 600),
          cmdline_args=['-–disable-plugins', ' -–ash-enable-night-light', '-–start-maximized'])
