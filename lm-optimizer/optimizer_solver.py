from __future__ import print_function
from ortools.linear_solver import pywraplp
import pandas as pd


def lasagna_solver(df_mama_ready, df_garfield_ready, mg_dist_dict, gg_dist_dict, mama_capacity, garfield_demand, max_dist_mama, mama_id, garfield_id, score_dict, cluster_dist, dist_parameter, mama_parameter):
    
    M = df_mama_ready['quantity'].max()*10

    m = pywraplp.Solver.CreateSolver('SCIP')

    # DECISION VARIABLES--
    x={}
    z={}
    for (i,j) in score_dict.keys():
        z[(i,j)] = m.IntVar(0, 1, '') #assignment of mama to garfield
        x[(i,j)] = m.IntVar(0, m.infinity(), '') #how many deliveries

    y={}
    for i in mama_id:
        y[i] = m.IntVar(0, 1, '') # whether mama i is included 


    # CONSTRAINTS--

    # Capacity: for each mama i, sum of x[i,j] is at most "capacity"

    for i in mama_id:
        m.Add(m.Sum(x[(i,j)] for (i2, j) in score_dict.keys() if i == i2) <= mama_capacity[i])
    
    # Demand: for each garfield j, sum of x[i,j] is at most "demand"-- THIS DOES NOT GUARANTEE WE MEET ALL DEMAND
    for j in garfield_id:
        m.Add(m.Sum(x[(i,j)] for (i, j2) in score_dict.keys() if j == j2) <= garfield_demand[j])

    # Distance: (i,j) pair, distance larger than mama's max distance forces z(i,j) = 0
    for (i,j) in score_dict.keys():
        m.Add(z[(i,j)] * mg_dist_dict[(i,j)] <= max_dist_mama[i])

    # Distance: if an (i,j) is chosen, (i,j_2) may only be chosen if not in restricted list
    cnt = 0
    for (i,j) in score_dict.keys():
        for (i2, j2) in score_dict.keys():
            if i == i2 and (j,j2) not in gg_dist_dict:
                m.Add((1-z[(i,j)]) >= z[(i, j2)]).set_is_lazy(True)
                cnt += 1
    
    print("length of score dict: ", len(score_dict))
    print("total lazy constraints: ", cnt)
            
    # Relate x and z (big M)
    for (i,j) in score_dict.keys():
        m.Add(x[(i,j)] <= M*z[(i,j)])

    for (i,j) in score_dict.keys():
        m.Add(x[(i,j)] >= z[(i,j)])

    
    # Relate mama_indicator and matches_indicator
    for (i,j) in score_dict.keys():
        m.Add(z[(i,j)] <= y[i])
    
    for i in mama_id:
        m.Add(y[i] <= m.Sum(z[(i2,j2)] for (i2, j2) in score_dict.keys() if i == i2))


    # OBJECTIVE FUNCTION    
    objective_terms = []
    for (i,j) in score_dict.keys():
        objective_terms.append(score_dict[(i,j)]*x[(i,j)] - dist_parameter*mg_dist_dict[(i,j)]*z[(i,j)])

    for i in mama_id:
        objective_terms.append(mama_parameter*y[i])

    m.Maximize(m.Sum(objective_terms))

    # Solve
    status = m.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("Optimization completed successfully. Objective value is", m.Objective().Value())
        
        # Store matches
        matches = {}
        for (i,j) in score_dict.keys():
            if x[(i,j)].solution_value() > 0:
                matches[(i,j)] = x[(i,j)].solution_value()
    
        # for (i,j) in score_dict.keys():
        #     print(str(i), ":", y[i].solution_value())

    else:
        print("Something went wrong")
    
    return matches