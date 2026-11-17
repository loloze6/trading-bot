def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
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
            r3 = c/c.shift(3)-1
            z3 = r3/(vol20.shift(3)*np.sqrt(3))
            fwd7 = c.shift(-7)/c-1
            fwd3 = c.shift(-3)/c-1
            ts = pd.to_datetime(b['timestamp'])
            for i in range(0, len(b), 7):
                if pd.isna(fwd7.iloc[i]): continue
                rows.append(dict(coin=coin, w=w, fwd7=fwd7.iloc[i], srun=srun.iloc[i], z1=z1.iloc[i], z3=z3.iloc[i],
                                 year=ts.iloc[i].year, vol=vol20.iloc[i]))
    g = pd.DataFrame(rows)
    g['ex7'] = g['fwd7'] - g.groupby('coin')['fwd7'].transform('mean')
    def reg(df, x):
        df = df.dropna(subset=[x, 'ex7'])
        r = stats.linregress(df[x], df['ex7'])
        return pd.Series({'n': len(df), 'slope': r.slope, 't': r.slope/r.stderr})
    out['ex7 on z1, all'] = reg(g, 'z1')
    out['ex7 on z1 by coin'] = g.groupby('coin').apply(lambda d: reg(d, 'z1'))
    out['ex7 on z1 by year'] = g.groupby('year').apply(lambda d: reg(d, 'z1'))
    out['ex7 on z3, all'] = reg(g, 'z3')
    out['ex7 on z1 clipped +-3'] = reg(g.assign(z1=g['z1'].clip(-3, 3)), 'z1')
    gp = g[g['z1'] > 0]
    out['ex7 on z1, up days only'] = reg(gp, 'z1')
    gn = g[g['z1'] < 0]
    out['ex7 on z1, down days only'] = reg(gn, 'z1')
    lb = g[g['srun'] <= -14].copy(); lb['len'] = -lb['srun']
    out['below run >=14: ex7 on length'] = reg(lb, 'len')
    out['below run >=14: ex7 on length by coin'] = lb.groupby('coin').apply(lambda d: reg(d, 'len'))
    return out
