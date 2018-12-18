import docplex.cp.modeler as cp
from docplex.cp.model import CpoModel
mdl = CpoModel(name='cheat cp')
ivars = mdl.integer_var_list(5, min=0, max=4, name="i_vars")
all_diff = mdl.add(cp.all_diff(ivars))
bounds = mdl.add(ivars[0]+ivars[1] <= 5)
costs = [[1, 2, 3, 4, 5],
         [2, 3, 4, 5, 1],
         [3, 4, 5, 1, 2],
         [4, 5, 1, 2, 3],
         [5, 1, 2, 3, 4]]
mdl.maximize(cp.sum(cp.element(costs[i], ivars[i]) for i in range(5)))  # use minimize for a minimization problem
mdl.write_information()
mdl.export_model()
msol = mdl.solve()
print(msol)
print('='.join(['']*40))
print("Solve status: " + msol.get_solve_status())
print('Objective: %.2f' % msol.get_objective_values()[0])
print(''.join(['=']*40))
print('Variables:')
for v in ivars:
    print('%s: %d' % (v.name, msol[v]))
    
    
# second model
mdl = CpoModel(name='cheat cp scheduling')
intervals = mdl.interval_var_list(3, start=[1, cp.INTERVAL_MAX], length=5, optional=True, name='optional_interval')
iend = mdl.interval_var(length=1, name='end')
ialt = mdl.interval_var(name='alternative_interval')
ispan = mdl.interval_var(name='span_interval')
iseq = mdl.sequence_var(intervals + [iend], types=[0, 0, 0, 1], name='sequence')
transitions = mdl.transition_matrix([[1, 2], [3, 4]], name='transitions')  # type of the variables are used as indices
mdl.add(cp.no_overlap(iseq, transitions))  # ensure that no present intervals overlap, add also the transition
mdl.add(cp.last(iseq, iend))  # ensure that iend is the last interval of the sequence

# ensure that only one interval is present among all intervals. ialt represent this interval
mdl.add(cp.alternative(ialt, intervals))

# ensure that ispan represent a group of intervals
mdl.add(cp.span(ispan, intervals + [iend]))

# add a cumulative function (here, only one interval can be performed)
mdl.add(cp.sum(cp.step_at_start(v, 1) for v in intervals) <= 1)
mdl.minimize(cp.sum([cp.max(cp.end_of(i) for i in intervals), cp.start_of(ialt), cp.end_of(ispan)]))
mdl.write_information()
mdl.export_model()
msol = mdl.solve(TimeLimit=10)  # add a time limit of 10 seconds
print(msol)
print('End of iend: %d' % msol.get_var_solution(iend).get_end())