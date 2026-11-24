import numpy as np, pandas as pd
from scipy import stats

def ctstat(dev, day):
    df = pd.DataFrame({'d': dev, 'day': day}).dropna()
    N = len(df)
    if N < 5: return np.nan, np.nan, N, 0
    m = df.d.mean()
    g = df.groupby('day').d.agg(['sum', 'count'])
    D = len(g)
    if D < 3: return m, np.nan, N, D
    r = g['sum'] - g['count'] * m
    var = D / (D - 1) * (r ** 2).sum() / N ** 2
    return m, m / np.sqrt(var), N, D

def explore(data):
    H = 10
    rows = []
    for coin, wins in data['bars'].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float)
            r1 = c.pct_change()
            vol60 = r1.rolling(60, min_periods=20).std()
            vs = (c / c.shift(10) - 1) / (vol60 * np.sqrt(10))
            ret3 = (c / c.shift(3) - 1) / (vol60 * np.sqrt(3))
            ret30 = (c / c.shift(30) - 1) / (vol60 * np.sqrt(30))
            vol20 = r1.rolling(20, min_periods=10).std()
            sgn = np.sign(r1)
            streak = np.zeros(len(b))
            for i in range(len(b)):
                if i == 0 or np.isnan(r1.iloc[i]) or sgn.iloc[i] == 0:
                    streak[i] = 0
                elif i > 0 and sgn.iloc[i] == sgn.iloc[i-1] and streak[i-1] != 0:
                    streak[i] = streak[i-1] + sgn.iloc[i]
                else:
                    streak[i] = sgn.iloc[i]
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b['timestamp'])
            reg = b['regime'].astype(str)
            # bars in regime run
            run = (reg != reg.shift()).cumsum()
            age = b.groupby(run).cumcount()
            for i in range(0, len(b), H):
                if np.isnan(fwd.iloc[i]): continue
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(), fwd=fwd.iloc[i],
                                 vs=vs.iloc[i], r3=ret3.iloc[i], r30=ret30.iloc[i], vol20=vol20.iloc[i],
                                 vol60=vol60.iloc[i], streak=streak[i], reg=reg.iloc[i], age=age.iloc[i],
                                 fc=b['forecast'].iloc[i], wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year))
    df = pd.DataFrame(rows)
    drift = df.groupby('coin').fwd.mean()
    df['dev'] = df.fwd - df.coin.map(drift)
    out = {}
    def tab(col, bins=None, q=None):
        d = df.dropna(subset=[col]).copy()
        if q: d['g'] = pd.qcut(d[col], q, duplicates='drop')
        elif bins is not None: d['g'] = pd.cut(d[col], bins)
        else: d['g'] = d[col]
        res = []
        for g, s in d.groupby('g', observed=True):
            m, t, n, D = ctstat(s.dev.values, s.day.values)
            res.append(dict(g=str(g), mean_dev=m, t=t, n=n, days=D))
        return pd.DataFrame(res)
    out['vs10 bins'] = tab('vs', bins=[-10, -1.5, -0.9487, -0.5, 0, 0.5, 0.9487, 1.5, 2.2, 10])
    out['r3 scaled bins'] = tab('r3', bins=[-10, -1.5, -0.75, 0, 0.75, 1.5, 10])
    out['r30 scaled bins'] = tab('r30', bins=[-10, -1.5, -0.75, 0, 0.75, 1.5, 10])
    out['streak'] = tab('streak', bins=[-20, -4.5, -2.5, -0.5, 0.5, 2.5, 4.5, 20])
    out['vol20 quint'] = tab('vol20', q=5)
    out['regime'] = tab('reg')
    tr = df[df.reg == 'trending'].copy()
    tr['ageg'] = pd.cut(tr.age, [-1, 2, 6, 15, 200])
    res = []
    for g, s in tr.groupby('ageg', observed=True):
        m, t, n, D = ctstat(s.dev.values, s.day.values); res.append(dict(g=str(g), mean_dev=m, t=t, n=n, days=D))
    out['trending by age'] = pd.DataFrame(res)
    res = []
    for g, s in df.groupby('yr'):
        m, t, n, D = ctstat(s.dev.values, s.day.values)
        st = s[s.vs >= 0.9487]
        m2, t2, n2, D2 = ctstat(st.dev.values, st.day.values)
        res.append(dict(yr=g, all_dev=m, n=n, up_dev=m2, up_t=t2, up_n=n2))
    out['by year'] = pd.DataFrame(res)
    # daily returns weekday
    dl = []
    for coin, wins in data['days'].items():
        for w, d in wins.items():
            dd = d.copy(); dd['coin'] = coin; dl.append(dd)
    D = pd.concat(dl)
    D['wd'] = pd.to_datetime(D['day']).dt.weekday
    out['weekday coin ret'] = D.groupby('wd').coin_return.agg(['mean', 'std', 'count']).assign(t=lambda x: x['mean'] / x['std'] * np.sqrt(x['count']))
    out['weekday book ret'] = D.groupby('wd').book_return.agg(['mean', 'std', 'count']).assign(t=lambda x: x['mean'] / x['std'] * np.sqrt(x['count']))
    # trades
    tl = []
    for coin, wins in data['trades'].items():
        for w, t in wins.items():
            tt = t.copy(); tt['coin'] = coin; tl.append(tt)
    T = pd.concat(tl)
    T['dur_d'] = T.duration_minutes / 1440
    T['durg'] = pd.cut(T.dur_d, [0, 5, 10, 15, 30, 60, 1000])
    out['trades by duration'] = T.groupby('durg', observed=True).net_profit_loss_percent.agg(['mean', 'median', 'count'])
    T['fcg'] = pd.qcut(T.entry_forecast, 4, duplicates='drop')
    out['trades by entry fc'] = T.groupby('fcg', observed=True).net_profit_loss_percent.agg(['mean', 'median', 'count'])
    out['trades by coin'] = T.groupby('coin').net_profit_loss_percent.agg(['mean', 'count'])
    return out
