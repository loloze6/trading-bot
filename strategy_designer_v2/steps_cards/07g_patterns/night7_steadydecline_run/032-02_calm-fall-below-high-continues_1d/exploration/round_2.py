import numpy as np, pandas as pd

def _ct(x, d):
    x = np.asarray(x, float); d = np.asarray(d)
    m = np.isfinite(x); x = x[m]; d = d[m]
    if len(x) < 5: return (np.nan, np.nan, len(x))
    mu = x.mean(); s = pd.Series(x - mu).groupby(d).sum()
    se = np.sqrt((s**2).sum()) / len(x)
    return (mu, mu/se if se > 0 else np.nan, len(x))

def _slope(x, y, d):
    x = np.asarray(x, float); y = np.asarray(y, float); d = np.asarray(d)
    m = np.isfinite(x) & np.isfinite(y); x = x[m]; y = y[m]; d = d[m]
    n = len(x)
    if n < 20: return (np.nan, np.nan, n)
    xc = x - x.mean(); b = (xc*(y - y.mean())).sum() / (xc**2).sum()
    e = (y - y.mean()) - b*xc
    s = pd.Series(xc*e).groupby(d).sum()
    G = s.shape[0]
    v = (s**2).sum() / (xc**2).sum()**2 * G/(G-1)*(n-1)/(n-2)
    return (round(b, 5), round(b/np.sqrt(v), 2), n)

def _summ(df, val, by):
    rows = []
    for k, g in df.groupby(by, observed=True):
        mu, t, n = _ct(g[val], g['day'])
        rows.append({'group': str(k), 'mean': round(mu, 5), 't': round(t, 2), 'n': n, 'days': g['day'].nunique()})
    return pd.DataFrame(rows)

def explore(data):
    H = 3
    recs = []
    for coin, wins in data['bars'].items():
        allg = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values; n = len(b)
            cs = pd.Series(c)
            fwd = np.full(n, np.nan); fwd[:n-H] = c[H:] / c[:n-H] - 1
            f1 = np.full(n, np.nan); f1[:-1] = c[1:] / c[:-1] - 1
            r1 = cs.pct_change()
            ts = pd.to_datetime(b['timestamp'])
            d = pd.DataFrame({'coin': coin, 'win': w, 'pos': np.arange(n), 'fwd': fwd, 'f1': f1,
                              'r1': r1.values,
                              'r3': (cs/cs.shift(3)-1).values, 'r7': (cs/cs.shift(7)-1).values,
                              'r14': (cs/cs.shift(14)-1).values, 'r60': (cs/cs.shift(60)-1).values,
                              'depth': (cs/cs.rolling(30, min_periods=30).max()-1).values,
                              'vol30': r1.rolling(30, min_periods=30).std().values,
                              'regime': b['regime'].values,
                              'day': ts.dt.floor('D').values, 'year': ts.dt.year.values})
            allg.append(d)
        cd = pd.concat(allg)
        grid = cd[cd['pos'] % H == 0]
        cd['ufwd'] = cd['fwd'] - grid['fwd'].mean()
        cd['u1'] = cd['f1'] - cd['f1'].mean()
        cd['r7z'] = cd['r7'] / (cd['vol30']*np.sqrt(7))
        recs.append(cd)
    D = pd.concat(recs)
    D['fc'] = D['regime'] == 'unknown'
    D['tr'] = np.where(D.r60 > 0.1, 'rising', np.where(D.r60 < -0.1, 'falling', 'choppy'))
    D.loc[D.r60.isna(), 'tr'] = np.nan
    G = D[D.pos % H == 0].copy()
    out = {}
    rows = []
    for lab, sub in [('falling calm', G[G.fc]), ('falling non-calm', G[(~G.fc) & (G.tr == 'falling')]),
                     ('choppy', G[G.tr == 'choppy']), ('rising', G[G.tr == 'rising']), ('all', G)]:
        for v in ['r3', 'r7', 'r14', 'r7z', 'depth']:
            b, t, n = _slope(sub[v], sub['ufwd'], sub['day'])
            rows.append({'set': lab, 'x': v, 'slope': b, 't': t, 'n': n})
    out['3d unusual on past return, by profile (slope>0 = continuation)'] = pd.DataFrame(rows)
    fc = G[G.fc].copy()
    rows = []
    for y, g in fc.groupby('year'):
        b, t, n = _slope(g['r7'], g['ufwd'], g['day']); rows.append({'year': y, 'slope r7': b, 't': t, 'n': n})
    for cn, g in fc.groupby('coin'):
        b, t, n = _slope(g['r7'], g['ufwd'], g['day']); rows.append({'year': cn, 'slope r7': b, 't': t, 'n': n})
    out['falling calm r7 slope by year and coin'] = pd.DataFrame(rows)
    fl = G[G.tr == 'falling'].copy()
    fl['q'] = pd.qcut(fl['r7'], 5, labels=False)
    out['falling (any agitation): ufwd by r7 quintile'] = _summ(fl, 'ufwd', 'q')
    # next-day after big 1-day falls by trend
    rows = []
    for lab, sub in [('falling calm', D[D.fc]), ('falling', D[D.tr == 'falling']), ('choppy', D[D.tr == 'choppy']),
                     ('rising', D[D.tr == 'rising']), ('all', D)]:
        b, t, n = _slope(sub['r1'], sub['u1'], sub['day']); rows.append({'set': lab, 'slope 1d->next1d': b, 't': t, 'n': n})
    out['next-day on today return'] = pd.DataFrame(rows)
    return out
