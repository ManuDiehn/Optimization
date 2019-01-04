# the production at each node if positive, otherwise the consumption
d = [ 500, -50, -95, -10, -73, -55, -125, -32, -40, -20 ]
size = len(d)
nodes = range(size)
print('Balanced demand (%d): %d' % (size, sum(d)))

# capacity of the arcs
ca = [ [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
       [20, 30, 40, 50, 60, 70, 80, 90, 100, 10],
       [30, 40, 50, 60, 70, 80, 90, 100, 10, 20],
       [40, 50, 60, 70, 80, 90, 100, 10, 20, 30],
       [50, 60, 70, 80, 90, 100, 10, 20, 30, 40],
       [60, 70, 80, 90, 100, 10, 20, 30, 40, 50],
       [70, 80, 90, 100, 10, 20, 30, 40, 50, 60],
       [80, 90, 100, 10, 20, 30, 40, 50, 60, 70],
       [90, 100, 10, 20, 30, 40, 50, 60, 70, 80],
       [100, 10, 20, 30, 40, 50, 60, 70, 80, 90]
     ]

# linear fixed cost: the cost of opening an arc is proportional to its capacity
fc = [ [10 * c for c in ca1] for ca1 in ca]

# linear variable cost: the cost of transporting one unit of gas
vc = 1

# unsatisfied demand: penalty for each unit of gas which is not consumed or produced
p = max(max(fc)) / min(min(ca))

sign = lambda a: (a>0) - (a<0)  # helper function that return 1 if a > 0, -1 if a < 0, 0 if a == 0


#######Model

from docplex.mp.model import Model
mdl = Model(name='gas network')

x = [ [mdl.continuous_var(lb=0, ub=c, name='x_%d_%d' %(i,j)) for j, c in enumerate(ca1)] for i, ca1 in enumerate(ca)]
y = [ [mdl.binary_var(name='y_%d_%d' %(i,j)) for j in nodes] for i in nodes]
z = [ mdl.continuous_var(lb=0, name='z_%d' % i) for i in nodes]

flow = mdl.add_constraints((sum(x[i]) - sum(x[j][i] for j in nodes) == d[i] - sign(d[i]) * z[i], 'flow_%d' % i)
                           for i in nodes)
open_arcs = [mdl.add_constraints((x[i][j] <= ca[i][j] * y[i][j], 'open_arc_%d_%d' %(i,j)) for j in nodes)
             for i in nodes]

mdl.minimize(sum(vc * x[i][j] for i in nodes for j in nodes) +
             sum(fc[i][j] * y[i][j] for i in nodes for j in nodes) +
             sum(p * z[i] for i in nodes))

mdl.solve()


print('Cost: %.2f' % mdl.objective_value)
for i, z_sol in enumerate(z):
    if z_sol.solution_value > 0:
        print('Demand not met for %d: %.2f' &(i, z_sol.solution_value))
for i in nodes:
    for j in nodes:
        if y[i][j].solution_value > 0:
            print('Flow from %d to %d: %.2f / %d' %(i, j, x[i][j].solution_value, ca[i][j]))