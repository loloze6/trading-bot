import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    C = 'debug_info.components.rsi_below_age.last_history_value'
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            n = len(b)
            lr = np.log(b['close']).diff()
            vol20 = lr.rolling(20).std().values
            r7p = b['close'].pct_change(7).values
            r14p = b['close'].pct_change(14).values
            for h in (7, 14):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     fwd=c[i+h]/c[i]-1,
                                     run=b[C].iloc[i] if C in b else np.nan,
                                     r7p=r7p[i], r14p=r14p[i], vol=vol20[i],
                                     pos=b['postRebalance_current_allocation'].iloc[i],
                                     wd=pd.Timestamp(b['timestamp'].iloc[i]).weekday()))
    g = pd.DataFrame(rows)
    g['ex'] = g['fwd'] - g.groupby(['coin','h'])['fwd'].transform('mean')

    def tab(df, col, q=5):
        d = df.dropna(subset=[col, 'ex']).copy()
        d['b'] = d.groupby('coin')[col].transform(lambda s: pd.qcut(s.rank(method='first'), q, labels=False))
        t = d.groupby('b')['ex'].agg(['mean', 'count', 'std'])
        t['t'] = t['mean'] / (t['std'] / np.sqrt(t['count']))
        sl = stats.linregress(d[col], d['ex'])
        t.loc['slope_t', 'mean'] = sl.slope / sl.stderr
        return t

    g14 = g[g.h == 14]; g7 = g[g.h == 7]
    out['14d excess by signed run quintile'] = tab(g14, 'run')
    a = g14[g14.run > 0]
    out['14d excess by run>0 (above 50) quintile'] = tab(a, 'run', 3)
    out['14d excess by past14d return quintile'] = tab(g14, 'r14p')
    out['7d excess by past7d return quintile'] = tab(g7, 'r7p')
    out['7d excess by vol20 quintile'] = tab(g7, 'vol')
    # weekday daily returns
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x['coin'] = coin; x['w'] = w
            d.append(x)
    D = pd.concat(d)
    D['wd'] = pd.to_datetime(D['day']).dt.weekday
    D['yr'] = pd.to_datetime(D['day']).dt.year
    t = D.groupby('wd')['coin_return'].agg(['mean', 'count', 'std'])
    t['t'] = t['mean'] / (t['std'] / np.sqrt(t['count']))
    out['coin daily return by weekday'] = t
    t = D.groupby('yr')[['book_return', 'coin_return']].mean()
    out['book vs coin mean daily by year'] = t
    # book by position sign
    pr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            p = b['postRebalance_current_allocation']
            r = b['close'].shift(-1) / b['close'] - 1
            pr.append(pd.DataFrame({'p': p, 'g': p * r, 'r': r, 'run': b[C]}))
    P = pd.concat(pr).dropna()
    P['side'] = np.sign(P['p'])
    out['gain by position side'] = P.groupby('side')[['g', 'r']].agg(['mean', 'count'])
    out['share short'] = float((P.p < 0).mean())
    # streak above 50 run length effect on next day
    return out
