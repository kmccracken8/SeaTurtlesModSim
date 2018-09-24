from modsim import *
from pandas import *

testDataframe = pandas.read_csv('data/testData.csv',index_col=0)
print(testDataframe)
testDataframe.columns = ['data']
print(testDataframe)

testData = testDataframe['data']
plot(testData)
savefig('figs/pandastestplot.pdf')
