import numpy as np, pandas as pd

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def _slope_t(df, xcol, ycol, day='day'):
    d = df.dropna(subset=[xcol, ycol])
    if len(d) < 20: return pd.Series({'n': len(d), 'days': np.nan, 'slope': np.nan, 't': np.nan})
    x = d[xcol] - d[xcol].mean(); y = d[ycol]
    b = (x*y).sum() / (x*x).sum()
    a = y.mean() - b*d[xcol].mean()
    e = y - a - b*d[xcol]
    s = (x*e).groupby(d[day]).sum()
    G = len(s)
    var = (s**2).sum() / (x*x).sum()**2 * G/(G-1)
    return pd.Series({'n': len(d), 'days': G, 'slope': b, 't': b/np.sqrt(var)})

def explore(data):
    rows = []
    for coin, wins in data['bars'].items():
        for w, b in wins.items():
            b = b.sort_values('timestamp').reset_index(drop=True)
            c = b['close']; r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            d = pd.DataFrame({'coin': coin, 'win': w, 'ts': pd.to_datetime(b['timestamp'])})
            d['r'] = r; d['z'] = r / sd.shift(1)
            d['f1'] = c.shift(-1)/c - 1
            d['regime'] = b['regime'].values
            rng = (b['high'] - b['low']).replace(0, np.nan)
            d['clv'] = (c - b['low']) / rng
            d['vol_c'] = np.log(b['volume'] / b['volume'].rolling(20, min_periods=10).mean().shift(1))
            d['rngz'] = (rng / c) / sd
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D['ex1'] = D['f1'] - D['coin'].map(D.groupby('coin')['f1'].mean())
    D['day'] = D['ts'].dt.floor('D')
    D['yr'] = D['ts'].dt.year
    D['wn'] = D['win'].str[1:].astype(int)
    D['half'] = np.where(D['wn'] <= 12, 'w1-12', 'w13-24')
    D['clvc'] = D['clv'] - 0.5
    hi = D[D['regime'] == 'mean_reversion'].copy()
    ot = D[D['regime'] != 'mean_reversion'].copy()
    res = {}
    # clv, controlling for z: residual of ex1 after z within hi
    def resid(df):
        d = df.dropna(subset=['z', 'ex1', 'clv']).copy()
        X = np.column_stack([np.ones(len(d)), d['z'].clip(-5, 5)])
        beta = np.linalg.lstsq(X, d['ex1'].values, rcond=None)[0]
        d['rex'] = d['ex1'] - X @ beta
        return d
    hr = resid(hi)
    res['hi: clv slope on ex1 raw / after z'] = pd.DataFrame({'raw': _slope_t(hi, 'clv', 'ex1'), 'after z': _slope_t(hr, 'clv', 'rex')}).T
    hr['zs'] = np.where(hr['z'] < 0, 'down', 'up')
    res['hi: clv slope after z, by side'] = hr.groupby('zs').apply(lambda g: _slope_t(g, 'clv', 'rex'))
    res['hi: clv slope after z, by half'] = hr.groupby('half').apply(lambda g: _slope_t(g, 'clv', 'rex'))
    res['hi: clv slope after z, by coin'] = hr.groupby('coin').apply(lambda g: _slope_t(g, 'clv', 'rex'))
    orr = resid(ot)
    res['other: clv slope after z'] = _slope_t(orr, 'clv', 'rex').to_frame().T
    # up-day reversal in hi vol
    up = hi[hi['z'] > 0]
    res['hi up days: slope ex1 on z'] = pd.DataFrame({'all': _slope_t(up, 'z', 'ex1'),
        'w1-12': _slope_t(up[up['half']=='w1-12'], 'z', 'ex1'), 'w13-24': _slope_t(up[up['half']=='w13-24'], 'z', 'ex1')}).T
    res['hi up days by z tercile'] = up.dropna(subset=['ex1']).assign(q=pd.qcut(up['z'], 3, labels=False)).groupby('q')['ex1'].agg(['size', 'mean', _t])
    # volume on falls in hi
    dn = hi[hi['z'] < 0]
    dr = resid(dn)
    res['hi down: vol_c slope raw / after z'] = pd.DataFrame({'raw': _slope_t(dn, 'vol_c', 'ex1'), 'after z': _slope_t(dr, 'vol_c', 'rex'),
        'after z w1-12': _slope_t(dr[dr['half']=='w1-12'], 'vol_c', 'rex'), 'after z w13-24': _slope_t(dr[dr['half']=='w13-24'], 'vol_c', 'rex')}).T
    res['hi down: z slope by half'] = dn.groupby('half').apply(lambda g: _slope_t(g, 'z', 'ex1'))
    # range size
    res['hi: rngz slope after z'] = _slope_t(hr, 'rngz', 'rex').to_frame().T
    res['hi: clv quintile x side ex1'] = hi.dropna(subset=['ex1', 'clv']).assign(q=pd.qcut(hi['clv'], 5, labels=False), s=np.where(hi['z'] < 0, 'down', 'up')).groupby(['s', 'q'])['ex1'].agg(['size', 'mean', _t])
    return res
