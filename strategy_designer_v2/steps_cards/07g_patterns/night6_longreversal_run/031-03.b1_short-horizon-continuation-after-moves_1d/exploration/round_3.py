import numpy as np, pandas as pd

def _ct(s, col, day='day'):
    s = s.dropna(subset=[col])
    m = s[col].mean()
    dev = (s[col] - m).groupby(s[day]).sum()
    se = np.sqrt((dev ** 2).sum()) / len(s)
    return m, (m / se if se > 0 else np.nan), len(s), s[day].nunique()

def _slope(s, x, y, day='day'):
    s = s.dropna(subset=[x, y])
    X = s[x] - s[x].mean()
    b = (X * s[y]).sum() / (X ** 2).sum()
    res = s[y] - s[y].mean() - b * X
    g = (X * res).groupby(s[day]).sum()
    se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
    return b, b / se, len(s), s[day].nunique()

def explore(data):
    out = {}
    rows = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df['close']; r1 = c.pct_change()
            sd = r1.rolling(60, min_periods=20).std()
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            z20 = ret20 / (sd * np.sqrt(20))
            z60 = ret60 / (sd * np.sqrt(60))
            ts = pd.to_datetime(df['timestamp'])
            for h in (10, 20):
                idx = np.arange(0, len(c) - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                for i, f in zip(idx, fwd):
                    rows.append(dict(coin=coin, w=int(w[1:]), h=h, fwd=f, z20=z20.iloc[i], z60=z60.iloc[i],
                                     sd=sd.iloc[i], day=ts.iloc[i].normalize().value, yr=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    g['drift'] = g.groupby(['coin', 'h'])['fwd'].transform('mean')
    g['usual'] = g.groupby(['coin', 'h'])['fwd'].transform('std')
    g['ex'] = g['fwd'] - g['drift']
    g['exz'] = g['ex'] / g['usual']
    g['a20'] = g['z20'].abs().clip(upper=5)
    g['a60'] = g['z60'].abs().clip(upper=5)
    res = []
    for h in (10, 20):
        s = g[g.h == h]
        for x in ('z20', 'a20', 'z60', 'a60'):
            b, t, n, nd = _slope(s.assign(xc=s[x].clip(-5, 5)), 'xc', 'exz')
            res.append(dict(h=h, x=x, slope=b, t=t, n=n, days=nd))
    out['slopes exz on z / |z| (clustered)'] = pd.DataFrame(res).round(4)
    # |z20| buckets fwd10, clustered, by half
    s = g[g.h == 10].dropna(subset=['a20']).copy()
    s['ab'] = pd.cut(s['a20'], [0, 0.5, 1, 1.5, 2, 5.01])
    rr = []
    for b, ss in s.groupby('ab', observed=True):
        m, t, n, nd = _ct(ss, 'exz'); rr.append(dict(b=str(b), n=n, days=nd, exz=m, t=t, ex_pct=ss['ex'].mean() * 100))
    out['|z20| bucket -> fwd10 exz'] = pd.DataFrame(rr).round(3)
    s['half'] = np.where(s['w'] <= 12, 'w1-12', 'w13-24')
    rr = []
    for k, ss in s.groupby('half'):
        b, t, n, nd = _slope(ss, 'a20', 'exz'); rr.append(dict(half=k, slope=b, t=t, n=n))
    for k, ss in s.groupby('coin'):
        b, t, n, nd = _slope(ss, 'a20', 'exz'); rr.append(dict(half=k, slope=b, t=t, n=n))
    out['|z20| slope by half and coin'] = pd.DataFrame(rr).round(4)
    # sign split: up extremes vs down extremes, fwd10
    rr = []
    for side, ss in [('up', s[s.z20 > 0]), ('down', s[s.z20 < 0])]:
        b, t, n, nd = _slope(ss, 'a20', 'exz'); rr.append(dict(side=side, slope=b, t=t, n=n))
    out['|z20| slope by side'] = pd.DataFrame(rr).round(4)
    # book: long vs short days share of gain
    d = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            a = df['postRebalance_current_allocation']
            r = df['close'].pct_change().shift(-1)
            d.append(pd.DataFrame(dict(a=a, r=r)))
    d = pd.concat(d).dropna()
    d['gain'] = d['a'] * d['r']
    d['side'] = np.where(d['a'] > 0, 'long', np.where(d['a'] < 0, 'short', 'flat'))
    out['bar gain by side'] = d.groupby('side')['gain'].agg(['mean', 'count', 'sum']).round(5)
    return out
