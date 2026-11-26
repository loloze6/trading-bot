def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.sort_values('timestamp').reset_index(drop=True)
            c = d['close'].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=15).std()
            ts = pd.to_datetime(d['timestamp'], utc=True)
            out = pd.DataFrame({
                'coin': coin, 'win': w, 'date': ts.dt.normalize(), 'yr': ts.dt.year,
                'wd': ts.dt.dayofweek, 'pos': np.arange(len(d)),
                'r': r, 'vol': vol,
                'nxt': c.shift(-1) / c - 1,
                'nxt2': c.shift(-2) / c - 1,
                's1': r / vol,
                's14': (c / c.shift(14) - 1) / (vol * np.sqrt(14)),
                'alloc': d['postRebalance_current_allocation'].astype(float),
            })
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    cm = A.groupby('coin')['nxt'].mean()
    A['ex'] = A['nxt'] - A['coin'].map(cm)
    cm2 = A[A.pos % 2 == 0].groupby('coin')['nxt2'].mean()
    A['ex2'] = A['nxt2'] - A['coin'].map(cm2)
    A['volrel'] = A['vol'] / A.groupby('coin')['vol'].transform('median')

    def cslope(df, x, y):
        df = df[[x, y, 'date']].dropna()
        if len(df) < 30: return (np.nan, np.nan, len(df), 0)
        xm = df[x] - df[x].mean()
        b = (xm * df[y]).sum() / (xm ** 2).sum()
        a = df[y].mean() - b * df[x].mean()
        e = df[y] - a - b * df[x]
        s = (xm * e).groupby(df['date']).sum()
        G = len(s)
        var = (s ** 2).sum() / ((xm ** 2).sum() ** 2) * G / (G - 1)
        return (b, b / np.sqrt(var), len(df), G)

    def cmean(df, y):
        dev = df[[y, 'date']].dropna()
        n = len(dev); m = dev[y].mean()
        dd = (dev[y] - m).groupby(dev['date']).sum()
        se = np.sqrt((dd ** 2).sum()) / n
        return m, m / se, n, len(dd)

    res = {}
    F = A[A.wd == 4].copy()
    F['q'] = F.groupby('coin')['s14'].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates='drop'))
    q = []
    for k in range(5):
        m = cmean(F[F.q == k], 'ex'); q.append({'fri_s14_q': k, 's14': F[F.q == k].s14.mean(), 'mean_ex': m[0], 't': m[1], 'n': m[2]})
    res['friday s14 quintiles -> saturday excess'] = pd.DataFrame(q).round(5)
    sp = {}
    sp['s14>0'] = cslope(F[F.s14 > 0], 's14', 'ex')
    sp['s14<0'] = cslope(F[F.s14 < 0], 's14', 'ex')
    res['friday slope by sign (b,t,n,days)'] = pd.DataFrame(sp, index=['b', 't', 'n', 'days']).T.round(5)
    yr = []
    for y, g in F.groupby('yr'):
        b = cslope(g, 's14', 'ex'); yr.append({'yr': y, 'slope': b[0], 't': b[1], 'n': b[2]})
    res['friday s14 slope by year'] = pd.DataFrame(yr).round(5)
    cr = []
    for co, g in F.groupby('coin'):
        b = cslope(g, 's14', 'ex'); cr.append({'coin': co, 'slope': b[0], 't': b[1], 'n': b[2]})
    res['friday s14 slope by coin'] = pd.DataFrame(cr).round(5)

    # one-day reversal, all days, by year / coin / vol
    yr = []
    for y, g in A.groupby('yr'):
        b = cslope(g, 's1', 'ex'); yr.append({'yr': y, 'slope': b[0], 't': b[1], 'n': b[2]})
    res['s1 reversal by year'] = pd.DataFrame(yr).round(5)
    cr = []
    for co, g in A.groupby('coin'):
        b = cslope(g, 's1', 'ex'); cr.append({'coin': co, 'slope': b[0], 't': b[1], 'n': b[2]})
    res['s1 reversal by coin'] = pd.DataFrame(cr).round(5)
    A['volt'] = pd.qcut(A['volrel'], 3, labels=['low', 'mid', 'high'])
    vr = []
    for v in ['low', 'mid', 'high']:
        g = A[A.volt == v]
        b = cslope(g, 's1', 'ex'); b2 = cslope(g[g.pos % 2 == 0], 's1', 'ex2')
        vr.append({'vol': v, 'slope1': b[0], 't1': b[1], 'slope2grid': b2[0], 't2grid': b2[1], 'n': b[2]})
    res['s1 reversal by vol tercile, 1d and 2d'] = pd.DataFrame(vr).round(5)
    # reversal asymmetry: down days vs up days
    sp = {'s1<0': cslope(A[A.s1 < 0], 's1', 'ex'), 's1>0': cslope(A[A.s1 > 0], 's1', 'ex')}
    res['s1 reversal by sign'] = pd.DataFrame(sp, index=['b', 't', 'n', 'days']).T.round(5)
    # saturday excess by year
    S = A[A.wd == 4]
    yr = []
    for y, g in S.groupby('yr'):
        m = cmean(g, 'ex'); yr.append({'yr': y, 'sat_mean_ex': m[0], 't': m[1], 'n': m[2]})
    res['saturday unconditional excess by year'] = pd.DataFrame(yr).round(5)
    # book worst/best saturdays: prior s14 and s1
    fr = A[(A.wd == 4) & (A.alloc.abs() > 0)].copy()
    fr['gain'] = fr.alloc * fr.nxt
    day = fr.groupby('date').agg(gain=('gain', 'mean'), s14=('s14', 'mean'), s1=('s1', 'mean'), vol=('volrel', 'mean'))
    dq = pd.qcut(day['gain'], 10, labels=False)
    res['book saturday deciles: prior state'] = day.groupby(dq).mean().round(4)
    return res
