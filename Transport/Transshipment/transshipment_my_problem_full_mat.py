"""
Transshipment problem
"""
# Import PuLP modeler functions
import pandas as pd
from pulp import *
import numpy as np

arcs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
departure = [0 ,0 ,0 ,0 ,1 ,1 ,1 ,2 ,2 ,3,1,2,2,3,3,3,4,4,4,4]
arrival =   [1,2,3,4 ,2 ,3 ,4 ,3,4,4,0,0,1,0,1,2,0,1,2,3]

cost = [4260 ,2916 ,2376 ,9216 ,2256 ,2400 ,8064 ,2580 ,6888 ,9456,4260,2916,2256,2376,2400,2580,9216,8064,6888,9456]

distance = [355 ,243 ,198 ,768 ,188 ,200 ,672 ,215 ,574 ,788,355,243,188,198,200,215,768,672,574,788]


avg_capacity = 70
avg_vel = 400
avg_vel = [avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel,avg_vel]
avg_grnd_time = 0.5
time_allowed = 13
allowed_planes = [round(13/((distance[i]/avg_vel[i])+avg_grnd_time)) for i in range(len(arcs))]

nodes = [0,1,2,3,4,5,6,7,8,9]
sup_dem_ij = [-1310 ,-758 ,2 ,748, 1318]
sup_dem_ji = [1310,758,-2,-748,-1318]

prob = LpProblem("Transshipment", LpMinimize)

flow = LpVariable.dicts("flow",(arcs),0,None,LpInteger)
aircrafts = LpVariable.dicts("aircrafts",(arcs),0,None,LpInteger)

prob += lpSum([aircrafts[i]*cost[i] for i in range(len(arcs))])

for i in arcs:
    prob +=  aircrafts[i] <= allowed_planes[i]

for i in range(0,len(nodes)//2):

        prob += lpSum(flow[j] for j in range(0,len(arcs)//2) if arrival[j] == i) - lpSum(flow[j] for j in range(0,len(arcs)//2) if departure[j] == i) <= sup_dem_ij[i]

for i in range(0,len(nodes)//2):
        prob += lpSum(flow[j] for j in range(len(arcs)//2,len(arcs)) if arrival[j] == i) - lpSum(flow[j] for j in range(len(arcs)//2,len(arcs)) if departure[j] == i) <= sup_dem_ji[i]
        
for i in arcs:
    prob += flow[i] <= aircrafts[i]*avg_capacity


log.info('==== Start PuLP optimization ====')
prob.solve(COIN_CMD(timeLimit=60*5))
print('Problem solution:',value(prob.objective))


for v in prob.variables():
    print(v.name, "=", v.varValue)

print(allowed_planes)