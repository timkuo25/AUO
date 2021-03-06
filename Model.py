import time
from gurobipy import *


def Model_wait(ma, h_bar, n, rA, rB, h, b, s, p, d, cD, cT):  # t is each minute
    start = time.time()
    m = Model("research")
    m.setParam('Timelimit', 1200)
    max = 0
    for i in range(1, ma+1):
        for j in range(n[i], n[i]+1):
            if s[i][j]+p[i][j] > max:
                max = s[i][j]+p[i][j]
    T = max

    # Decision Variables
    X = {}
    Y = {}
    W = {}
    Z = {}
    a = {}
    a_1 = {}
    a_2 = {}
    U = {}
    G = {}

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
            U[i, j] = m.addVar(vtype="I", name="U(%s,%s)" % (i, j))
    for i in range(1, ma+1):
        for t in range(T):
            a[i, t] = m.addVar(vtype="B", name="a(%s,%s)" % (i, t))
            a_1[i, t] = m.addVar(vtype="B", name="a_1(%s,%s)" % (i, t))
            a_2[i, t] = m.addVar(vtype="B", name="a_2(%s,%s)" % (i, t))
    for i in range(1, ma+1):
        for j in range(n[i]+1):
            G[i, j] = m.addVar(vtype="I", name="U(%s,%s)" % (i, j))

    # Constraints
    for i in range(1, ma+1):
        m.addConstr(X[i, 0] == 0)

    for (i, j) in X:
        if j != 0:
            for k in range(j, n[i]+1):
                m.addConstr(Y[i, k] >= X[i, j])

    for i in range(1, ma + 1):  # There is at most one maintenance on the machine i
        m.addConstr(quicksum(X[i, j] for j in range(n[i] + 1)) <= 1)

    for (i, j) in Y:
        m.addConstr(Y[i, j] <= quicksum(X[i, k] for k in range(1, j+1)))

    for (i, j) in Z:
        m.addConstr(Z[i, j] >= s[i][j] + p[i][j] + W[i, j] - d[i][j])

    for (i, j) in W:
        m.addConstr(W[i, j] >= b[i] * quicksum(X[i, k] for k in range(1, j+1)) -
                    quicksum(Y[i, k] * (s[i][k]-s[i][k-1] - p[i][k-1]) for k in range(1, j+1)) +
                    quicksum(G[i, k] for k in range(1, j+1)))

    M = 0
    for i in range(1, ma+1):
        for j in range(1, n[i]+1):
            M += p[i][j]
    M = M * ma

    for (i, j) in X:
        if j != 0:
            for t in range(s[i][j-1] + p[i][j-1], T):
                m.addConstr(t - (s[i][j-1] + p[i][j-1] + U[i, j])
                            <= M * (a_1[i, t] + (1-X[i, j])))
                m.addConstr(s[i][j-1] + p[i][j-1] + U[i, j] + 1 +
                            b[i] - t <= M * (a_2[i, t] + (1-X[i, j])))

    for i in range(1, ma+1):
        for t in range(T):
            m.addConstr(a_1[i, t] + a_2[i, t] - 1 <= a[i, t])

    for t in range(T):
        m.addConstr(quicksum(a[i, t] * h[i] for i in range(1, ma+1)) <= h_bar)

    for (i, j) in U:
        m.addConstr(U[i, j] <= M * X[i, j])
        m.addConstr(U[i, j] >= -M * X[i, j])

    for (i, j) in G:
        m.addConstr(U[i, j] - M*(1-X[i, j]) <= G[i, j])
        m.addConstr(G[i, j] <= U[i, j] + M*(1-X[i, j]))
        m.addConstr(-M*X[i, j] <= G[i, j])
        m.addConstr(G[i, j] <= M*X[i, j])

    m.update()
    m.setObjective(cD * quicksum(p[i][j] * ((rA[i] * Y[i, j]) + rB[i] * (1 - Y[i, j])) for (i, j) in Y)
                   + cT * quicksum(Z[i, j] for (i, j) in Z), GRB.MINIMIZE)
    m.Params.LogToConsole = 0
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


