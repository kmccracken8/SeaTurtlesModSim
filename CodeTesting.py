from modsim import *
from pandas import *

x_array = linspace(1,10,10)
y_array = linspace(1,10,10)

data = TimeSeries()

for t in linspace(1,10,10):
    data[t] = t

plot(data)
savefig('figs/testplot.pdf')



from modsim import *
from pandas import *

testDataframe = pandas.read_csv('data/testData.csv',index_col=0)
print(testDataframe)
testDataframe.columns = ['data']
print(testDataframe)

testData = testDataframe['data']
plot(testData)
savefig('figs/pandastestplot.pdf')
