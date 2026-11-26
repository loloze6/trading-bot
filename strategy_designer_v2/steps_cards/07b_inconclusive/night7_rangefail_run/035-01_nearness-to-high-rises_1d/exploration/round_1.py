import numpy as np, pandas as pd

def _clus_slope(x, y, g):
    x = np.asarray(x, float); y = np.asarray(y, float); g = np.asarray(g)
    m = ~(np.isnan(x) | np.isnan(y))
    x, y, g = x[m], y[m], g[m]
    n = len(x)
    if n < 30: return (np.nan, np.nan, n)
    X = np.column_stack([np.ones(n), x])
    XtX = np.linalg.inv(X.T @ X)
    b = XtX @ X.T @ y
    e = y - X @ b
    df = pd.DataFrame({'g': g, 's0': e, 's1': e * x}).groupby('g').sum()
    S = df[['s0', 's1']].values
    V = XtX @ (S.T @ S) @ XtX
    return (b[1], b[1] / np.sqrt(V[1, 1]), n)

def explore(data):
    bars = data['bars']
    rows = []
    for coin, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float)
            r = c.pct_change()
            hi = c.shift(1).rolling(20).max()
            sd = r.rolling(20).std()
            dist = (c - hi) / hi / sd
            ret60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            day = pd.to_datetime(b['timestamp']).dt.floor('D')
            for h in [1, 3, 5, 10, 20]:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    if np.isnan(fwd.iloc[i]): continue
                    rows.append((coin, w, h, day.iloc[i], b['forecast'].iloc[i], dist.iloc[i],
                                 ret60.iloc[i], vol30.iloc[i], fwd.iloc[i]))
    D = pd.DataFrame(rows, columns=['coin', 'w', 'h', 'day', 'f', 'dist', 'r60', 'v30', 'fwd'])
    D['drift'] = D.groupby(['coin', 'h'])['fwd'].transform('mean')
    D['ex'] = D['fwd'] - D['drift']
    out = {}
    hz = []
    for h in [1, 3, 5, 10, 20]:
        d = D[D.h == h]
        s, t, n = _clus_slope(d.f, d.ex, d.day)
        s2, t2, n2 = _clus_slope(d.dist, d.ex, d.day)
        hz.append((h, s, t, n, s2, t2))
    out['by_horizon (forecast slope, raw dist slope)'] = pd.DataFrame(hz, columns=['h', 'slope_f', 't_f', 'n', 'slope_dist', 't_dist'])
    d = D[D.h == 5].copy()
    d['trend'] = np.where(d.r60 > .1, 'rising', np.where(d.r60 < -.1, 'falling', np.where(d.r60.isna(), 'na', 'choppy')))
    d['agit'] = np.where(d.v30 > d.groupby('coin')['v30'].transform('median'), 'agit', 'calm')
    res = []
    for k, g in d.groupby('trend'):
        s, t, n = _clus_slope(g.f, g.ex, g.day); res.append(('trend', k, s, t, n, g.ex.mean()))
    for k, g in d.groupby('agit'):
        s, t, n = _clus_slope(g.f, g.ex, g.day); res.append(('agit', k, s, t, n, g.ex.mean()))
    for k, g in d.groupby('w'):
        s, t, n = _clus_slope(g.f, g.ex, g.day); res.append(('win', k, s, t, n, g.ex.mean()))
    for k, g in d.groupby('coin'):
        s, t, n = _clus_slope(g.f, g.ex, g.day); res.append(('coin', k, s, t, n, g.ex.mean()))
    out['h5 subsets'] = pd.DataFrame(res, columns=['by', 'grp', 'slope', 't', 'n', 'mean_ex'])
    d['fq'] = pd.qcut(d.f, 5, labels=False, duplicates='drop')
    q = d.groupby('fq').agg(n=('ex', 'size'), f_mean=('f', 'mean'), dist_mean=('dist', 'mean'), ex_mean=('ex', 'mean'), ex_sd=('ex', 'std'))
    q['t'] = q.ex_mean / (q.ex_sd / np.sqrt(q.n))
    out['h5 forecast quintiles'] = q
    d['dq'] = pd.qcut(d.dist, 5, labels=False, duplicates='drop')
    q2 = d.groupby('dq').agg(n=('ex', 'size'), dist_mean=('dist', 'mean'), ex_mean=('ex', 'mean'), ex_sd=('ex', 'std'))
    q2['t'] = q2.ex_mean / (q2.ex_sd / np.sqrt(q2.n))
    out['h5 raw distance quintiles'] = q2
    return out
