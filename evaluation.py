import run, helper, sys

# pares input parameters for potential custom ranges
params = helper.parseArguments(sys.argv)

# chosen prime numbers as base seeds
selectedRandomPrimes = [
    982434227,982390301,982449889,982406627,982406809,982400521,982412141,982394291,982430263,982447637,982396931,982430819,982399151,982419479,982412329,982426883,982427539,982401317,982399799,982445341,982425713,982401757,982398419,982443211,982388467,982402781,982388947,982403369,982415297,982450039,982405103,982432883,982426309,982447021,982443331,982412933,982389403,982402697,982391741,982441259,982439413,982427443,982405069,982390567,982439891,982426201,982399441,982440299,982419433,982445587,982418221,982449239,982443589,982402921,982420609,982435007,982410097,982394293,982413319,982391273,982431823,982427987,982450943,982440587,982418243,982415857,982413983,982418873,982415429,982399813,982394737,982398799,982400183,982418209,982409521,982417697,982441637,982415381,982396637,982444417,982436311,982413227,982429909,982421203,982427273,982396003,982431493,982391737,982423543,982389073,982402823,982414061,982429229,982415689,982389613,982407707,982440941,982443733,982409873,982403033
]

# simulation parameters
size = 40
probabilityOfDeath = 0
infectionLengthFrom = 6
infectionLengthTo = 9
individual = '20,20'
rangeFrom = 0
rangeTo = 100

if '-rangeFrom' in params:
    val = int(params['-rangeFrom'])
    if val < 0 or val > 100:
        raise ValueError("Range has to be within 0 <= from < to <= 100.")
    rangeFrom = val

if '-rangeTo' in params:
    val = int(params['-rangeTo'])
    if val < 0 or val > 100 or rangeTo < rangeFrom:
        raise ValueError("Range has to be within 0 <= from < to <= 100.")
    rangeTo = val

# threshold is half the population
threshold = (size * size) / 2

#  prepare csv list with length of selected prime numbers and space for probability and average
csv = []
for i in range(0, len(selectedRandomPrimes)+2):
    csv.append([])

# for each probability in the range, trigger the simulation for each of the prime numbers
for i in range(rangeFrom, rangeTo):
    results = []
    infectionProbability = float(i) / 100

    # set infection probability as header
    csv[0].append(infectionProbability)

    for j in range(0, len(selectedRandomPrimes)):
        result = run.run([
            '-N', str(size),
            '-minDays', str(infectionLengthFrom),
            '-maxDays', str(infectionLengthTo),
            '-L', str(probabilityOfDeath),
            '-S', str(infectionProbability),
            '-seed', str(selectedRandomPrimes[j]),
            '--silent',
            '-x', individual
        ])

        csv[j+2].append(result)
        results.append(result)

    # calculate average of infected individuals and write below header in csv
    infected = sum(results) / len(results)
    csv[1].append(infected)

    # once epidemic is reached, stop
    if (infected >= threshold):
        print("Probability of {0} infected {1} in average!".format(infectionProbability, infected))
        break

# write results to csv
file = open("results.csv", "w")
for i in range(0, len(csv)):
    file.write(";".join(str(val) for val in csv[i]))
    file.write("\n")
file.close()
