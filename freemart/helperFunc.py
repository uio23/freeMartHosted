import numpy as np

def isFloat(variable: str) -> bool:
    '''
    Check if a string holds float value
    '''

    try:
        float(variable)
        return True
    except ValueError:
        return False


def removeOutliers(numList: list) -> list[int]:
    '''
    Clean a numerical list from extream outlier values\n
    (iqr * 3.5)
    '''

    cleanedList = []

    try:
        processedList = sorted([float(x) for x in numList])
    except ValueError:
        raise ValueError('List must hold numerical values')

    try:
        upper_q = np.percentile(processedList, 75)
        lower_q = np.percentile(processedList, 25)
    except IndexError:
        raise IndexError('Cannot remove outliers from an empty list')

    iqr = (upper_q - lower_q) * 3.5
    q_set = (lower_q - iqr, upper_q + iqr)
    for price in processedList:
        if price >= q_set[0] and price <= q_set[1]:
            cleanedList.append(price)
    return cleanedList
