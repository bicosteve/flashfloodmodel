def CategorizeSlopePosition(data):
    category = 0
    if data == "A":
        category = 0
    elif data == "D":
        category = 1
    elif data == "H":
        category = 2
    elif data == "L":
        category = 3
    elif data == "M":
        category = 4

    return category


def CategorizeSurfaceStoniness(data):
    category = 0
    if data == "A":
        category = 0
    elif data == "C":
        category = 1
    elif data == "D":
        category = 2
    elif data == "F":
        category = 3
    elif data == "M":
        category = 4
    elif data == "N":
        category = 5
    elif data == "V":
        category = 6

    return category


def CategorizeErosionDegree(data):
    category = 0
    if data == "E":
        category = 0
    elif data == "M":
        category = 1
    elif data == "S":
        category = 2
    elif data == "V":
        category = 3
    return category


def CategorizeSensitivityToCapping(data):
    category = 0
    if data == "M":
        category = 0
    elif data == "N":
        category = 1
    elif data == "S":
        category = 2
    elif data == "W":
        category = 3

    return category


def CategorizeLandUseType(data):
    category = 0
    if data == "Agriculture":
        category = 0
    elif data == "Forest":
        category = 1
    elif data == "Urban":
        category = 2
    elif data == "Wetland":
        category = 3

    return category


def CategorizeAffectedArea(data):
    return int(data)
