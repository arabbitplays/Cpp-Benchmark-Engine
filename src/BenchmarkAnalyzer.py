import statistics

def calculateMedian(values):
    return statistics.median(values)

def calculateMedianAbsolutDeviation(values, median):
    deviations = [abs(x - median) for x in values]
    return statistics.median(deviations)

def getAnalytics(values):
    med = calculateMedian(values)
    mad = calculateMedianAbsolutDeviation(values, med)
    return med, mad