def Model_period(ma, h_bar, n, rA, rB, h, b, s, p, d, cD, cT):  # t is the period
    start = time.time()

    # Starting time preprocessing
    ss = {}  # Updated starting time
    TT = []  # T set

    for i in range(1, ma+1):  # Update the starting time if there is the idle time
        for j in range(n[i], 0, -1):
            if s[i][j-1] + p[i][j-1] != s[i][j]:
                ss[i, j] = s[i][j-1] + p[i][j-1]
                TT.append(ss[i, j])
            else:
                ss[i, j] = s[i][j]
                TT.append(ss[i, j])

    last = [s[i][n[i]] + p[i][n[i]] for i in range(1, ma+1)]
    last.sort()
    for i in range(len(last)-1):
        TT.append(last[i])
    TT = list(set(TT))
    TT.sort()  # Complete the T period set

    temp = 0
    span = {}  # Span that includes period to period
    for i in range(1, ma+1):
        for j in range(1, n[i]+1):
            valid = 0
            temp = ss[i, j] + b[i]
            for k in range(len(TT)):
                if TT[k] >= temp:
                    span[i, j] = (TT.index(ss[i, j]), k-1)
                    valid = 1
                    break
            if valid == 0:
                span[i, j] = (TT.index(ss[i, j]), len(TT)-1)

    m = Model("research")
    m.setParam('Timelimit', 1200)

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
            for t in range(len(TT)):
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

    for i in range(1, ma + 1):  # There is at most one maintenance on the machine i
        m.addConstr(quicksum(X[i, j] for j in range(n[i] + 1)) <= 1)

    for (i, j) in Y:
        m.addConstr(Y[i, j] <= quicksum(X[i, k] for k in range(1, j+1)))

    for (i, j) in Z:
        m.addConstr(Z[i, j] >= s[i][j] + p[i][j] + W[i, j] - d[i][j])

    for (i, j) in W:
        m.addConstr(W[i, j] >= b[i] * quicksum(X[i, k] for k in range(1, j+1)) -
                    quicksum(Y[i, k] * (s[i][k]-s[i][k-1] - p[i][k-1]) for k in range(1, j+1)))

    for t in range(len(TT)):
        m.addConstr(quicksum(quicksum(A[i, j, t] * X[i, j] * h[i]
                                      for j in range(n[i]+1)) for i in range(1, ma+1)) <= h_bar)

    for (i, j) in X:
        if j != 0:
            for t in range(len(TT)):
                if t in range(span[i, j][0], span[i, j][1]+1):
                    m.addConstr(A[i, j, t] == 1)
                else:
                    m.addConstr(A[i, j, t] == 0)

    m.update()
    m.setObjective(cD * quicksum(p[i][j] * ((rA[i] * Y[i, j]) + rB[i] * (1 - Y[i, j])) for (i, j) in Y)
                   + cT * quicksum(Z[i, j] for (i, j) in Z), GRB.MINIMIZE)
    m.Params.LogToConsole = 0
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


def Model_eachMin(ma, h_bar, n, rA, rB, h, b, s, p, d, cD, cT):  # t is each minute
    start = time.time()
    m = Model("research")
    m.setParam('Timelimit', 1200)
    max = 0
    for i in range(1, ma+1):
        for j in range(n[i], n[i]+1):
            if s[i][j]+p[i][j] > max:
                max = s[i][j]+p[i][j]
    T = max

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

    for i in range(1, ma + 1):  # There is at most one maintenance on the machine i
        m.addConstr(quicksum(X[i, j] for j in range(n[i] + 1)) <= 1)

    for (i, j) in Y:
        m.addConstr(Y[i, j] <= quicksum(X[i, k] for k in range(1, j+1)))

    for (i, j) in Z:
        m.addConstr(Z[i, j] >= s[i][j] + p[i][j] + W[i, j] - d[i][j])

    for (i, j) in W:
        m.addConstr(W[i, j] >= b[i] * quicksum(X[i, k] for k in range(1, j+1)) -
                    quicksum(Y[i, k] * (s[i][k]-s[i][k-1] - p[i][k-1]) for k in range(1, j+1)))

    for t in range(T):
        m.addConstr(quicksum(quicksum(A[i, j, t] * X[i, j] * h[i]
                                      for j in range(n[i]+1)) for i in range(1, ma+1)) <= h_bar)

    for (i, j) in X:
        if j != 0:
            for t in range(T):
                if t in range(s[i][j-1] + p[i][j-1] + 1, s[i][j-1] + p[i][j-1] + int(b[i]) + 1):
                    m.addConstr(A[i, j, t] == 1)
                else:
                    m.addConstr(A[i, j, t] == 0)

    m.update()
    m.setObjective(quicksum(p[i][j] * ((rA[i] * Y[i, j]) + rB[i] * (1 - Y[i, j])) for (i, j) in Y)
                   + quicksum(Z[i, j] for (i, j) in Z), GRB.MINIMIZE)
    m.Params.LogToConsole = 0
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
