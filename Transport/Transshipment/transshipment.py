"""
Transshipment problem
"""
# Import PuLP modeler functions
import pandas as pd
from pulp import *
import numpy as np

arcs = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
departure = [1,1,1,1,2,2,2,2,3,3,3,4,4,4]
arrival = [3,4,5,6,3,4,5,6,4,5,6,3,5,6]
cost = [8,13,25,28,15,12,26,25,6,16,17,6,14,16]
capacity= [100,100,100,100,100,100,100,100,100,100,100,100,100,100]

to_series = pd.Series(data=arrival)
nodes = [1,2,3,4,5,6]
sup_dem = [-160,-200,0,0,180,180]

prob = LpProblem("Transshipment", LpMinimize)

flow = LpVariable.dicts("flow",(arcs),0,None,LpInteger)
inflow = LpVariable.dicts("inflow",(nodes),None,None,LpInteger)
outflow = LpVariable.dicts("outflow",(nodes),None,None,LpInteger)

prob += lpSum([flow[i]*cost[i-1] for i in arcs])

for i in nodes:
        prob += lpSum(flow[j+1] for j in range(len(arcs)) if arrival[j] == i) - lpSum(flow[j+1] for j in range(len(arcs)) if departure[j] == i) == sup_dem[i-1]

for i in arcs:
    prob += flow[i] <= capacity[i-1]

log.info('==== Start PuLP optimization ====')
prob.solve(GLPK(timeLimit=60*5))
print('Problem solution:',value(prob.objective))
