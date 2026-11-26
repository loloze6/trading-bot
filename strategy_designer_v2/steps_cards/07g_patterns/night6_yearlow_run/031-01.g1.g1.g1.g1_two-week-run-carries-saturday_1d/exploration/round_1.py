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
            lo60 = c.rolling(60, min_periods=40).min()
            hi60 = c.rolling(60, min_periods=40).max()
            out = pd.DataFrame({
                'coin': coin, 'win': w, 'date': ts.dt.normalize(),
                'wd': ts.dt.dayofweek, 'pos': np.arange(len(d)),
                'r': r, 'vol': vol,
                'nxt': c.shift(-1) / c - 1,
                'nxt5': c.shift(-5) / c - 1,
                's1': r / vol,
                's3': (c / c.shift(3) - 1) / (vol * np.sqrt(3)),
                's14': (c / c.shift(14) - 1) / (vol * np.sqrt(14)),
                'dlow': np.log(c / lo60) / vol,
                'dhigh': np.log(hi60 / c) / vol,
                'alloc': d['postRebalance_current_allocation'].astype(float),
                'fc': d['forecast'].astype(float),
            })
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    cm = A.groupby('coin')['nxt'].mean()
    A['ex'] = A['nxt'] - A['coin'].map(cm)
    cm5 = A[A.pos % 5 == 0].groupby('coin')['nxt5'].mean()
    A['ex5'] = A['nxt5'] - A['coin'].map(cm5)
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
        s = df[[y, 'date']].dropna().groupby('date')[y].sum()
        n = df[y].notna().sum()
        m = df[y].mean()
        dev = df[[y, 'date']].dropna()
        dd = (dev[y] - m).groupby(dev['date']).sum()
        se = np.sqrt((dd ** 2).sum()) / n
        return m, m / se, n, len(dd)

    res = {}
    wdrows = []
    for wd in range(7):
        sub = A[A.wd == wd]
        b14 = cslope(sub, 's14', 'ex'); b1 = cslope(sub, 's1', 'ex'); b3 = cslope(sub, 's3', 'ex')
        m = cmean(sub, 'ex')
        wdrows.append({'wd_of_signal': wd, 'slope_s14': b14[0], 't_s14': b14[1], 'slope_s3': b3[0], 't_s3': b3[1],
                       'slope_s1': b1[0], 't_s1': b1[1], 'mean_next_ex': m[0], 't_mean': m[1], 'n': b14[2], 'days': b14[3]})
    res['by signal weekday: next-day excess on s14/s3/s1'] = pd.DataFrame(wdrows).round(5)

    allrow = {}
    for x in ['s1', 's3', 's14', 'dlow', 'dhigh']:
        b = cslope(A, x, 'ex'); allrow[x + ' next1'] = b
        g = A[A.pos % 5 == 0]
        b5 = cslope(g, x, 'ex5'); allrow[x + ' next5grid'] = b5
    res['all days slopes (b,t,n,days)'] = pd.DataFrame(allrow, index=['b', 't', 'n', 'days']).T.round(5)

    A['volt'] = pd.qcut(A['volrel'], 3, labels=['lowvol', 'midvol', 'highvol'])
    vr = []
    for v in ['lowvol', 'midvol', 'highvol']:
        for wdset, nm in [([4], 'fri'), ([0, 1, 2, 3, 5, 6], 'otherdays')]:
            sub = A[(A.volt == v) & A.wd.isin(wdset)]
            b = cslope(sub, 's14', 'ex'); m = cmean(sub, 'ex')
            vr.append({'vol': v, 'days': nm, 'slope': b[0], 't': b[1], 'n': b[2], 'absnext': sub['nxt'].abs().mean(), 'mean_ex': m[0], 't_mean': m[1]})
    res['s14 slope by vol tercile'] = pd.DataFrame(vr).round(5)

    q = []
    A['s1q'] = A.groupby('coin')['s1'].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates='drop'))
    for k in range(5):
        m = cmean(A[A.s1q == k], 'ex'); q.append({'s1_quintile': k, 'mean_ex': m[0], 't': m[1], 'n': m[2]})
    A['dlq'] = A.groupby('coin')['dlow'].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates='drop'))
    g = A[A.pos % 5 == 0]
    for k in range(5):
        m = cmean(g[g.dlq == k], 'ex5'); q.append({'dlow_quintile_next5': k, 'mean_ex': m[0], 't': m[1], 'n': m[2]})
    res['quintiles'] = pd.DataFrame(q).round(5)

    # book
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x['coin'] = coin; x['win'] = w; D.append(x)
    D = pd.concat(D)
    D['date'] = pd.to_datetime(D['day'], utc=True)
    bk = D.groupby('date')['book_return'].mean().dropna()
    bkd = pd.DataFrame({'r': bk, 'wd': bk.index.dayofweek})
    res['book by weekday'] = bkd.groupby('wd')['r'].agg(['mean', 'std', 'min', 'max', 'count']).round(5)
    fr = A[(A.wd == 4) & (A.alloc.abs() > 0)].copy()
    fr['gain'] = fr.alloc * fr.nxt
    fr['side'] = np.where(fr.alloc > 0, 'long', 'short')
    fr['s14q'] = pd.qcut(fr['fc'], 5, labels=False, duplicates='drop')
    res['friday positions by side'] = fr.groupby('side')['gain'].agg(['mean', 'std', 'count', 'sum']).round(5)
    res['friday gain by forecast quintile'] = fr.groupby('s14q').agg(fc=('fc', 'mean'), gain=('gain', 'mean'), ex=('ex', 'mean'), n=('gain', 'count'), absalloc=('alloc', lambda s: s.abs().mean())).round(5)
    sat = bkd[bkd.wd == 5]['r']
    res['saturday book: share of total, worst5 mean, best5 mean'] = pd.Series({'sat_sum': sat.sum(), 'all_sum': bkd.r.sum(), 'worst5': sat.nsmallest(5).mean(), 'best5': sat.nlargest(5).mean(), 'nonsat_abs_mean': bkd[bkd.wd != 5].r.abs().mean()}).round(5)
    return res
