import pandas as pd, numpy as np
from scipy import stats

def rsi(c, n=14):
    d = np.diff(c, prepend=np.nan)
    up = pd.Series(np.where(d > 0, d, 0.0)); dn = pd.Series(np.where(d < 0, -d, 0.0))
    au = up.ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    ad = dn.ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    r = 100 - 100/(1 + au/ad)
    r[:n] = np.nan
    return r.values

def explore(data):
    out = {}
    col = 'debug_info.components.rsi_below_age.last_history_value'
    rows = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df['close'].values; v = df[col].values; R = rsi(c); n = len(df)
            for h in (7, 14):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, wi=int(w[1:]), h=h, age=v[i], rsi=R[i],
                                     ret=c[i+h]/c[i]-1,
                                     past=(c[i]/c[i-h]-1) if i >= h else np.nan))
    g = pd.DataFrame(rows)
    g['ex'] = g['ret'] - g.groupby(['coin', 'h'])['ret'].transform('mean')
    g['fold'] = pd.cut(g['wi'], [0, 6, 12, 18, 24], labels=['A', 'B', 'C', 'D'])
    res = []
    for h in (7, 14):
        s = g[g.h == h]
        for nm, d, x in [('rsi_all', s, 'rsi'), ('rsi_below50', s[s.rsi < 50], 'rsi'),
                         ('rsi_above50', s[s.rsi > 50], 'rsi'),
                         ('run_le20_below', s[(s.age < 0) & (s.age >= -20)], 'age'),
                         ('run_below_noC', s[(s.age < 0) & (s.fold != 'C')], 'age')]:
            d = d.dropna(subset=[x, 'ex'])
            xx = d[x] if x == 'rsi' else -d[x]
            r = stats.linregress(xx, d['ex'])
            res.append(dict(h=h, set=nm, n=len(d), slope=r.slope, t=r.slope/r.stderr))
    out['slopes'] = pd.DataFrame(res)
    s = g[(g.h == 7)].dropna(subset=['age'])
    s['side'] = np.where(s.age < 0, 'below', 'above')
    out['side7_by_fold'] = s.groupby(['fold', 'side'])['ex'].agg(['count', 'mean'])
    out['side7_by_coin'] = s.groupby(['coin', 'side'])['ex'].agg(['count', 'mean', 'std'])
    b = s[s.side == 'below'].copy()
    b['bin'] = pd.cut(-b['age'], [0, 3, 7, 14, 30, 61])
    out['bins7_below'] = b.groupby('bin')['ex'].agg(['count', 'mean', 'std'])
    d = g[(g.h == 7)].dropna(subset=['rsi', 'ex'])
    d['rbin'] = pd.cut(d['rsi'], [0, 30, 40, 45, 50, 55, 60, 70, 100])
    out['rsi_bins7'] = d.groupby('rbin')['ex'].agg(['count', 'mean', 'std'])
    return out
