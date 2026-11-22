def explore(data):
    import numpy as np, pandas as pd
    out = {}
    r6, r36, rb = [], [], []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float); h = b['high'].astype(float); l = b['low'].astype(float)
            n = len(b)
            if n < 400: continue
            ts = pd.to_datetime(b['timestamp'])
            yr = ts.dt.year
            r1 = c.pct_change()
            ret6 = c / c.shift(6) - 1
            rng6 = h.rolling(6).max() / l.rolling(6).min() - 1
            z6 = ret6 / ret6.rolling(180).std()
            rm = rng6 / rng6.rolling(180).mean()
            for i in range(0, n - 6, 6):
                r6.append(dict(coin=coin, yr=yr.iloc[i], z6=z6.iloc[i], rm=rm.iloc[i], fwd=c.iloc[i+6]/c.iloc[i]-1))
            for i in range(0, n - 36, 36):
                r36.append(dict(coin=coin, yr=yr.iloc[i], z6=z6.iloc[i], rm=rm.iloc[i], fwd=c.iloc[i+36]/c.iloc[i]-1))
            rb.append(pd.DataFrame(dict(coin=coin, yr=yr, hour=ts.dt.hour, wd=ts.dt.weekday, r=r1.shift(-1))))
    d6 = pd.DataFrame(r6).dropna(); d36 = pd.DataFrame(r36).dropna(); db = pd.concat(rb).dropna()
    for d in (d6, d36):
        d['ab'] = d['fwd'] - d.groupby('coin')['fwd'].transform('mean')
    db['ab'] = db['r'] - db.groupby('coin')['r'].transform('mean')
    def summ(g):
        x = g['ab']
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    # 24h reversal after down days, by coin and year (bottom decile of z6)
    d6['zd'] = pd.qcut(d6['z6'], 10, labels=False)
    low = d6[d6['zd'] == 0]
    out['24h abn after bottom-decile z, by coin'] = low.groupby('coin').apply(summ)
    out['24h abn after bottom-decile z, by year'] = low.groupby('yr').apply(summ)
    out['24h abn by z decile x range-multiple tercile (mean)'] = d6.assign(rt=pd.qcut(d6['rm'], 3, labels=['lo','mid','hi'])).groupby(['zd','rt'])['ab'].mean().unstack()
    # 6d on a non-overlapping 36-bar grid
    d36['zd'] = pd.qcut(d36['z6'], 10, labels=False)
    out['6d abn (36-grid) by z decile'] = d36.groupby('zd').apply(summ)
    d36['rq'] = pd.qcut(d36['rm'], 5, labels=False)
    out['6d abn (36-grid) by range quintile'] = d36.groupby('rq').apply(summ)
    d36['dir'] = np.where(d36['z6'] < 0, 'down', 'up')
    out['6d abn (36-grid) by range quintile x dir'] = d36.groupby(['rq','dir']).apply(summ).unstack()
    hi = d36[d36['rq'] == 4]
    out['6d abn top range quintile by coin'] = hi.groupby('coin').apply(summ)
    out['6d abn top range quintile by year'] = hi.groupby('yr').apply(summ)
    # hour effects robustness
    out['abn 16h bar by coin'] = db[db.hour == 16].groupby('coin').apply(summ)
    out['abn 20h bar by coin'] = db[db.hour == 20].groupby('coin').apply(summ)
    out['abn 16h bar by year'] = db[db.hour == 16].groupby('yr').apply(summ)
    out['abn 20h bar by year'] = db[db.hour == 20].groupby('yr').apply(summ)
    out['abn friday by year'] = db[db.wd == 4].groupby('yr').apply(summ)
    return out
