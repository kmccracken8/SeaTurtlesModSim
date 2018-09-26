from modsim import *
from pandas import *

system = System(nestR = .002, rr1 = .01, rr2 = .59, rr3 = .28, rr4 = .16, rr5 = .047, rr6 = .015)
state = State(population = 2000, r1T = TimeSeries(), r2T = TimeSeries(), r3T = TimeSeries(), r4T = TimeSeries(), r5T = TimeSeries(), r6T = TimeSeries(), newN = TimeSeries())

turtleDataframe = pandas.read_csv('data/Garner_LeatherbackRemigrationIntervalsData_StCroix.csv',index_col = 0, header = 0)
nestingTurtleData = turtleDataframe['Turtles']
ri1 = turtleDataframe['RI1']
ri2 = turtleDataframe['RI2']
ri3 = turtleDataframe['RI3']
ri4 = turtleDataframe['RI4']
ri5 = turtleDataframe['RI5']
ri6 = turtleDataframe['RI6up']
new = turtleDataframe['Unknown']

def stepmk1(system,state,t,fiveYearPop, sixAndBefore, sabAge, r1T, r2T, r3T, r4T, r5T, r6T):
    if t < 1985:
        newNesters = 22
    else:
        newNesters = system.nestR * state.population
    state.newN[t] = newNesters

    R1 = fiveYearPop[1] * system.rr1
    r1T[t] = R1
    R2 = fiveYearPop[2] * system.rr2
    r2T[t] = R2
    R3 = fiveYearPop[3] * system.rr3
    r3T[t] = R3
    R4 = fiveYearPop[4] * system.rr4
    r4T[t] = R4
    R5 = fiveYearPop[5] * system.rr5
    r5T[t] = R5
    if t > 1988:
        R6up = (sixAndBefore / sabAge) * system.rr6
    else:
        R6up = 0
    r6T[t] = R6up

    nesters = newNesters + R1 + R2 + R3 + R4 + R5 + R6up
    return nesters

def runSimulation(system,state,step):
    results = TimeSeries()
    fiveYearPop = TimeSeries()

    for n1 in range(1,6):
        fiveYearPop[n1] = 0

    for t in range(1983,2020):
        if t <= 1988:
            sixAndBefore = 0
            sabAge = 1
        else:
            sabAge = t - 1983 - 5
            for s in range (1983,t-5):
                sixAndBefore = sixAndBefore + results[s]

        if t <= 1987:
            begC = (t - 1983) + 1
        else:
            begC = 6

        if t != 1983:
            for p in range(1,begC):
                fiveYearPop[p] = results[t-p]

        results[t] = step(system,state,t, fiveYearPop, sixAndBefore, sabAge, state.r1T, state.r2T, state.r3T, state.r4T, state.r5T, state.r6T)
    return results

def plotResults(turtleData, timeseries, title, colorin):
    plot(turtleData, '--', label='Nesting Data')
    plot(timeseries, color=colorin, label='model')

    decorate(xlabel='Year',
             ylabel='Nesting Population',
             title=title)




pId = 0

plt.figure(11)
plotResults(nestingTurtleData, runSimulation(system,state,stepmk1), 'Model Mk1','purple')
savefig('figs/Returnyearcomparisons/nestingTurtleData-ModelMk1-' + str(pId) + '.png')

for num in range(1,7):
    plotData = 'ri' + str(num)
    stateData = 'state.r' + str(num) + 'T'
    plotTitle = 'r' + str(num) + 'graph'
    plt.figure(num)
    plotResults(eval(plotData),eval(stateData),plotTitle,'blue')
    savefig('figs/Returnyearcomparisons/' + str(pId) + '-returnRateTurtleData-ModelMk1-' + str(num) + '.png')

plt.figure(10)
plotResults(new,state.newN,'New Nesters','blue')
savefig('figs/Returnyearcomparisons/' + str(pId) + '-newNestersTurtleData-ModelMk1-10.png')
