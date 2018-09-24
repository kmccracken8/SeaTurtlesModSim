from modsim import *
from pandas import *

x_array = linspace(1,10,10)
y_array = linspace(1,10,10)

data = TimeSeries()

for t in linspace(1,10,10):
    data[t] = t

plot(data)
savefig('figs/testplot.pdf')
