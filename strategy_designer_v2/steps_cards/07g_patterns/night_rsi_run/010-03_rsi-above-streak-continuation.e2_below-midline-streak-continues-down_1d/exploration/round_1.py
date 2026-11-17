def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    daily = []
    fc = 'debug_info.components.rsi_below_age.last_history_value'
    for coin in data['bars']:
        # coin's mean 7d return over all windows (grid)
        allg = []
        for w, b in data['bars'][coin].items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float)
            d = c.diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100/(1+up/dn)
            side = np.sign(rsi-50)
            run = side.groupby((side != side.shift()).cumsum()).cumcount()+1
            signed_run = run*side
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            past7 = c/c.shift(7)-1
            past30 = c/c.shift(30)-1
            fwd7 = c.shift(-7)/c-1
            ts = pd.to_datetime(b['timestamp'])
            for i in range(0, len(b), 7):
                if pd.isna(fwd7.iloc[i]): continue
                rows.append(dict(coin=coin, w=w, fwd7=fwd7.iloc[i], rsi=rsi.iloc[i], srun=signed_run.iloc[i],
                                 vol20=vol20.iloc[i], past7=past7.iloc[i], past30=past30.iloc[i],
                                 fc=b['forecast'].iloc[i], alloc=b['postRebalance_current_allocation'].iloc[i],
                                 year=ts.iloc[i].year))
            dd = data['days'][coin][w].copy()
            dd['coin'] = coin; dd['w'] = w
            dd['wd'] = pd.to_datetime(dd['day']).dt.dayofweek
            daily.append(dd)
    g = pd.DataFrame(rows)
    g['ex7'] = g['fwd7'] - g.groupby('coin')['fwd7'].transform('mean')
    def summ(grp):
        x = grp['ex7'].dropna()
        return pd.Series({'n': len(x), 'mean_ex7': x.mean(), 't': x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    g['rsi_q'] = pd.qcut(g['rsi'], 5, labels=False)
    out['ex7 by rsi quintile'] = g.groupby('rsi_q').apply(summ)
    g['srun_b'] = pd.cut(g['srun'], [-200, -30, -14, -7, -1, 0, 7, 14, 30, 200])
    out['ex7 by signed run'] = g.groupby('srun_b').apply(summ)
    g['p7_q'] = g.groupby('coin')['past7'].transform(lambda s: pd.qcut(s, 5, labels=False))
    out['ex7 by past7 quintile'] = g.groupby('p7_q').apply(summ)
    g['p30_q'] = g.groupby('coin')['past30'].transform(lambda s: pd.qcut(s, 5, labels=False))
    out['ex7 by past30 quintile'] = g.groupby('p30_q').apply(summ)
    g['v_q'] = g.groupby('coin')['vol20'].transform(lambda s: pd.qcut(s, 5, labels=False))
    out['ex7 by vol20 quintile'] = g.groupby('v_q').apply(summ)
    out['ex7 by coin x rsi quintile'] = g.groupby(['coin', 'rsi_q']).apply(summ)
    out['ex7 by year'] = g.groupby('year').apply(summ)
    D = pd.concat(daily)
    D['coin_mean'] = D.groupby('coin')['coin_return'].transform('mean')
    def dsum(grp):
        x = grp['coin_return'].dropna()
        return pd.Series({'n': len(x), 'mean': x.mean(), 't': x.mean()/(x.std()/np.sqrt(len(x)))})
    out['coin daily ret by weekday'] = D.groupby('wd').apply(dsum)
    bk = D.groupby(['w', 'day'])['book_return'].mean().dropna()
    out['book daily mean/sd/n'] = pd.Series({'mean': bk.mean(), 'sd': bk.std(), 'n': len(bk),
                                            'sharpe': bk.mean()/bk.std()*np.sqrt(365)})
    out['grid alloc stats'] = g.groupby(g['alloc'] < 0)['ex7'].agg(['count', 'mean'])
    return out
