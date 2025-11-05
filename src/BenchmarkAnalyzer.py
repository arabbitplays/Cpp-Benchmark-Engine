import statistics

def median(values):
    return statistics.median(values)

def medianAbsolutDeviation(values, median):
    deviations = [abs(x - median) for x in values]
    return statistics.median(deviations)

def getAnalytics(values):
    med = median(values)
    mad = medianAbsolutDeviation(values, med)
    return med, mad
