from sympy import Symbol, solve, pprint
s = Symbol('s')
u = Symbol('u')
t = Symbol('t')
a = Symbol('a')
expr = u*t + (1/2)*a*t*t - s
t_expr = solve(expr,t, dict=True)
print(t_expr)
