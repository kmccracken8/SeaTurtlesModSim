from modsim import *
from pandas import *

systemTest = System(nestR = .002, rr1 = .01, rr2 = .59, rr3 = .28, rr4 = .16, rr5 = .047, rr6 = .015, startYear = 1984, endYear = 2020, startPop = 200)
stateTest = State(population = 2000, r1T = TimeSeries(), r2T = TimeSeries(), r3T = TimeSeries(), r4T = TimeSeries(), r5T = TimeSeries(), r6T = TimeSeries(), newN = TimeSeries())

turtleDataframe2 = pandas.read_csv('data/NOAA_LeatherbackNestsData.csv',index_col = 0, header = 0)
nestsData = turtleDataframe2['Nests']

def stepmk1(system,state,t,fiveYearPop, sixAndBefore, sabAge, r1T, r2T, r3T, r4T, r5T, r6T):
    if t < int(system.startYear) + 2:  #for the first two years, we want a solid base of new nesters
        newNesters = system.startPop
    else:
        newNesters = system.nestR * state.population# new nesters arriving this year based on a tuned rate and current population
    state.newN[t] = newNesters

    R1 = fiveYearPop[1] * system.rr1    #fiveYearPop = the population from the previous 5 years
                                        #i.e. fiveYearPop[1] is the population 1 year ago
    r1T[t] = R1                         #fills the system's Timeseries for return numbers every x years for each year
    R2 = fiveYearPop[2] * system.rr2
    r2T[t] = R2
    R3 = fiveYearPop[3] * system.rr3
    r3T[t] = R3
    R4 = fiveYearPop[4] * system.rr4
    r4T[t] = R4
    R5 = fiveYearPop[5] * system.rr5
    r5T[t] = R5
    if t > int(system.startYear) + 5:       #once we have 6 years of data we can include the tuned rate from 6 years ago and before
        R6up = (sixAndBefore / sabAge) * system.rr6     #sixAndBefore/sabAge is the average population from the beginning of the model
    else:
        R6up = 0
    r6T[t] = R6up

    nesters = newNesters + R1 + R2 + R3 + R4 + R5 + R6up       #sums all the nesters added this year
    return nesters      #returns the number of nesters this year

def runSimulation(system,state,step):
    results = TimeSeries()  #Stores nesting population
    fiveYearPop = TimeSeries() #Temporarily stores the population for the last five years for each step

    for n1 in range(1,6): #Fills fiveYearPop temporary values before they can be set
        fiveYearPop[n1] = 0

    for t in range(int(system.startYear),int(system.endYear)):  #Once we have six years of data this sums the population of every year six years before t and earlier
        if t <= int(system.startYear) + 5:
            sixAndBefore = 0
            sabAge = 1 #Not 0 to avoid dividing by 0 in stop
        else:
            sabAge = t - int(system.startYear) - 5 #Give number of years that hve happened since start of mdel until 6 years prior
            for s in range (int(system.startYear),t-5):
                sixAndBefore = sixAndBefore + results[s]    #Adds populaiton from the last year to the total population from start of model

        if t <= int(system.startYear) + 4:   #Prevents fiveYearPop from receiving population data from years that weren't simulated
            begC = (t - int(system.startYear)) + 1
        else:
            begC = 6    #begC is a counter to define range for the loop below

        if t != int(system.startYear):   #Stores population data in fiveYearPop as long as it's not the first year of simulation
            for p in range(1,begC):
                fiveYearPop[p] = results[t-p]   #Fills fiveYearPop in reverse so that the first instance is 1 year ago, etc.

        #Runs step functions, calculating nesting population based on previous year populations
        results[t] = step(system,state,t, fiveYearPop, sixAndBefore, sabAge, state.r1T, state.r2T, state.r3T, state.r4T, state.r5T, state.r6T)
    return results

def plotResults(turtleData, timeseries, title, colorin):    #Plotting function
    plot(turtleData, '--', label='Nesting Data')
    plot(timeseries, color=colorin, label='model')

    decorate(xlabel='Year',
             ylabel='Nesting Population',
             title=title)

plt.figure(11) #plots new figure with id 11

plotResults(nestsData, runSimulation(systemTest,stateTest,stepmk1), 'Model Mk1','purple')   #Plots nesting population data against simulated nesting population
savefig('figs/NewData/nestsData-ModelMk1-.png')
