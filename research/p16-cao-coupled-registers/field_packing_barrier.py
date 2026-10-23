#!/usr/bin/env python3
"""Model-specific barrier: (F_q x F_q) coordinatewise multiplication is not
an invertible-input/output linear isotope of a quadratic FIELD multiplication.
This does not identify Cao's rank-two job algebra or prove a P16 no-go.
"""
from itertools import product
import argparse,json

P=3
def field_mul(x,y):
    a,b=x;c,d=y
    return ((a*c-b*d)%P,(a*d+b*c)%P)
def component_mul(x,y):
    return ((x[0]*y[0])%P,(x[1]*y[1])%P)
def det(m):
    return (m[0]*m[3]-m[1]*m[2])%P
def transform(m,x):
    return ((m[0]*x[0]+m[1]*x[1])%P,(m[2]*x[0]+m[3]*x[1])%P)

def run():
    gl=[m for m in product(range(P),repeat=4) if det(m)]
    assert len(gl)==48
    x=(1,0);y=(0,1)
    assert component_mul(x,y)==(0,0)
    for a in gl:
        xx=transform(a,x)
        assert xx!=(0,0)
        for b in gl:
            yy=transform(b,y)
            assert yy!=(0,0)
            assert field_mul(xx,yy)!=(0,0)
    return {'status':'PASS_SPECIFIC_FIELD_PACKING_ZERO_DIVISOR_BARRIER',
            'input_algebra':'F3 x F3 direct product',
            'target_algebra':'F9=F3[t]/(t^2+1) quadratic field',
            'invertible_2x2_matrices':48,'tested_encoder_pairs':2304,
            'proof':'The direct product has nonzero x=(1,0) and y=(0,1) with xy=0. Invertible input maps preserve nonzero elements; field multiplication of nonzero elements is nonzero; an invertible output map cannot turn it into zero.',
            'Cao_H2_correspondence_proved':False,'new_kappa_proved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out')
    a=p.parse_args();s=run()
    if a.out:open(a.out,'w').write(json.dumps(s,indent=2,sort_keys=True)+'\n')
    print(s['status'],s['tested_encoder_pairs'])
