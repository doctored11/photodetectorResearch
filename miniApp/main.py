import eel
from mpmath import mpf
# from numpy.distutils.fcompiler import none

from logic.calcInitial import dictionary
from logic.calcPhoto import text
from logic.unifier import mathStart

eel.init("web")
# ________________________
# dictionary['df'][0] = 'none'
# print(dictionary['df'][0] == 'none', dictionary['df'][0], 'none')
#
# z = 2
# eel.getFromPython(z)
jsInputArray = []

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


# _________________________

eel.start("index.html", size=(1100, 600), cmdline_args=['-–disable-plugins', ' -–ash-enable-night-light', '-–start-maximized'])
