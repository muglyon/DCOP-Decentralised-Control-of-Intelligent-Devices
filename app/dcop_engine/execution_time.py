CONFIDENCE_PERCENT = 1.95

total = []
for_dpop = []


def average(data):
    return sum(data) / len(data)


def divergence(data):
    # Moyenne des carrés des écarts de la moyenne
    avg = average(data)
    return average([(x - avg)**2 for x in data])


def standard_deviation(data):
    # Racine carré de la variance
    return divergence(data)**0.5


def confidence_interval(data):
    avg = average(data)
    step = (CONFIDENCE_PERCENT * (standard_deviation(data) / (len(data)**0.5)))
    return [avg - step, avg + step]
