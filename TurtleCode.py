from modsim import *
from pandas import *

system = System(nestR = .01, rr1 = .01, rr2 = .4, rr3 = .3, rr4 = .04, rr5 = .02, rr6 = .01)
state = State(population = 2000, r1T = TimeSeries(), r2T = TimeSeries(), r3T = TimeSeries(), r4T = TimeSeries(), r5T = TimeSeries(), r6T = TimeSeries(),)

turtleDataframe = pandas.read_csv('data/Garner_LeatherbackRemigrationIntervalsData_StCroix.csv',index_col = 0, header = 0)
nestingTurtleData = turtleDataframe['Turtles']
ri1 = turtleDataframe['RI1']
ri2 = turtleDataframe['RI2']
ri3 = turtleDataframe['RI3']
ri4 = turtleDataframe['RI4']
ri5 = turtleDataframe['RI5']
ri6up = turtleDataframe['RI6up']

def stepmk1(system,state,t,fiveYearPop, sixAndBefore, sabAge, r1T, r2T, r3T, r4T, r5T, r6T):
    newNesters = system.nestR * state.population
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

    for t in range(1983,2011):
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

plotResults(nestingTurtleData, runSimulation(system,state,stepmk1), 'Model Mk1','purple')
savefig('figs/nestingTurtleData-ModelMk1-16.pdf')

plotResults(ri2, state.r2T,'r2graph','grey')
savefig('figs/Returnyearcomparisons/2-returnRateTurtleData-ModelMk1-16.pdf')
plotResults(ri3, state.r3T,'r3graph','grey')
savefig('figs/Returnyearcomparisons/3-returnRateTurtleData-ModelMk1-16.pdf')
