"""
Transshipment problem
"""
# Import PuLP modeler functions
import pandas as pd
from pulp import *
import numpy as np

arcs = [1,2,3,4,5,6,7,8,9,10]
departure = [1 ,1 ,1 ,1 ,2 ,2 ,2 ,3 ,3 ,4]
arrival =   [2 ,3 ,4 ,5 ,3 ,4 ,5 ,4 ,5 ,5]
cost = [4260 ,2916 ,2376 ,9216 ,2256 ,2400 ,8064 ,2580 ,6888 ,9456]
distance = [355 ,243 ,198 ,768 ,188 ,200 ,672 ,215 ,574 ,788]
capacity= [100,100,100,100,100,100,100,100,100,100]
avg_capacity = 70
avg_vel = 400
avg_vel = [avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel]
avg_grnd_time = 0.5
time_allowed = 13
allowed_planes = [round(13/((distance[i]/avg_vel[i])+avg_grnd_time)) for i in range(len(arcs))]

nodes = [1,2,3,4,5]
sup_dem = [-1310 ,-758 ,2 ,748, 1318]

prob = LpProblem("Transshipment", LpMinimize)

flow = LpVariable.dicts("flow",(arcs),0,None,LpInteger)
aircrafts = LpVariable.dicts("aircrafts",(arcs),0,None,LpInteger)

prob += lpSum([aircrafts[i+1]*cost[i] for i in range(len(arcs))])

for i in arcs:
    prob +=  aircrafts[i] <= allowed_planes[i-1]

for i in nodes:
        prob += lpSum(flow[j+1] for j in range(len(arcs)) if arrival[j] == i) - lpSum(flow[j+1] for j in range(len(arcs)) if departure[j] == i) <= sup_dem[i-1]



for i in arcs:
    prob += flow[i] <= aircrafts[i]*avg_capacity


log.info('==== Start PuLP optimization ====')
prob.solve(COIN_CMD(timeLimit=60*5))
print('Problem solution:',value(prob.objective))


for v in prob.variables():
    print(v.name, "=", v.varValue)

print(allowed_planes)