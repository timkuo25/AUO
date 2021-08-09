#!/usr/bin/env python
# coding: utf-8

# In[9]:
import time
from gurobipy import *

# t is each minute
def Model_1_solve(ma, h, b, n, rA, rB, s, p, d, cD, cT):
    start = time.time()
    m = Model("research")
    T = 1000

    # Decision Variables
    X = {}
    Y = {}
    W = {}
    Z = {}
    A = {}

    for i in range(1, ma+1):
        for j in range(n[i]+1):
            X[i, j] = m.addVar(vtype="B", name="X(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            Y[i, j] = m.addVar(vtype="B", name="Y(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            W[i, j] = m.addVar(vtype="I", name="W(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            Z[i, j] = m.addVar(vtype="I", name="Z(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            for t in range(T):
                A[i, j, t] = m.addVar(
                    vtype="B", name="A(%s,%s,%s)" % (i, j, t))
    m.update()

    # Constraints
    for i in range(1, ma+1):
        m.addConstr(X[i, 0] == 0)

    for (i, j) in X:
        if j != 0:
            for k in range(j, n[i]+1):
                m.addConstr(Y[i, k] >= X[i, j])
                print(Y[i, k] >= X[i, j])

    for i in range(1, ma + 1):  # There is at most one maintenance on the machine i
        m.addConstr(quicksum(X[i, j] for j in range(n[i] + 1)) <= 1)

    for (i, j) in Y:
        m.addConstr(Y[i, j] <= quicksum(X[i, k] for k in range(1, j+1)))

    for (i, j) in Z:
        m.addConstr(Z[i, j] >= s[i][j] + p[i][j] + W[i, j] - d[i][j])

    for (i, j) in W:
        m.addConstr(W[i, j] >= b * quicksum(X[i, k] for k in range(1, j+1)) -
                    quicksum(Y[i, k] * (s[i][k]-s[i][k-1] - p[i][k-1]) for k in range(1, j+1)))

    for t in range(T):
        m.addConstr(quicksum(quicksum(A[i, j, t] * X[i, j]
                                      for j in range(n[i]+1)) for i in range(1, ma+1)) <= h)

    for (i, j) in X:
        for t in range(T):
            if t in range(s[i][j] + p[i][j] + 1, s[i][j] + p[i][j] + b + 1):
                m.addConstr(A[i, j, t] == 1)
            else:
                m.addConstr(A[i, j, t] == 0)

    m.update()
    m.setObjective(quicksum(p[i][j] * ((rA[i] * Y[i, j]) + rB[i] * (1 - Y[i, j])) for (i, j) in Y)
                   + quicksum(Z[i, j] for (i, j) in Z), GRB.MINIMIZE)
    m.Params.LogToConsole = 0
    m.setParam('Timelimit', 1200)
    m.optimize()

    # Output
    if m.status == 2:
        opt = m.ObjVal
        gap = 0
        lowerbound = opt
    elif m.status == 9:
        opt = m.ObjVal
        gap = m.MIPGap
        lowerbound = opt/(gap+1)

    end = time.time()
    model_spend = end - start

    return opt, model_spend, gap, lowerbound

# t is the period
def Model_2_solve(ma, h, b, n, rA, rB, s, p, d, cD, cT):
    start = time.time()
    m = Model("research")
    T = 1000

    # Decision Variables
    X = {}
    Y = {}
    W = {}
    Z = {}
    A = {}

    for i in range(1, ma+1):
        for j in range(n[i]+1):
            X[i, j] = m.addVar(vtype="B", name="X(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            Y[i, j] = m.addVar(vtype="B", name="Y(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            W[i, j] = m.addVar(vtype="I", name="W(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            Z[i, j] = m.addVar(vtype="I", name="Z(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            for t in range(T):
                A[i, j, t] = m.addVar(
                    vtype="B", name="A(%s,%s,%s)" % (i, j, t))
    m.update()

    # Constraints
    for i in range(1, ma+1):
        m.addConstr(X[i, 0] == 0)

    for (i, j) in X:
        if j != 0:
            for k in range(j, n[i]+1):
                m.addConstr(Y[i, k] >= X[i, j])
                print(Y[i, k] >= X[i, j])

    for i in range(1, ma + 1):  # There is at most one maintenance on the machine i
        m.addConstr(quicksum(X[i, j] for j in range(n[i] + 1)) <= 1)

    for (i, j) in Y:
        m.addConstr(Y[i, j] <= quicksum(X[i, k] for k in range(1, j+1)))

    for (i, j) in Z:
        m.addConstr(Z[i, j] >= s[i][j] + p[i][j] + W[i, j] - d[i][j])

    for (i, j) in W:
        m.addConstr(W[i, j] >= b * quicksum(X[i, k] for k in range(1, j+1)) -
                    quicksum(Y[i, k] * (s[i][k]-s[i][k-1] - p[i][k-1]) for k in range(1, j+1)))

    
    for t in range(T):
        m.addConstr(quicksum(quicksum(A[i, j, t] * X[i, j]
                                      for j in range(n[i]+1)) for i in range(1, ma+1)) <= h)
    #Difference
    

    m.update()
    m.setObjective(quicksum(p[i][j] * ((rA[i] * Y[i, j]) + rB[i] * (1 - Y[i, j])) for (i, j) in Y)
                   + quicksum(Z[i, j] for (i, j) in Z), GRB.MINIMIZE)
    m.Params.LogToConsole = 0
    m.setParam('Timelimit', 1200)
    m.optimize()

    # Output
    if m.status == 2:
        opt = m.ObjVal
        gap = 0
        lowerbound = opt
    elif m.status == 9:
        opt = m.ObjVal
        gap = m.MIPGap
        lowerbound = opt/(gap+1)

    end = time.time()
    model_spend = end - start

    return opt, model_spend, gap, lowerbound
