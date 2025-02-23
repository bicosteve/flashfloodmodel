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
