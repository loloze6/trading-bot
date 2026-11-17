import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    col = 'debug_info.components.rsi_below_age.last_history_value'
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df['close'].values
            v = df[col].values
            n = len(df)
            for h in (7, 14, 28):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, wi=int(w[1:]),
                                     age=v[i], ret=c[i+h]/c[i]-1,
                                     pos=df['postRebalance_current_allocation'].iloc[i],
                                     past14=(c[i]/c[i-14]-1) if i >= 14 else np.nan))
    g = pd.DataFrame(rows)
    g['ex'] = g['ret'] - g.groupby(['coin', 'h'])['ret'].transform('mean')
    out['age_range'] = g['age'].describe()
    res = []
    for h in (7, 14, 28):
        for side in ('below', 'above'):
            s = g[(g.h == h) & ((g.age < 0) if side == 'below' else (g.age > 0))].dropna(subset=['age', 'ex'])
            x = s['age'].abs()
            r = stats.linregress(x, s['ex'])
            res.append(dict(h=h, side=side, n=len(s), mean_ex=s['ex'].mean(),
                            t_mean=s['ex'].mean()/(s['ex'].std()/np.sqrt(len(s))),
                            slope=r.slope, t_slope=r.slope/r.stderr))
    out['by_h_side'] = pd.DataFrame(res)
    s = g[(g.h == 14) & (g.age < 0)].copy()
    s['run'] = -s['age']
    s['bin'] = pd.cut(s['run'], [0, 5, 10, 20, 40, 61])
    out['bins14_below'] = s.groupby('bin')['ex'].agg(['count', 'mean', 'std'])
    s['fold'] = pd.cut(s['wi'], [0, 6, 12, 18, 24], labels=['A', 'B', 'C', 'D'])
    out['coin_fold_slope'] = s.groupby(['coin', 'fold']).apply(
        lambda d: pd.Series(dict(n=len(d), mean_ex=d['ex'].mean(),
                                 corr=d[['run', 'ex']].corr().iloc[0, 1])))
    a = g[(g.h == 14) & (g.age > 0)].copy()
    a['bin'] = pd.cut(a['age'], [0, 5, 10, 20, 40, 61])
    out['bins14_above'] = a.groupby('bin')['ex'].agg(['count', 'mean', 'std'])
    return out
