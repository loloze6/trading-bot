import numpy as np, pandas as pd

def _t(df, col='ex'):
    d = df.dropna(subset=[col])
    n = len(d)
    if n < 5: return (n, np.nan, np.nan, 0)
    m = d[col].mean()
    s = (d[col]-m).groupby(d['day']).sum()
    se = np.sqrt((s**2).sum())/n
    return (n, m, m/se if se>0 else np.nan, d['day'].nunique())

def _tab(df, by):
    rows = {}
    for k, g in df.groupby(by, observed=True):
        n, m, t, nd = _t(g)
        rows[k] = {'n': n, 'days': nd, 'mean_ex_%': round(100*m,3) if m==m else m, 't': round(t,2) if t==t else t,
                   'mean_fwd_%': round(100*g['fwd'].mean(),3)}
    return pd.DataFrame(rows).T

def explore(data):
    recs = []
    for coin, wins in data['bars'].items():
        cg = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, h, l, o = b['close'], b['high'], b['low'], b['open']
            rng = (h-l)/c
            f = pd.DataFrame({
                'day': pd.to_datetime(b['timestamp']).dt.floor('D'),
                'wd': pd.to_datetime(b['timestamp']).dt.weekday,
                'ret5': c/c.shift(5)-1,
                'ret20': c/c.shift(20)-1,
                'r1': c/c.shift(1)-1,
                'rr': (h-l)/(h-l).rolling(20).mean(),
                'body': (c-o).abs()/(h-l).replace(0,np.nan),
                'cl': (c-l)/(h-l).replace(0,np.nan),
                'vol20': c.pct_change().rolling(20).std(),
                'fwd': c.shift(-3)/c-1,
                'fwd1': c.shift(-1)/c-1,
                'pos': b['postRebalance_current_allocation'],
            })
            f = f.iloc[::3]
            f['coin']=coin; f['w']=w
            cg.append(f)
        cf = pd.concat(cg)
        cf['ex'] = cf['fwd'] - cf['fwd'].mean()
        cf['volq'] = pd.qcut(cf['vol20'].rank(method='first'), 3, labels=['lowvol','mid','highvol'])
        recs.append(cf)
    d = pd.concat(recs).dropna(subset=['fwd','ret5','rr'])
    d['run'] = np.where(d['ret5']>0,'up5','down5')
    d['rrq'] = pd.qcut(d['rr'],5,labels=False)
    d['clq'] = pd.qcut(d['cl'],5,labels=False)
    d['bodyq'] = pd.qcut(d['body'],3,labels=['flat','mid','full'])
    d['r1q'] = pd.qcut(d['r1'],5,labels=False)
    d['ret5q'] = pd.qcut(d['ret5'],5,labels=False)
    d['ret20q'] = pd.qcut(d['ret20'],5,labels=False)
    out = {}
    out['range quintile x run'] = _tab(d, ['run','rrq'])
    wide = d[d['rrq']>=3]
    out['wide days: run x body'] = _tab(wide, ['run','bodyq'])
    out['up5: close-location quintile'] = _tab(d[d.run=='up5'], 'clq')
    out['down5: close-location quintile'] = _tab(d[d.run=='down5'], 'clq')
    out['ret5 quintile'] = _tab(d, 'ret5q')
    out['ret20 quintile'] = _tab(d, 'ret20q')
    out['r1 quintile'] = _tab(d, 'r1q')
    out['vol tercile x run'] = _tab(d, ['volq','run'])
    out['weekday'] = _tab(d, 'wd')
    out['up5 wide: vol tercile'] = _tab(d[(d.run=='up5')&(d.rrq>=3)], 'volq')
    return out
