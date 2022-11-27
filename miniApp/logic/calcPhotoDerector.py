from logic.calcNoise import calcFeuNoise, calcRadNoise, calcTemNoise, calcDiodNoise
from logic.calcPhoto import multiplyGraph, text
from logic.calcSensative import SpectralSensitivityFPUToLaserRadiation, calcMaxSensative, calcSeacht, calcSensative


def calcPhotoDetector(id, distributionX1, distributionX2, distributionY1, distributionY2):

    kacht = multiplyGraph(id, distributionX1, distributionY1)[0]
    ka = multiplyGraph(id, distributionX2, distributionY2)[0]
    if (kacht <=0 or ka <=0):
        print("приемник не подходит по спектру")
        return

    Sea = calcSensative(id)
    Seacht = calcSeacht(kacht, ka, Sea)
    Smax = calcMaxSensative(ka, Sea)
    Selaz = SpectralSensitivityFPUToLaserRadiation(1, Smax)
    type = "none"
    for txt in text['info']:
        if (int(txt['id']) == id):
            type = (txt['type'])
    # шумы  ФЭУ
    if ( type == "ФЭУ"):
        sqIdr = calcFeuNoise(id, Sea, Seacht)[0]
        sqIrad = calcRadNoise(id, Seacht)
        sqITem = calcTemNoise(id, calcFeuNoise(id, Sea, Seacht)[1])
        # для теплового шума нужна Rн

    # шумы для диодов
    if (type == "Фотодиод"):
        sqIdr = calcDiodNoise(id, Seacht)
        sqIrad = calcRadNoise(id, Seacht)
        # для теплового шума нужна Rб - брать 1кОм

    # Шумы для резисторов
    if (type == "Фоторезистор"):
        sqIrad = calcRadNoise(id, Seacht)
        # и прочее

    print("id",id)
    print("ka", ka)
    print("kacht", kacht)
    print(kacht, ka, Sea)
    print(Seacht, "Seacht")
    print(Smax, "SeMAx")
    print(Selaz, "Selax")
    print("----")
    print(sqIdr,"sqIdr")
    print("Irad", sqIrad)
    print("sqITem", sqITem)
