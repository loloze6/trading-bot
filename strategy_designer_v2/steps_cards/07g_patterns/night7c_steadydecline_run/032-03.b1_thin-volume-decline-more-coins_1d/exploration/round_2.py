import numpy as np, pandas as pd
from scipy import stats

def _clt(d, col):
    d = d.dropna(subset=[col])
    if len(d) < 5: return np.nan, len(d), 0
    m = d[col].mean()
    g = (d[col]-m).groupby(d['day']).sum()
    G = len(g)
    se = np.sqrt((g**2).sum()*G/(G-1))/len(d)
    return (m/se if se>0 else np.nan), len(d), G

def _slope_clt(d, x, y):
    d = d.dropna(subset=[x,y]).copy()
    d = d[np.isfinite(d[x])]
    if len(d) < 20: return {'slope':np.nan,'t':np.nan,'n':len(d),'days':0}
    X = d[x]-d[x].mean(); Y = d[y]-d[y].mean()
    b = (X*Y).sum()/(X**2).sum()
    e = Y-b*X
    s = (X*e).groupby(d['day']).sum()
    G = len(s)
    se = np.sqrt((s**2).sum()*G/(G-1))/(X**2).sum()
    return {'slope':b,'t':b/se,'n':len(d),'days':G}

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b['close']; v = b['volume'].replace(0,np.nan)
            rng = (b['high']-b['low'])/c
            r1 = c.pct_change()
            f = pd.DataFrame({'coin':coin,'win':w,'day':pd.to_datetime(b['timestamp']).dt.floor('D')})
            f['ret28'] = c/c.shift(28)-1
            f['ret14'] = c/c.shift(14)-1
            f['ret7'] = c/c.shift(7)-1
            f['vr7_28'] = np.log(v.rolling(7).mean()/v.shift(7).rolling(28).mean())
            f['rr7_28'] = np.log(rng.rolling(7).mean()/rng.shift(7).rolling(28).mean())
            f['rr28_42'] = np.log(rng.rolling(28).mean()/rng.shift(28).rolling(42).mean())
            f['vr28_42'] = np.log(v.rolling(28).mean()/v.shift(28).rolling(42).mean())
            f['rng1'] = np.log(rng/rng.shift(1).rolling(28).mean())
            f['vthin_rec'] = b.get('debug_info.components.vol_thin.last_history_value')
            f['fwd5'] = c.shift(-5)/c-1
            f['grid'] = (np.arange(len(b))%5==0)
            f['alloc'] = b['postRebalance_current_allocation']
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    G = A[A.grid & A.fwd5.notna()].copy()
    drift = G.groupby('coin')['fwd5'].mean()
    G['ex5'] = G['fwd5'] - G['coin'].map(drift)
    G['yr'] = G['day'].dt.year
    dec = G[G.ret28<0]
    out = {}
    res = {}
    for x in ['ret28','ret14','ret7','vr7_28','rr7_28','rr28_42','vr28_42','rng1','vthin_rec']:
        res['all_'+x] = _slope_clt(G, x, 'ex5')
        res['dec_'+x] = _slope_clt(dec, x, 'ex5')
    out['slopes'] = pd.DataFrame(res).T
    def tab(D, key, q=5):
        D = D.dropna(subset=[key,'ex5']).copy(); D = D[np.isfinite(D[key])]
        D['b'] = pd.qcut(D[key], q, labels=False, duplicates='drop')
        r = []
        for k, g in D.groupby('b'):
            t, n, nd = _clt(g, 'ex5')
            r.append({'bin':k,'key_mean':g[key].mean(),'ex5':g['ex5'].mean(),'t':t,'n':n,'days':nd})
        return pd.DataFrame(r)
    out['dec_by_rr28_42'] = tab(dec,'rr28_42')
    out['dec_by_vr28_42'] = tab(dec,'vr28_42')
    out['dec_by_vthin_rec'] = tab(dec,'vthin_rec')
    out['all_by_rng1'] = tab(G,'rng1')
    # calm vs panic declines (range ratio median split): slope on ret28
    d2 = dec.dropna(subset=['rr28_42'])
    med = d2.rr28_42.median()
    r = {}
    for lab, g in [('calm',d2[d2.rr28_42<med]),('panic',d2[d2.rr28_42>=med])]:
        s = _slope_clt(g,'ret28','ex5'); t,n,nd = _clt(g,'ex5'); s.update({'ex5':g.ex5.mean(),'t_mean':t}); r[lab]=s
    out['dec_calm_panic'] = pd.DataFrame(r).T
    # mid-decline band (-28%..-12%) by year and window count
    mid = dec[(dec.ret28>-0.30)&(dec.ret28<-0.12)]
    r=[]
    for k,g in mid.groupby('yr'):
        t,n,nd=_clt(g,'ex5'); r.append({'yr':k,'ex5':g.ex5.mean(),'t':t,'n':n})
    out['mid_decline_by_year']=pd.DataFrame(r)
    deep = dec[dec.ret28<=-0.30]
    t,n,nd=_clt(deep,'ex5'); out['deep_decline']=pd.DataFrame([{'ex5':deep.ex5.mean(),'t':t,'n':n,'days':nd}])
    # book largest day gains/losses
    dd=[]
    for coin,wins in data['days'].items():
        for w,d in wins.items():
            d=d.copy(); d['coin']=coin; dd.append(d)
    D=pd.concat(dd).dropna(subset=['book_return'])
    D=D[D.book_return!=0]
    q=D.book_return.quantile([0.05,0.95])
    out['book_tails']=pd.DataFrame({'n_low':[(D.book_return<=q[0.05]).sum()],'sum_low':[D.book_return[D.book_return<=q[0.05]].sum()],
        'n_high':[(D.book_return>=q[0.95]).sum()],'sum_high':[D.book_return[D.book_return>=q[0.95]].sum()],'sum_all':[D.book_return.sum()],
        'coinret_on_low':[D.coin_return[D.book_return<=q[0.05]].mean()],'coinret_on_high':[D.coin_return[D.book_return>=q[0.95]].mean()]})
    return out
