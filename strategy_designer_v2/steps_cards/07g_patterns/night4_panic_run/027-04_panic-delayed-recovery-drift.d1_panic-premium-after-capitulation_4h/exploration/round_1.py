def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    fc = 'debug_info.components.capitulation_panic.last_history_value'
    rows78, rows6, rowsbar, rowspanic = [], [], [], []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float); h = b['high'].astype(float); l = b['low'].astype(float)
            n = len(b)
            if n < 700: continue
            r1 = c.pct_change()
            ret6 = c / c.shift(6) - 1
            rng6 = (h.rolling(6).max() / l.rolling(6).min() - 1)
            sd6 = ret6.rolling(180).std()
            rngm = rng6.rolling(180).mean()
            z6 = ret6 / sd6
            rm = rng6 / rngm
            prior = c / c.shift(540) - 1
            vol30 = r1.rolling(180).std()
            ts = pd.to_datetime(b['timestamp'])
            # 78-bar grid
            for i in range(0, n - 78, 78):
                rows78.append(dict(coin=coin, w=w, f=b['forecast'].iloc[i], raw=b[fc].iloc[i] if fc in b else np.nan,
                                   z6=z6.iloc[i], rm=rm.iloc[i], prior=prior.iloc[i], vol=vol30.iloc[i],
                                   fwd=c.iloc[i+78]/c.iloc[i]-1, fwd_lag=(c.iloc[min(i+84,n-1)]/c.iloc[i+6]-1) if i+84<n else np.nan))
            for i in range(0, n - 6, 6):
                rows6.append(dict(coin=coin, w=w, z6=z6.iloc[i], rm=rm.iloc[i], vol=vol30.iloc[i],
                                  fwd6=c.iloc[i+6]/c.iloc[i]-1, fwd36=(c.iloc[i+36]/c.iloc[i]-1) if i+36<n else np.nan))
            rowsbar.append(pd.DataFrame(dict(coin=coin, hour=ts.dt.hour, wd=ts.dt.weekday, r=r1.shift(-1),
                                             alloc=b['postRebalance_current_allocation'])))
    d78 = pd.DataFrame(rows78); d6 = pd.DataFrame(rows6); db = pd.concat(rowsbar)
    drift = d78.groupby('coin')['fwd'].transform('mean')
    d78['ab'] = d78['fwd'] - drift
    d6['ab6'] = d6['fwd6'] - d6.groupby('coin')['fwd6'].transform('mean')
    d6['ab36'] = d6['fwd36'] - d6.groupby('coin')['fwd36'].transform('mean')
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    # 1 forecast bins
    d78['fbin'] = pd.cut(d78['f'], [-0.1, 0.001, 1, 5, 21], labels=['0','0-1','1-5','5+'])
    out['78bar abn by forecast bin'] = d78.groupby('fbin').apply(summ, 'ab')
    # 2 panic (z6 low) by prior sign; graded
    d78['panicq'] = pd.qcut(d78['z6'], 5, labels=['q1low','q2','q3','q4','q5high'])
    d78['priorsign'] = np.where(d78['prior'] < 0, 'neg', 'pos')
    out['78bar abn by 24h z quintile x prior sign'] = d78.groupby(['panicq','priorsign']).apply(summ, 'ab').unstack()
    out['78bar abn by range-multiple quintile'] = d78.groupby(pd.qcut(d78['rm'], 5)).apply(summ, 'ab')
    out['78bar abn by prior 90d quintile'] = d78.groupby(pd.qcut(d78['prior'], 5)).apply(summ, 'ab')
    out['78bar abn by vol quintile'] = d78.groupby(pd.qcut(d78['vol'], 5)).apply(summ, 'ab')
    # 3 6-bar grid: next 24h and 6d by z6 decile
    d6['zd'] = pd.qcut(d6['z6'], 10, labels=False)
    out['24h abn by past-24h z decile'] = d6.groupby('zd').apply(summ, 'ab6')
    out['6d abn by past-24h z decile'] = d6.groupby('zd').apply(summ, 'ab36')
    out['6d abn by range multiple quintile'] = d6.groupby(pd.qcut(d6['rm'], 5)).apply(summ, 'ab36')
    # 4 hour/weekday
    db['ab'] = db['r'] - db.groupby('coin')['r'].transform('mean')
    out['4h abn by hour'] = db.groupby('hour').apply(summ, 'ab')
    out['4h abn by weekday'] = db.groupby('wd').apply(summ, 'ab')
    out['share bars in position'] = float((db['alloc'].abs() > 1e-6).mean())
    return out
