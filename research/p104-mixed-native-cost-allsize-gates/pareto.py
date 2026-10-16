#!/usr/bin/env python3
"""Exhaustive nondominated 4D cost frontier of the single-sign bank family."""
import importlib.util
from pathlib import Path
p=Path(__file__).resolve().with_name('single_sign_optimum.py')
spec=importlib.util.spec_from_file_location('bank',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
points=set(m.costs)
def dominates(x,y):
    return all(a<=b for a,b in zip(x,y)) and any(a<b for a,b in zip(x,y))
frontier=sorted([x for x in points if not any(dominates(y,x) for y in points if y!=x)],
                key=lambda x:(x[3],x[0],x[1],x[2]))
assert len(points)==133 and len(frontier)==14
assert frontier[0]==(2224,416,1112,0)
assert (1496,292,764,8) in frontier
assert frontier[-1]==(1504,288,776,12)
print('PASS_SINGLE_SIGN_PARETO banks=4096 distinct_costs=133 nondominated=14 native=UNPROVEN kappa=UNCHANGED')
