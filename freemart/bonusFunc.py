import statistics as stats
import numpy as np

from .models import User, Product


def removeOutliers(list):
    cleanedList = sorted([int(x) for x in list])
    try:
        upper_q = np.percentile(cleanedList, 75)
        lower_q = np.percentile(cleanedList, 25)
        iqr = (upper_q - lower_q) * 3.5
        q_set = (lower_q - iqr, upper_q + iqr)
        resultList = []
        for price in cleanedList:
            if price >= q_set[0] and price <= q_set[1]:
                resultList.append(price)
        return resultList
    except IndexError:
        return []

def calcSaleBonus(user):
    print(user.sale_count)
    if user.sale_count <= 7:
        totalPrice = 0
        productCount = 0
        priceAvg = 0
        saleBonus = 0
        items = Product.query.filter(Product.listed==True, Product.username != user.username).all()
        prices = [item.price for item in items]
        try:
            priceAvg = stats.mean(removeOutliers(prices))
            saleBonus = round((priceAvg/3), 2)
        except stats.StatisticsError:
            pass
        return float(saleBonus)
    return 0


def calcQuizBonus(user):
    saleBonus = calcSaleBonus(user)
    quizBonus = round((priceAvg/3), 2)
    return quizBonus
