import numpy as np, pandas as pd
from scipy import stats

def _ct(x, d):
    x = np.asarray(x, float); d = np.asarray(d)
    m = np.isfinite(x)
    x = x[m]; d = d[m]
    if len(x) < 5: return (np.nan, np.nan, len(x))
    mu = x.mean()
    s = pd.Series(x - mu).groupby(d).sum()
    se = np.sqrt((s**2).sum()) / len(x)
    return (mu, mu/se if se > 0 else np.nan, len(x))

def _summ(df, val, by):
    rows = []
    for k, g in df.groupby(by, observed=True):
        mu, t, n = _ct(g[val], g['day'])
        rows.append({'group': str(k), 'mean': round(mu, 5), 't': round(t, 2), 'n': n, 'days': g['day'].nunique()})
    return pd.DataFrame(rows)

def explore(data):
    H = 3
    recs = []
    daily = []
    for coin, wins in data['bars'].items():
        allg = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b['close'].values
            n = len(b)
            fwd = np.full(n, np.nan)
            fwd[:n-H] = c[H:] / c[:n-H] - 1
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            f1 = np.full(n, np.nan); f1[:-1] = c[1:] / c[:-1] - 1
            cs = pd.Series(c)
            hi30 = cs.rolling(30, min_periods=30).max()
            depth = c / hi30.values - 1
            r60 = cs / cs.shift(60) - 1
            r7 = cs / cs.shift(7) - 1
            vol = pd.Series(r1).rolling(20, min_periods=20).std()
            volrank = vol.rank(pct=True)
            ts = pd.to_datetime(b['timestamp'])
            d = pd.DataFrame({'coin': coin, 'win': w, 'pos': np.arange(n), 'fwd': fwd, 'r1': r1, 'f1': f1,
                              'depth': depth, 'r60': r60.values, 'r7': r7.values, 'volrank': volrank.values,
                              'regime': b['regime'].values, 'fc': b['forecast'].values,
                              'alloc': b['postRebalance_current_allocation'].values,
                              'day': ts.dt.floor('D').values, 'wd': ts.dt.weekday.values,
                              'year': ts.dt.year.values})
            allg.append(d)
        cd = pd.concat(allg)
        grid = cd[cd['pos'] % H == 0]
        mu = grid['fwd'].mean()
        cd['ufwd'] = cd['fwd'] - mu
        cd['mu1'] = cd['f1'] - cd['f1'].mean()
        recs.append(cd)
    D = pd.concat(recs)
    D['fc_on'] = D['regime'] == 'unknown'
    G = D[(D['pos'] % H == 0)].copy()
    out = {}
    out['regime counts'] = D['regime'].value_counts()
    # depth quintile within falling calm vs elsewhere
    G['dq'] = pd.qcut(G['depth'], 5, labels=False, duplicates='drop')
    out['ufwd by depth q, falling calm'] = _summ(G[G.fc_on], 'ufwd', 'dq')
    out['ufwd by depth q, other'] = _summ(G[~G.fc_on], 'ufwd', 'dq')
    # 60d trend buckets everywhere
    G['tr'] = pd.cut(G['r60'], [-9, -0.3, -0.1, 0.1, 0.3, 9])
    out['ufwd by 60d trend'] = _summ(G, 'ufwd', 'tr')
    out['ufwd by 60d trend, falling calm only'] = _summ(G[G.fc_on], 'ufwd', 'tr')
    # 7-day return quintiles
    G['r7q'] = pd.qcut(G['r7'], 5, labels=False, duplicates='drop')
    out['ufwd by 7d ret q, all'] = _summ(G, 'ufwd', 'r7q')
    out['ufwd by 7d ret q, falling calm'] = _summ(G[G.fc_on], 'ufwd', 'r7q')
    # large 1-day moves next-day (daily, every day: 1 step horizon non-overlapping)
    D['r1q'] = pd.qcut(D['r1'], 10, labels=False, duplicates='drop')
    out['next-day unusual by 1d ret decile'] = _summ(D, 'mu1', 'r1q')
    out['next-day unusual by 1d ret decile, falling calm'] = _summ(D[D.fc_on], 'mu1', pd.qcut(D[D.fc_on]['r1'], 5, labels=False))
    # vol level
    G['vq'] = pd.cut(G['volrank'], [0, .33, .66, 1.0])
    out['ufwd by window-vol tercile'] = _summ(G, 'ufwd', 'vq')
    out['next-day unusual by weekday'] = _summ(D, 'mu1', 'wd')
    out['ufwd falling calm by year'] = _summ(G[G.fc_on], 'ufwd', 'year')
    # book daily returns
    dd = []
    for coin, wins in data['days'].items():
        for w, t in wins.items():
            t = t.copy(); t['coin'] = coin; t['win'] = w; dd.append(t)
    DD = pd.concat(dd)
    bk = DD.groupby(['win', 'day'])[['book_return', 'coin_return']].mean().dropna()
    out['book vs coin corr'] = float(bk.corr().iloc[0, 1])
    bk['bq'] = pd.qcut(bk['book_return'].rank(method='first'), 20, labels=False)
    top = bk[bk.bq == 19]; bot = bk[bk.bq == 0]
    out['book top5% days: mean book, mean coins'] = f"{top.book_return.mean():.4f}, {top.coin_return.mean():.4f}, n={len(top)}"
    out['book bottom5% days: mean book, mean coins'] = f"{bot.book_return.mean():.4f}, {bot.coin_return.mean():.4f}, n={len(bot)}"
    bw = bk.groupby(level=0)['book_return'].agg(['mean', 'count'])
    out['book by window'] = bw
    # trades
    tr = []
    for coin, wins in data['trades'].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t['coin'] = coin; tr.append(t)
    T = pd.concat(tr)
    T['dur_d'] = T['duration_minutes'] / 1440
    T['durq'] = pd.cut(T['dur_d'], [0, 3.5, 7, 15, 1000])
    out['trades by duration'] = T.groupby('durq', observed=True)['net_profit_loss_percent'].agg(['mean', 'count', 'median'])
    out['trades by coin'] = T.groupby('coin')['net_profit_loss_percent'].agg(['mean', 'count'])
    return out
