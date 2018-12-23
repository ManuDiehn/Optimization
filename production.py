biscuits = ['cookie', 'cupcake', 'brownie']
goods = ['flour', 'sugar', 'chocolate', 'oil', 'eggs']
# quantities
w = [[.1, .15, .1, .05, 0],  # cookie
     [.3, .2, .05, .1, 2],  # cupcake
     [.05, .3, .3, .1, 3]]  # brownie
c = [2, 3, 5]  # price
s = [25, 40, 30, 15, 300]  # stock
print(w)
from docplex.mp.model import Model
mdl = Model(name='production')

x = [mdl.continuous_var(lb=0, name='%s_production' % b) for b in biscuits]
stocks = mdl.add_constraints((sum(w[j][i] * v for j, v in enumerate(x)) <= s[i], '%s_stock' % g)
                             for i, g in enumerate(goods))
mdl.maximize(sum(c[i] * v for i, v in enumerate(x)))
mdl.solve()
print('Revenue: %.2f' % mdl.objective_value)
print('Production:')
for i, b in enumerate(biscuits):
    print('  %s: %.2f' %(b, x[i].solution_value))

print('Expected increase of revenue for:')
for i, g in enumerate(goods):
    print('  %s: %.2f (left: %.2f)' %(g, stocks[i].dual_value, stocks[i].slack_value))


stocks[1].right_expr += 1
mdl.solve()

print('Revenue: %.2f' % mdl.objective_value)
print('Production:')
for i, b in enumerate(biscuits):
    print('  %s: %.2f' %(b, x[i].solution_value))
print('Expected increase of revenue for:')
for i, g in enumerate(goods):
    print('  %s: %.2f (left: %.2f)' %(g, stocks[i].dual_value, stocks[i].slack_value))