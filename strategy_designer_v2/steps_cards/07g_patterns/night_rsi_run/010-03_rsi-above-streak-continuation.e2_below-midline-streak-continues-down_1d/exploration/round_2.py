def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []; D = []
    for coin in data['bars']:
        for w, b in data['bars'][coin].items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float)
            d = c.diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100/(1+up/dn)
            side = np.sign(rsi-50)
            run = side.groupby((side != side.shift()).cumsum()).cumcount()+1
            srun = run*side
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z1 = r1/vol20.shift(1)
            fwd7 = c.shift(-7)/c-1
            fwd1 = c.shift(-1)/c-1
            # drawdown from 60-day high
            dd60 = c/c.rolling(60, min_periods=20).max()-1
            ts = pd.to_datetime(b['timestamp'])
            for i in range(0, len(b), 7):
                if pd.isna(fwd7.iloc[i]): continue
                rows.append(dict(coin=coin, w=w, fwd7=fwd7.iloc[i], srun=srun.iloc[i], rsi=rsi.iloc[i],
                                 z1=z1.iloc[i], dd60=dd60.iloc[i], year=ts.iloc[i].year))
            dd = data['days'][coin][w].copy(); dd['coin']=coin; dd['w']=w
            dd['wd'] = pd.to_datetime(dd['day']).dt.dayofweek
            dd['year'] = pd.to_datetime(dd['day']).dt.year
            D.append(dd)
    g = pd.DataFrame(rows)
    g['ex7'] = g['fwd7'] - g.groupby('coin')['fwd7'].transform('mean')
    def summ(grp):
        x = grp['ex7'].dropna()
        return pd.Series({'n': len(x), 'mean': x.mean(), 't': x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    g['srun_b'] = pd.cut(g['srun'], [-200, -30, -14, -1, 0, 14, 30, 200])
    out['coin x signed run'] = g.groupby(['coin','srun_b']).apply(summ)
    long_b = g[g['srun'] <= -30]
    out['long below run (<=-30) by year'] = long_b.groupby('year').apply(summ)
    out['long below run n windows'] = long_b['w'].nunique()
    below = g[g['srun'] < 0].dropna(subset=['ex7'])
    out['below: spearman run length vs ex7'] = pd.Series(stats.spearmanr(-below['srun'], below['ex7']), index=['rho','p'])
    g['dd_q'] = g.groupby('coin')['dd60'].transform(lambda s: pd.qcut(s, 5, labels=False))
    out['ex7 by dd60 quintile (0=deepest)'] = g.groupby('dd_q').apply(summ)
    g['z_b'] = pd.cut(g['z1'], [-20, -2, -1, 0, 1, 2, 20])
    out['ex7 by last-day z-move'] = g.groupby('z_b').apply(summ)
    X = pd.concat(D)
    def dsum(grp):
        x = grp['coin_return'].dropna()
        return pd.Series({'n': len(x), 'mean': x.mean(), 't': x.mean()/(x.std()/np.sqrt(len(x)))})
    out['sat & wed by coin'] = X[X['wd'].isin([2,5])].groupby(['wd','coin']).apply(dsum)
    out['saturday by year'] = X[X['wd']==5].groupby('year').apply(dsum)
    bk = X.groupby(['w','day'])['book_return'].mean().dropna()
    q = bk.quantile([0.01, 0.99])
    out['book tail counts'] = pd.Series({'n_low': (bk<=q.iloc[0]).sum(), 'n_high': (bk>=q.iloc[1]).sum(),
                                         'sum_low': bk[bk<=q.iloc[0]].sum(), 'sum_high': bk[bk>=q.iloc[1]].sum(),
                                         'total': bk.sum()})
    return out
