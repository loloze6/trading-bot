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
            v30 = r.rolling(30).std()
            vpct = v30.rolling(min(365, len(b)), min_periods=60).apply(lambda a: (a <= a[-1]).mean(), raw=True)
            day = pd.to_datetime(b['timestamp']).dt.floor('D')
            for h in [3, 5]:
                fwd = c.shift(-h) / c - 1
                for off in range(h):
                    for i in range(off, len(b), h):
                        if np.isnan(fwd.iloc[i]): continue
                        rows.append((coin, w, h, off, day.iloc[i], b['forecast'].iloc[i], dist.iloc[i],
                                     ret60.iloc[i], vpct.iloc[i], fwd.iloc[i]))
    D = pd.DataFrame(rows, columns=['coin', 'w', 'h', 'off', 'day', 'f', 'dist', 'r60', 'vp', 'fwd'])
    D['drift'] = D[D.off == 0].groupby(['coin', 'h'])['fwd'].mean().reindex(pd.MultiIndex.from_arrays([D.coin, D.h])).values
    D['ex'] = D['fwd'] - D['drift']
    out = {}
    res = []
    for (h, off), g in D.groupby(['h', 'off']):
        s, t, n = _clus_slope(g.f, g.ex, g.day)
        lo, hi_ = g.ex.quantile([.01, .99])
        s2, t2, _ = _clus_slope(g.f, g.ex.clip(lo, hi_), g.day)
        res.append((h, off, s, t, n, s2, t2))
    out['grid offsets (slope, t, winsorised slope, t)'] = pd.DataFrame(res, columns=['h', 'off', 's', 't', 'n', 's_win', 't_win'])
    d = D[(D.h == 5) & (D.off == 0)].copy()
    d['trend'] = np.where(d.r60 > .1, 'rising', np.where(d.r60 < -.1, 'falling', np.where(d.r60.isna(), 'na', 'choppy')))
    d['agit'] = np.where(d.vp.isna(), 'na', np.where(d.vp > .5, 'agit', 'calm'))
    res = []
    for k, g in d.groupby(['trend', 'agit']):
        s, t, n = _clus_slope(g.f, g.ex, g.day); res.append((str(k), s, t, n, g.ex.mean()))
    for k, g in d.groupby('agit'):
        s, t, n = _clus_slope(g.f, g.ex, g.day); res.append((k, s, t, n, g.ex.mean()))
    out['h5 profile cells'] = pd.DataFrame(res, columns=['grp', 'slope', 't', 'n', 'mean_ex'])
    d['above'] = d.dist >= 0
    res = []
    for k, g in d.groupby('above'):
        s, t, n = _clus_slope(g.dist, g.ex, g.day)
        res.append((str(k), s, t, n, g.ex.mean(), g.ex.median()))
    out['h5 at/above high vs below (raw dist)'] = pd.DataFrame(res, columns=['above', 'slope', 't', 'n', 'mean', 'median'])
    d['fq'] = pd.qcut(d.f, 5, labels=False, duplicates='drop')
    out['h5 quintile medians'] = d.groupby('fq').ex.agg(['median', 'mean', lambda s: (s > 0).mean()])
    return out
